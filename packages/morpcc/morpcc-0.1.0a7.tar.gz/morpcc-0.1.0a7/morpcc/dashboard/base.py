import abc
import copy
import typing
from uuid import uuid4

from morepath import Response


class BaseWidget(abc.ABC):

    template: typing.Optional[str] = None

    def __init__(self) -> None:
        self.widget_id = "widget-%s" % uuid4().hex

    @abc.abstractmethod
    def render(self, context, request, load_template):
        raise NotImplementedError()

    @abc.abstractmethod
    def render_script(self, context, request, load_template):
        return None


class ContainerWidget(BaseWidget):

    template: typing.Optional[str] = None
    widget_css_class: typing.Optional[str] = None

    def __init__(
        self,
        *,
        contents=None,
        css_class: typing.Optional[str] = None,
        css_style: typing.Optional[str] = None
    ) -> None:
        self.contents = contents or []
        self.css_class = css_class
        self.css_style = css_style
        super().__init__()

    def add(self, widget):
        self.contents.append(widget)

    def get_css_class(self):
        if self.css_class:
            return self.css_class

    def get_css_style(self):
        if self.css_style:
            return self.css_style

    def render(self, context, request, load_template):

        widget_html = []
        for w in self.contents:
            h = w.render(context, request, load_template)
            widget_html.append(h)
        if self.template:
            data = {
                "widget": self,
                "content": "\n\n".join(widget_html),
                "css_class": self.get_css_class(),
                "css_style": self.get_css_style(),
                "load_template": load_template,
                "request": request,
            }

            template = load_template(self.template)
            html = template(**data)
        else:
            html = "\n\n".join(widget_html)

        return html

    def render_script(self, context, request, load_template):

        widget_script = []
        for w in self.contents:
            s = w.render_script(context, request, load_template)
            if s:
                widget_script.append(s)
        script = "\n\n".join(widget_script)

        return script


class Row(ContainerWidget):

    template: str = "master/dashboard/row.pt"

    def __init__(self, *, height=None, **kwargs) -> None:
        self.height = height
        super().__init__(**kwargs)


class Container(ContainerWidget):
    pass


class Column(ContainerWidget):

    template: str = "master/dashboard/col.pt"

    def __init__(
        self,
        contents=None,
        css_class: typing.Optional[str] = None,
        xs_size=None,
        sm_size=None,
        md_size=4,
        lg_size=None,
        xl_size=None,
    ):
        self.xs_size = xs_size
        self.sm_size = sm_size
        self.md_size = md_size
        self.lg_size = lg_size
        self.xl_size = xl_size
        self.css_class = css_class
        super().__init__(contents=contents, css_class=css_class)

    def get_css_class(self):
        base_css = super().get_css_class() or ""
        col_css = []
        for size in ["xs", "sm", "md", "lg", "xl"]:
            s = getattr(self, "%s_size" % size, None)
            if s:
                col_css.append("col-%s-%s" % (size, s))

        if base_css and col_css:
            css_class = "%s %s" % (" ".join(col_css), base_css)
        elif base_css:
            css_class = base_css
        elif col_css:
            css_class = " ".join(col_css)
        else:
            css_class = None

        return css_class


class Widget(Column):

    template: typing.Optional[str] = None
    widget_css_class: typing.Optional[str] = None
    default_opts: dict = {}

    def __init__(self, datasource, **kwargs):
        self.datasource = datasource
        for k, v in self.default_opts.items():
            if k not in kwargs:
                if hasattr(self, k):
                    setattr(self, k, v)
                else:
                    kwargs[k] = v
        super().__init__(**kwargs)

    def get_css_class(self):
        css_class = super().get_css_class()
        if self.widget_css_class and css_class:
            return "%s %s" % (css_class, self.widget_css_class)
        return css_class

    def get_datasource(self, request):
        return request.app.get_datasource(self.datasource, request)

    def render(self, context, request, load_template):
        source = self.get_datasource(request)
        template = load_template(self.template)
        data = source.compute()
        html = template(
            request=request,
            widget=self,
            data=data,
            css_class=self.get_css_class(),
            css_style=self.get_css_style(),
            load_template=load_template,
        )
        return html
