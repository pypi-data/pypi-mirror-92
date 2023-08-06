import os
import tempfile

import morepath
import morpcc
import morpfw
import morpfw.sql as morpsql
import yaml
from morpfw.tests.common import create_admin, get_client, make_request

from . import democms


def get_democms_client():

    morepath.scan(morpfw)
    morepath.scan(morpcc)
    morepath.scan(democms)

    settings_file = os.path.join(os.path.dirname(__file__), "democms/settings.yml")
    with open(settings_file) as sf:
        settings = yaml.load(sf, Loader=yaml.Loader)

    settings["configuration"][
        "morpfw.storage.sqlstorage.dburi"
    ] = "postgresql://postgres@localhost:45678/morpcc_tests"

    settings["configuration"][
        "morpfw.storage.sqlstorage.dburi.warehouse"
    ] = "postgresql://postgres@localhost:45678/morpcc_warehouse"

    settings["configuration"][
        "morpfw.beaker.session.url"
    ] = "postgresql://postgres@localhost:45678/morpcc_cache"

    test_settings = tempfile.mktemp()
    with open(test_settings, "w") as ts:
        yaml.dump(settings, ts)

    c = get_client(test_settings)
    os.unlink(test_settings)

    req = c.mfw_request
    morpsql.Base.metadata.create_all(bind=req.db_session.bind)

    create_admin(req, "admin", "password", "admin@localhost.local")

    return c


def follow(resp):
    while resp.status_code == 302:
        resp = resp.follow()

    return resp

