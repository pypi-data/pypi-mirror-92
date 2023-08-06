import os
import time
from datetime import datetime

import pytz
from a_un import load_license, validate_license

from ..app import App
from ..root import Root


@App.html(model=Root, name="license", template="master/license.pt")
def view(context, request):
    copyright_notice = request.app.get_copyright_notice(request)
    license = request.get_license()
    return {
        "hide_title": True,
        "copyright_notice": copyright_notice,
        "license": license,
        "license_expired": license["expired"] if license else None,
    }
