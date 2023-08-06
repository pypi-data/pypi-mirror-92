import morpfw

from .. import permission as perm
from ..app import App
from .modelui import SettingCollectionUI


@App.html(
    model=SettingCollectionUI,
    name="listing",
    permission=perm.ManageSite,
    template="master/setting/listing.pt",
)
def listing(context, request):
    page_name = request.GET.get("page", "general")
    page = request.app.config.setting_page_registry.get(request, page_name)
    pages = request.app.config.setting_page_registry.values(request)
    pages = [v for v in pages if v.enabled(context, request)]
    form = page.form(context, request)
    data = page.form_data(context, request)
    return {
        "current_page": page_name,
        "pages": pages,
        "page_title": "Settings",
        "form_title": page.title,
        "form": form,
        "form_data": data,
    }


@App.html(
    model=SettingCollectionUI,
    name="listing",
    permission=perm.ManageSite,
    template="master/setting/listing.pt",
    request_method="POST",
)
def process_listing(context, request):
    page_name = request.GET.get("page", "general")
    page = request.app.config.setting_page_registry.get(request, page_name)
    pages = request.app.config.setting_page_registry.values(request)
    pages = [v for v in pages if v.enabled(context, request)]
    error = page.process_form(context, request)
    if not error:
        request.notify(
            "success", "Settings saved", "Configuration have been successfully updated"
        )
        return morpfw.redirect(request.url)
    return {
        "current_page": page_name,
        "pages": pages,
        "page_title": "Settings",
        "form_title": page.title,
        "form": error["form"],
        "form_data": error["form_data"],
    }
