# Import smtplib for the actual sending function
import smtplib
import socket

# Import the email modules we'll need
from email.message import EmailMessage

import morpfw

from ..app import App

SIGNAL = "morpcc.messaging.email"


class EmailMessagingProvider(object):
    def __init__(self, request):
        self.request = request
        self.app = request.app

    def send(self, to, subject, message):
        (
            self.app.async_dispatcher(SIGNAL).dispatch(
                self.request, obj={"to": to, "subject": subject, "message": message}
            )
        )


@App.async_subscribe(SIGNAL)
def send_email(request_options, obj):
    with morpfw.request_factory(**request_options) as request:
        app = request.app
        from_ = app.get_config("morpcc.smtp.from", f"no-reply@{socket.gethostname()}")
        smtphost = app.get_config("morpcc.smtp.host", "localhost")
        smtpport = app.get_config("morpcc.smtp.port", 25)

    # Open the plain text file whose name is in textfile for reading.
    msg = EmailMessage()
    msg.set_content(obj["message"])

    # me == the sender's email address
    # you == the recipient's email address
    msg["Subject"] = "Hello world"
    msg["From"] = from_
    msg["To"] = obj["to"]

    # Send the message via our own SMTP server.
    s = smtplib.SMTP(smtphost, smtpport)
    s.send_message(msg)
    s.quit()

    return {}


# @App.periodic(name=SIGNAL, seconds=120)
# def retry_send_email(request):
#    return {}
#


@App.messagingprovider("email")
def get_email_provider(request, name):
    return EmailMessagingProvider(request)
