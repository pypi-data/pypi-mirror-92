from .app import App
from morpcc.portlet import navigation_portlet as old_nav


@App.portlet(name='morpcc.main_navigation', template='master/portlet/navigation.pt')
def new_main_nav(context, request):
    result = old_nav(context, request)
    result['navtree'][0]['children'].append({
        'title': 'Hello', 'icon': 'home', 'href': 'http://www.google.com'
    })
    return result
