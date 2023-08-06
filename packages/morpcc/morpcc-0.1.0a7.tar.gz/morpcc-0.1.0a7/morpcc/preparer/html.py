from html_sanitizer import Sanitizer as _Sanitizer


class HTMLSanitizer(object):
    def __init__(self, settings=None):
        if settings is None:
            settings = {
                "tags": (
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "a",
                    "strong",
                    "em",
                    "p",
                    "ul",
                    "ol",
                    "li",
                    "br",
                    "sub",
                    "sup",
                    "hr",
                ),
            }
        self.sanitizer = _Sanitizer(settings)

    def __call__(self, request, schema, value, mode=None):
        if value:
            return self.sanitizer.sanitize(value)
        return None
