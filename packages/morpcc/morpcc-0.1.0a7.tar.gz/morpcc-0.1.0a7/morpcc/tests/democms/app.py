import morpfw
import morpcc
from morpcc import permission as ccperm


class App(morpcc.App):
    pass


class AppRoot(morpcc.Root):
    pass


@App.path(model=AppRoot, path='/')
def get_approot(request):
    return AppRoot(request)


@App.template_directory()
def get_template_directory():
    return 'templates'
