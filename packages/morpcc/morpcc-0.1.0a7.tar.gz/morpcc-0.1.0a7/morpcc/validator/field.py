import re

valid_refdatakey_pattern = re.compile(r"^[A-Z0-9_\- ]*$")


def valid_refdatakey(request, schema, field, value, mode=None):
    if not valid_refdatakey_pattern.match(value):
        return "Only upper cased alphanumeric, _, -, and spaces are accepted"
