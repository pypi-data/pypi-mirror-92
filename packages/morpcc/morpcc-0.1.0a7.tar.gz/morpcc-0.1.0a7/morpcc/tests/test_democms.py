# Copyright (c) 2019 Mohd Izhar Firdaus Bin Ismail
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import tempfile

import morepath
import morpcc
import morpcc.authn.storage
import morpfw
import morpfw.sql as morpsql
import yaml
from morpfw.tests.common import create_admin, get_client, make_request

from . import democms
from .democms.app import App
from .democms_common import follow, get_democms_client

pages = [
    "/",
    "/profile/+view",
    "/page/+listing",
    "/page/+create",
    "/page/+modal-create",
    "/page/+datatable.json",
    "/+site-settings",
]


def test_democms(pgsql_db, pgsql_db_warehouse, pgsql_db_cache):
    c = get_democms_client()
    r = c.get("/")
    # test redirect to login page
    assert r.status_code == 302
    assert r.headers["Location"].split("?")[0].endswith("/login")

    # test login
    r = c.post(
        r.headers["Location"],
        {
            "__formid_": "deform",
            "username": "admin",
            "password": "password",
            "Submit": "Login",
        },
    )

    assert "userid" in c.cookies.keys()

    # test load homepage
    r = c.get("/")

    assert r.status_code == 200

    # test load common pages
    for p in pages:
        r = c.get(p)
        assert r.status_code == 200

    # create page
    r = c.post(
        "/page/+create",
        {
            "__formid__": "deform",
            "title": "pagetitle",
            "description": "pagedesc",
            "location": "pageloc",
            "body": "pagebody",
            "Submit": "submit",
        },
    )

    assert r.status_code == 302

    page_url = r.headers["Location"]

    # read
    r = r.follow().follow()

    assert r.status_code == 200

    # edit page

    r = c.post(
        page_url + "/+edit",
        {
            "__formid__": "deform",
            "title": "pagetitle",
            "description": "pagedesc",
            "location": "pageloc",
            "body": "pagebody2",
            "Submit": "submit",
        },
    )

    assert r.status_code == 302

    # read
    r = follow(r)

    assert r.status_code == 200

    # delete
    r = c.post(page_url + "/+delete", {},)

    # read
    r = c.get(page_url, expect_errors=True)
    assert r.status_code == 404
