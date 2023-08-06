import string

import nltk
import rulez
from morpfw.crud.searchprovider.base import SearchProvider

from ..app import App
from .model import IndexContentCollection


class IndexSearchProvider(SearchProvider):
    def parse_query(self, qs):
        if qs is None:
            return None
        if not qs.strip():
            return None

        query = qs.translate(str.maketrans("", "", string.punctuation)).lower()

        if not query.strip():
            return None

        query = " & ".join(nltk.word_tokenize(query))
        return {"field": "searchabletext", "operator": "match", "value": query}

    def search(self, query=None, offset=0, limit=None, order_by=None):
        idxcol = self.context
        lorder_by = []
        order_by = order_by or []
        indexes = [idx["name"] for idx in idxcol.__parent__.search()]
        for ob in order_by:
            if ob[0] in indexes:
                lorder_by.append(ob)
        if not lorder_by:
            lorder_by = None
        return idxcol.search(query, offset, limit, order_by=lorder_by)


@App.searchprovider(model=IndexContentCollection)
def get_searchprovider(context):
    return IndexSearchProvider(context)
