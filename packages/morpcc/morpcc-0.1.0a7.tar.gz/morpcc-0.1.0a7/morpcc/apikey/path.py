from .model import APIKeyModelUI, APIKeyCollectionUI
from ..app import App
from morpfw.authn.pas.apikey.path import get_apikey, get_apikey_collection


@App.path(model=APIKeyCollectionUI, path='/manage-apikeys')
def get_apikey_collection_ui(request):
    col = get_apikey_collection(request)
    return APIKeyCollectionUI(request, col)


@App.path(model=APIKeyModelUI, path='/manage-apikeys/{identifier}',
          variables=lambda obj: {'identifier': obj.model.data['uuid']})
def get_apikey_model_ui(request, identifier):
    apikey = get_apikey(request, identifier)
    col = get_apikey_collection(request)
    return APIKeyModelUI(request, apikey, APIKeyCollectionUI(request, col))
