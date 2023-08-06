from deform.widget import SequenceWidget


def patch():
    from deform.compat import string_types, url_quote

    def prototype(self, field, **kw):
        # we clone the item field to bump the oid (for easier
        # automated testing; finding last node)
        item_field = field.children[0].clone()
        if not item_field.name:
            info = "Prototype for %r has no name" % field
            raise ValueError(info)
        # NB: item_field default should already be set up
        proto = item_field.render_template(self.item_template, parent=field, **kw)
        if isinstance(proto, string_types):
            proto = proto.encode("utf-8")
        proto = url_quote(proto)
        return proto

    if not getattr("SequenceWidget", "__prototype_patched", False):
        SequenceWidget.prototype = prototype
        SequenceWidget.__prototype_patched = True


patch()
