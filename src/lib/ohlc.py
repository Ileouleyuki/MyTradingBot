#!/usr/bin/env python
# encoding: utf-8
# https://github.com/bokeh/bokeh/blob/branch-2.3/examples/app/ohlc/main.py

from bokeh.models.sources import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import (DatetimeTickFormatter)
from math import pi
"""
import os
import datetime
from math import pi


from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Span
from bokeh.models import (DatetimeTickFormatter)
from bokeh.models import BoxAnnotation, Range1d
from bokeh.models.formatters import PrintfTickFormatter
"""
"""
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
"""


class OhlcGraph:
    """
    Classe permettant de créer le graphique OHLC
    """
    def __init__(self, prices):
        """
        ====================================================================
        Initialisation Objet
        ====================================================================
        """
        # Copie des données
        self.data = prices.copy(deep=True)
        # Variables du Graphiques
        self.tools = "xpan,xwheel_zoom,ywheel_zoom, box_zoom,reset,save"
        self._plots = []
        # Parametrage Generaux
        self.format_date = '%a %d %b %Y\n%H:%M'

        self.INCREASING_COLOR = '#009900'
        self.DECREASING_COLOR = 'red'
        self.DATE_FMT = '%d %b %Y'
        self.DATETIME_FMT = '%a %d %b %Y, %H:%M:%S'

    def save(self):
        """
        ====================================================================
        Implementation du Graphique
        ====================================================================
        """
        fig = gridplot(
            self._plots,
            ncols=1,
            toolbar_options=dict(logo=None),
            sizing_mode='stretch_width',
            toolbar_location='right',
            merge_tools=True,
        )
        return fig

    def styling(self, plot):
        """
        ====================================================================
        Implementation du Style
        ====================================================================
        """
        # Implementation du Style
        plot.background_fill_color = "#222222"
        plot.border_fill_color = "#222222"
        plot.outline_line_width = 7
        plot.outline_line_alpha = 0.3
        plot.outline_line_color = "#222222"
        # changer juste quelques choses sur la grille x
        plot.xgrid.grid_line_color = None
        plot.xgrid.grid_line_alpha = 0.5
        plot.xgrid.grid_line_dash = [6, 4]
        # changer juste certaines choses sur la grille en y
        plot.ygrid.grid_line_color = "#ffffff"
        plot.ygrid.grid_line_alpha = 0.5
        plot.ygrid.grid_line_dash = [6, 4]
        # changer juste certaines choses sur l'axe des x
        # fig.xaxis.axis_line_width = 3
        # fig.xaxis.axis_line_color = "red"

        # changer juste certaines choses sur l'axe y
        plot.yaxis.major_label_text_color = "#ffffff"
        # plot.yaxis.major_label_orientation = "vertical"

        # plot.x_range.follow = "end"
        # plot.x_range.follow_interval = 10
        return plot

    def ohlc(self, height=250):
        """
        ====================================================================
        Creation du graphique Candlestick OHLC
        ====================================================================
        """
        # Formatage des Dates
        self._xaxis_dt_format = self.DATE_FMT
        if self.data.index[0].hour > 0:
            self._xaxis_dt_format = self.DATETIME_FMT

        # Creation de la Figure
        self._fig_ohlc = figure(
            plot_height=height,
            toolbar_location="right",
            sizing_mode='stretch_both',
            x_axis_type="datetime",
            tools=self.tools,
            active_drag='xpan',
            active_scroll='ywheel_zoom'
        )
        self._fig_ohlc.xaxis.major_label_orientation = pi/4
        self._fig_ohlc.grid.grid_line_alpha = 0.8
        self._fig_ohlc.yaxis.visible = True
        self._fig_ohlc.xaxis.visible = False

        # Preparation des DataSource
        inc = self.data.close > self.data.open
        dec = self.data.open > self.data.close
        inc_source = ColumnDataSource(data=dict(
            x1=self.data.index[inc],
            top1=self.data.open[inc],
            bottom1=self.data.close[inc],
            high1=self.data.high[inc],
            low1=self.data.low[inc],
            Date1=self.data.index[inc]
        ))
        dec_source = ColumnDataSource(data=dict(
            x2=self.data.index[dec],
            top2=self.data.open[dec],
            bottom2=self.data.close[dec],
            high2=self.data.high[dec],
            low2=self.data.low[dec],
            Date2=self.data.index[dec]
        ))

        # Ajout des Graphique
        w = 24 * 60 * 60 * 10  # day in seconds * 10

        # HIGH et LOW
        self._fig_ohlc.segment(
            self.data.index,
            self.data.high,
            self.data.index,
            self.data.low,
            color="white",
            legend_label="OHLC"
        )

        # OPEN et CLOSE
        self._fig_ohlc.vbar(
            x='x1',
            width=w,
            top='top1',
            bottom='bottom1',
            source=inc_source,
            fill_color=self.INCREASING_COLOR,
            line_color=self.INCREASING_COLOR
        )
        self._fig_ohlc.vbar(
            x='x2',
            width=w,
            top='top2',
            bottom='bottom2',
            source=dec_source,
            fill_color=self.DECREASING_COLOR,
            line_color=self.DECREASING_COLOR
        )

        # Formatage de l'axe X (Temps)
        self._fig_ohlc.xaxis.visible = True
        self._fig_ohlc.xaxis.major_label_overrides = {
            i: date.strftime(self._xaxis_dt_format) for i, date in enumerate(self.data.index)
        }
        self._fig_ohlc.xaxis.formatter = DatetimeTickFormatter(
            hours=["%a %d %B %Y %H:%M"],
            days=["%a %d %B %Y %H:%M"],
            months=["%a %d %B %Y %H:%M"],
            years=["%a %d %B %Y %H:%M"],
        )
        self._fig_ohlc.xaxis.major_label_orientation = "horizontal"

        self._fig_ohlc.yaxis.axis_label = "OHLC"
        self._fig_ohlc.legend.visible = False
        self._fig_ohlc.legend.location = "top_left"

        self._fig_ohlc.x_range.follow = "end"

        # Application du Style
        self._fig_ohlc = self.styling(self._fig_ohlc)

        # Ajout du Graphique OHLC
        self._plots.append(self._fig_ohlc)
