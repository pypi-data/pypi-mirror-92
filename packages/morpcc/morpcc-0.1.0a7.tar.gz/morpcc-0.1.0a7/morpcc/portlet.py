from datetime import datetime

import pytz
import rulez
import timeago
from morpfw.authn.pas.user.path import get_user_collection
from morpfw.crud import permission as crudperms
from webob.exc import HTTPUnauthorized

from .app import App
from .users.path import get_current_user_model_ui
from .util import permits, typeinfo_link, types_navigation


@App.portletprovider(name="morpcc.left-portlets")
def left_portlets(context, request):
    return ["morpcc.logo", "morpcc.profile", "morpcc.main_navigation"]


@App.portletprovider(name="morpcc.top-navigation")
def topnav_portlets(context, request):
    return ["morpcc.topnav"]


@App.portletprovider(name="morpcc.abovecontent-portlets")
def abovecontent_portlets(context, request):
    return ["morpcc.timezone", "morpcc.breadcrumb"]


@App.portletprovider(name="morpcc.topleft-portlets")
def topleft_portlets(context, request):
    return []


@App.portletprovider(name="morpcc.style-portlets")
def style_portlets(context, request):
    return ["morpcc.custom_styles"]


@App.portletprovider(name="morpcc.header-script-portlets")
def header_scripts_portlets(context, request):
    return ["morpcc.custom_header_scripts"]


@App.portletprovider(name="morpcc.footer-script-portlets")
def footer_scripts_portlets(context, request):
    return ["morpcc.custom_footer_scripts"]


@App.portletprovider(name="morpcc.footer-portlets")
def footer_portlets(context, request):
    return ["morpcc.footer"]


@App.portlet(name="morpcc.main_navigation", template="master/portlet/navigation.pt")
def navigation_portlet(context, request):

    general_children = [
        {"title": "Home", "icon": "home", "href": request.relative_url("/")},
    ]

    types_nav = types_navigation(request)

    navtree = []
    navtree.append({"section": "General", "children": general_children})
    if types_nav:
        navtree.append({"section": "Collections", "children": types_nav})

    return {"navtree": navtree}


@App.portlet(name="morpcc.profile", template="master/portlet/profile.pt")
def profile_portlet(context, request):
    user = get_current_user_model_ui(request)
    if user is None:
        raise HTTPUnauthorized
    username = user.model["username"]
    xattr = user.model.xattrprovider()
    if user.model.get_blob("profile-photo"):
        photo_url = request.link(user, "+download?field=profile-photo")
    else:
        photo_url = request.relative_url("/__static__/morpcc/img/person-icon.jpg")
    return {
        "displayname": xattr.get("displayname", username) or username,
        "profilephoto_url": photo_url,
        "tzinfo": user.model["timezone"] or "UTC",
    }


@App.portlet(name="morpcc.topnav", template="master/portlet/topnav.pt")
def topnav_portlet(context, request):
    now = datetime.now(tz=pytz.UTC)
    user = get_current_user_model_ui(request)
    username = user.model["username"]
    xattr = user.model.xattrprovider()
    if user.model.get_blob("profile-photo"):
        photo_url = request.link(user, "+download?field=profile-photo")
    else:
        photo_url = request.relative_url("/__static__/morpcc/img/person-icon.jpg")

    notif_col = request.get_collection("morpcc.notification").ui()
    notifs = notif_col.search(
        query=rulez.field["userid"] == request.identity.userid,
        limit=10,
        order_by=("created", "desc"),
    )
    unread_notifs = notif_col.collection.aggregate(
        query=rulez.and_(
            rulez.field["read"] == None,
            rulez.field["userid"] == request.identity.userid,
        ),
        group={"count": {"function": "count", "field": "uuid"}},
    )
    license = request.get_license()
    license_expired = False
    if license:
        license_expired = license["expired"]

    def _timeago(dt):
        return timeago.format(dt, now)

    def get_icon_url(txt):
        if not txt:
            return None
        if txt.lower().startswith("http"):
            return txt
        elif txt.startswith("/"):
            return request.relative_url(txt)
        return None

    return {
        "displayname": xattr.get("displayname", username) or username,
        "profilephoto_url": photo_url,
        "notifications": notifs,
        "notification_count": unread_notifs[0]["count"],
        "tzinfo": user.model["timezone"] or "UTC",
        "license_expired": license_expired,
        "timeago": _timeago,
        "get_icon_url": get_icon_url,
    }


@App.portlet(name="morpcc.breadcrumb", template="master/portlet/breadcrumb.pt")
def breadcrumb_portlet(context, request):
    """
    Breadcrumbs should return as 
    {
        'breadcrumb': [{'title': '...', 'url': '...', 'active': False}, 
                       {'title': '...', 'url': '...', 'active': False},
                       {'title': '...', 'url': '...', 'active': True}]
    }
    """
    breadcrumb = request.app.get_breadcrumb(context, request)
    return {"breadcrumb": breadcrumb}


@App.portlet(name="morpcc.timezone", template="master/portlet/timezone.pt")
def timezone_portlet(context, request):
    user = get_current_user_model_ui(request)
    return {"timezone": user.model["timezone"] or "UTC"}


@App.portlet(name="morpcc.logo", template="master/portlet/logo.pt")
def logo_portlet(context, request):
    return {}


@App.portlet(name="morpcc.footer", template="master/portlet/footer.pt")
def footer_portlet(context, request):
    copyright_notice = request.app.get_copyright_notice(request)
    return {"copyright_notice": copyright_notice}


@App.portlet(name="morpcc.custom_styles", template="master/portlet/custom_styles.pt")
def custom_styles_portlet(context, request):
    return {}


@App.portlet(
    name="morpcc.custom_header_scripts",
    template="master/portlet/custom_header_scripts.pt",
)
def custom_header_scripts_portlet(context, request):
    return {}


@App.portlet(
    name="morpcc.custom_footer_scripts",
    template="master/portlet/custom_footer_scripts.pt",
)
def custom_footer_scripts_portlet(context, request):
    return {}
