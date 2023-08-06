import morpfw
from webob.exc import HTTPNotFound
from ..app import App
from ..root import Root
from ..permission import ViewHome
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hmac, hashes
import binascii
import time
import json
import base64
from urllib.parse import quote


class SignedTokenProvider(object):

    def __init__(self, signature_field='sig'):
        self.signature_field = signature_field

    def _construct_message(self, payload: dict):
        keys = sorted(payload.keys())
        message = '###'.join(str(payload[k])
                             for k in keys if (k != self.signature_field))
        return message

    def _compute_signature(self, key: str, message: str):
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(message.encode('utf-8'))
        sig = h.finalize()
        return base64.b64encode(sig).decode('utf-8')

    def generate_token(self, key: str, payload: dict):
        payload = payload.copy()
        message = self._construct_message(payload)
        signature = self._compute_signature(key, message)
        payload[self.signature_field] = signature
        payload_json = json.dumps(payload).encode('utf-8')
        token = base64.b64encode(payload_json).decode('ascii')
        return token

    def load_token(self, token: str):
        try:
            payload_json = base64.b64decode(
                token.encode('ascii')).decode('utf-8')
        except binascii.Error:
            return None
        try:
            payload = json.loads(payload_json)
        except json.JSONDecodeError:
            return None
        return payload

    def verify_payload(self, key: str, payload: dict):
        message = self._construct_message(payload)
        sig = self._compute_signature(key, message)
        if payload[self.signature_field] == sig:
            return payload
        return None


@App.json(model=Root, name='send-verification', permission=ViewHome,
          request_method='POST')
def send_verification(context, request):
    app = request.app
    user = morpfw.get_current_user(request)
    destination = user['email']
    key = user['nonce'].encode('utf-8')

    payload = {'method': 'verify-email',
               'userid': request.identity.userid,
               'timestamp': int(time.time())}

    tokenprovider = SignedTokenProvider()
    token = tokenprovider.generate_token(key, payload)

    link = request.relative_url(f'/verify?token={quote(token)}')
    mailer = app.get_messagingprovider(request, 'email')
    mailer.send(to=destination, subject="Email verification",
                message=f"Hello world \n\n {link}")
    return {'message': 'Verification email sent',
            'status': 'success'}


@App.view(model=Root, name='verify', request_method='GET')
def verify(context, request):
    token = request.GET.get('token', None)
    if not token:
        raise HTTPNotFound()
    tokenprovider = SignedTokenProvider()
    payload = tokenprovider.load_token(token)

    if not payload:
        raise HTTPNotFound()

    if 'userid' not in payload:
        raise HTTPNotFound()

    user = morpfw.get_user_by_userid(request, payload['userid'])
    if not user:
        raise HTTPNotFound()

    key = user['nonce'].encode('utf-8')

    if not tokenprovider.verify_payload(key, payload):
        raise HTTPNotFound()

    xattr = user.xattrprovider()
    xattr.update({'morpfw.email.validated': True})

    return morpfw.redirect(request.relative_url('/'))
