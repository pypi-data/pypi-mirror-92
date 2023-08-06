import json

from deform.widget import TextAreaWidget
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import find_lexer_class_by_name

SUPPORTED_EDITAREA_SYNTAX = [
    "basic",
    "c",
    "cpp",
    "html",
    "js",
    "perl",
    "python",
    "ruby",
    "tsql",
    "xml",
    "brainfuck",
    "coldfusion",
    "css",
    "java",
    "pas",
    "php",
    "robotstxt",
    "sql",
    "vb",
    "json",
]

ALT_EDITAREA_SYNTAX = {"pytb": "python"}


class CodeWidget(TextAreaWidget):

    css_class = "code"
    template = "code"
    readonly_template = "readonly/code"
    syntax = "python"

    def highlight(self, code):
        Lexer = find_lexer_class_by_name(self.syntax)
        formatter = HtmlFormatter()
        highlighted = highlight(code, Lexer(), formatter)
        return highlighted

    def editarea_syntax(self):
        if self.syntax in SUPPORTED_EDITAREA_SYNTAX:
            return self.syntax
        return ALT_EDITAREA_SYNTAX.get(self.syntax, "text")


class JSONCodeWidget(CodeWidget):
    """ Code widget to use with JSON/Dictionary field"""

    syntax = "json"

    def deserialize(self, field, pstruct):
        pstruct = super().deserialize(field, pstruct)
        return json.loads(pstruct)

    def serialize(self, field, cstruct, **kw):
        cstruct = json.dumps(cstruct, indent=4)
        return super().serialize(field, cstruct, **kw)
