import itertools
import json

from .base import Widget

default_color_stack = ["#455C73", "#9B59B6", "#26B99A", "#3498DB", "#BDC3C7"]


class TileStatsCount(Widget):
    """
        Requires row to have 'tile_count' class
    """

    template = "master/dashboard/tile_stats_count.pt"
    widget_css_class = "tile_stats_count"

    default_opts = {
        "xs_size": 6,
        "sm_size": 4,
        "md_size": 2,
        "lg_size": 2,
        "xl_size": 2,
    }

    def __init__(
        self,
        datasource,
        *,
        title=None,
        increment_from=None,
        icon="database",
        value_col="value",
        increment_col="increment",
        **kwargs
    ):
        self.title = title
        self.increment_from = increment_from
        self.value_col = value_col
        self.increment_col = increment_col
        self.icon = icon
        super().__init__(datasource, **kwargs)

    def chart_data(self, data):
        increment = data[0].get(self.increment_col, 0)
        value = data[0][self.value_col]
        before_inc = value - increment
        if before_inc <= 0:
            increment_percentage = 0
        else:
            increment_percentage = int((increment / before_inc) * 100)

        increment_icon = None
        if increment_percentage > 0:
            increment_icon = "sort-asc"
        elif increment_percentage < 0:
            increment_icon = "sort-desc"
        return {
            "value": value,
            "increment": abs(increment_percentage),
            "increment_icon": increment_icon,
        }


class PercentChart(Widget):

    template = "master/dashboard/percent_chart.pt"

    default_opts = {"sm_size": 4, "md_size": 4, "lg_size": 4}

    def __init__(
        self,
        datasource,
        *,
        title=None,
        limit=10,
        label_col="label",
        value_col="value",
        total_col="total",
        **kwargs
    ):
        self.title = title
        self.limit = limit
        self.label_col = label_col
        self.value_col = value_col
        self.total_col = total_col
        super().__init__(datasource, **kwargs)

    def chart_data(self, data):
        result = []
        for idx, r in enumerate(data):
            if idx > self.limit:
                break
            value = r[self.value_col]
            total = r[self.total_col]
            row = {
                "label": r[self.label_col],
                "value_percent": int((value / total) * 100),
                "value_short": self.human_value(value),
            }
            result.append(row)
        return result

    def human_value(self, value):
        if value > 10 ** 12:
            return "%sT" % int(value / (10 ** 12))
        if value > 10 ** 9:
            return "%sB" % int(value / (10 ** 9))
        if value > 10 ** 6:
            return "%sM" % int(value / (10 ** 6))
        if value > 10 ** 3:
            return "%sK" % int(value / (10 ** 3))
        return "%s" % value


class EChart(Widget):

    template = "master/dashboard/echarts.pt"

    def __init__(
        self,
        datasource,
        *,
        title=None,
        title_small=None,
        chart_height=200,
        label_col="label",
        value_col="value",
        **kwargs
    ):
        self.title = title
        self.title_small = title_small
        self.chart_height = chart_height
        self.label_col = label_col
        self.value_col = value_col
        super().__init__(datasource, **kwargs)

    def render_script(self, context, request, load_template):
        source = self.get_datasource(request)
        chart_config = self.chart_config(source.compute())
        script = """
        <script>
            $(document).ready(function () { 
                var ctx = document.getElementById("%s");
                var chart = echarts.init(ctx);
                chart.setOption(%s);
                $(window).on('resize', function(){
                    if(chart != null && chart != undefined){
                        chart.resize();
                    }
                });
            })
        </script>
        """ % (
            self.widget_id,
            json.dumps(chart_config),
        )
        return script

    def get_css_style(self):
        style = super().get_css_style() or ""
        if self.chart_height:
            style += "height:%spx;" % self.chart_height
        return style

    def chart_config(self, data):
        raise NotImplementedError()


class PieChart(EChart):
    def __init__(self, datasource, *, max_items=4, **kwargs):
        self.max_items = max_items
        super().__init__(datasource, **kwargs)

    def chart_config(self, data):
        labels = []
        chart_data = []
        max_items = self.max_items
        for idx, row in enumerate(sorted(data, key=lambda x: x[self.value_col])):

            if idx < max_items:
                chart_data.append(
                    {"name": row[self.label_col], "value": row[self.value_col]}
                )
            else:
                if "Others" not in labels:
                    labels.append("Others")
                if len(chart_data) <= max_items:
                    chart_data.append({"name": "Others", "value": 0})
                chart_data[-1]["value"] += row[self.value_col]

        return {"series": [{"type": "pie", "data": chart_data,}], "legend": {}}


class DoughnutChart(PieChart):
    def chart_config(self, data):
        result = super().chart_config(data)
        for s in result["series"]:
            s["radius"] = ["50%", "70%"]
        return result


class LineChart(EChart):

    default_opts = {"sm_size": 12, "md_size": 12, "lg_size": 12, "chart_height": 300}

    def __init__(self, datasource, *, series_col=None, default_label="Count", **kwargs):
        self.series_col = series_col
        self.default_label = default_label
        super().__init__(datasource, **kwargs)

    def chart_config(self, data):
        series_data = {}
        labels = []
        for row in data:
            if row["label"] not in labels:
                labels.append(row[self.label_col])
            if self.series_col:
                series_key = row[self.series_col]
            else:
                series_key = None
            series_data.setdefault(series_key, [])
            series_data[series_key].append(row[self.value_col])

        datasets = []
        for idx, r in sorted(enumerate(series_data.items()), key=lambda x: x[1][0]):
            ds = {}
            k, v = r
            cidx = idx % len(default_color_stack)
            default_color = default_color_stack[cidx]
            if k:
                ds["name"] = k
            else:
                ds["name"] = self.default_label
            ds["type"] = "line"
            ds["data"] = v
            datasets.append(ds)
        return {
            "xAxis": {"type": "category", "boundaryGap": False, "data": labels},
            "yAxis": {"type": "value"},
            "series": datasets,
            "legend": {},
        }


class HorizontalBar(LineChart):

    default_opts = {"sm_size": 12, "md_size": 6, "lg_size": 6, "chart_height": 300}

    def chart_config(self, data):
        conf = super().chart_config(data)
        for s in conf["series"]:
            s["type"] = "bar"
        return {
            "xAxis": {"type": "value"},
            "yAxis": {"type": "category", "data": conf["xAxis"]["data"]},
            "series": conf["series"],
            "legend": {},
            "grid": {
                "left": "10%",
                "right": "4%",
                "bottom": "3%",
                "containLabel": True,
            },
        }

