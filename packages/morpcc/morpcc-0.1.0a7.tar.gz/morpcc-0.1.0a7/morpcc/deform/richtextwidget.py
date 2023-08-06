from deform.widget import RichTextWidget as BaseRichTextWidget

TOOLBAR1 = (
    "undo redo styleselect old italic underline strikethrough subscript superscript "
)

TOOLBAR2 = "bullist numlist outdent indent blockquote removeformat cut copy paste "


class RichTextWidget(BaseRichTextWidget):

    default_options = tuple(
        list(BaseRichTextWidget.default_options)
        + [("toolbar1", TOOLBAR1), ("toolbar2", TOOLBAR2)]
    )
