from .app import App
import morepath


@App.tween_factory()
def make_tween(app, handler):
    def set_caching_headers(request: morepath.Request):
        response = handler(request)
        if not response.headers.get('Cache-Control'):
            response.headers['Cache-Control'] = 'no-store'
        return response
    return set_caching_headers
