from .app import App
from webob import static
from webob.exc import HTTPNotFound, HTTPUnauthorized, HTTPNotModified
from pkg_resources import resource_filename
import os
import hashlib
from datetime import datetime, timedelta
from morpfw.static import StaticRoot
import morepath

ETAG = hashlib.md5(datetime.now().strftime(
    r'%Y%d%d%H').encode('ascii')).hexdigest()


class MorpCCStaticRoot(StaticRoot):

    module = 'morpcc'
    directory = 'static_files'


@App.path(model=MorpCCStaticRoot, path='/__static__/morpcc', absorb=True)
def get_staticroot(absorb):
    return MorpCCStaticRoot(absorb)


class DeformStaticRoot(StaticRoot):

    module = 'deform'
    directory = 'static'


@App.path(model=DeformStaticRoot, path='/__static__/deform', absorb=True)
def get_deformstaticroot(absorb):
    return DeformStaticRoot(absorb)
