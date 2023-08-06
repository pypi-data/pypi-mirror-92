from qm_spider import *
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Page, Pie, Timeline, Boxplot
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

class Line_Py:
    def __init__(self):
        pass


class Bar_Py:
    def __init__(self, title, x_value, y_name, y_value, *args, subtitle=''):
        self.x_value = x_value
        self.y_name = y_name
        self.y_value = y_value
        self.title = title
        self.subtitle = subtitle
        self.args = args

    def one_bar_air(self):
        c = (
            Bar()
                .add_xaxis(self.x_value)
                .add_yaxis(self.y_name, self.y_value)
                .add_yaxis(self.args[0], self.args[1])
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                    title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            )
        )
        return c