#!/usr/bin/env python
# encoding: utf-8
# https://github.com/bokeh/bokeh/blob/branch-2.3/examples/app/ohlc/main.py
import os
import datetime
from math import pi
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Span
from bokeh.models import (DatetimeTickFormatter)
from bokeh.models import BoxAnnotation, Range1d
from bokeh.models.formatters import PrintfTickFormatter


class Graphique:

    def __init__(self, prices):
        """
        Initialisation Objet
        """
        # Copie des données
        self.data = prices.copy(deep=True)
        # Variables du Graphiques
        self.tools = "xpan,xwheel_zoom,ywheel_zoom, box_zoom,reset,save"
        self._plots = []
        # Parametrage Generaux
        self.format_date = '%a %d %b %Y\n%H:%M'
        self.path_graph = (
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) +
            os.sep + "tmp" + os.sep +
            datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "-graph.png"
        )

        self.INCREASING_COLOR = '#009900'
        self.DECREASING_COLOR = '#990000'
        self.BUY_SIG_COLOR = '#33FF33'
        self.SELL_SIG_COLOR = '#FF3333'
        self.DATE_FMT = '%d %b %Y'
        self.DATETIME_FMT = '%a %d %b %Y, %H:%M:%S'

    @property
    def path(self, column: str = None):
        return self.path_graph

    def save(self):
        """
        Sauvegarde du grahique
        """
        fig = gridplot(
            self._plots,
            ncols=1,
            toolbar_options=dict(logo=None),
            sizing_mode='stretch_width',
            toolbar_location='above',
            merge_tools=True,
        )
        return fig

    def ohlc(self, height=250):
        """
        Creation du graphique Candlestick OHLC
        """
        # Formatage des Dates
        self._xaxis_dt_format = self.DATE_FMT
        if self.data.index[0].hour > 0:
            self._xaxis_dt_format = self.DATETIME_FMT

        # Initialisation de la Figure
        self._fig_ohlc = figure(
            plot_height=height,
            x_axis_type="datetime",
            tools=self.tools,
            sizing_mode='stretch_both',
            active_drag='xpan',
            active_scroll='ywheel_zoom',
            toolbar_location="above",
            title=None)
        self._fig_ohlc.xaxis.major_label_orientation = pi/4
        self._fig_ohlc.grid.grid_line_alpha = 0.8
        self._fig_ohlc.yaxis.visible = True
        self._fig_ohlc.xaxis.visible = False

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

        w = 24 * 60 * 60  # day in seconds

        # HIGH et LOW
        self._fig_ohlc.segment(
            self.data.index,
            self.data.high,
            self.data.index,
            self.data.low,
            color="black",
            legend_label="OHLC"
        )

        # OPEN et Close
        r1 = self._fig_ohlc.vbar(
            x='x1',
            width=w,
            top='top1',
            bottom='bottom1',
            source=inc_source,
            fill_color=self.INCREASING_COLOR,
            line_color="black"
        )
        r2 = self._fig_ohlc.vbar(
            x='x2',
            width=w,
            top='top2',
            bottom='bottom2',
            source=dec_source,
            fill_color=self.DECREASING_COLOR,
            line_color="black"
        )

        # Formatage des Tick X
        self._fig_ohlc.yaxis.formatter = NumeralTickFormatter(format="€ 5.6f")
        # p.yaxis.formatter = NumeralTickFormatter(format='$ 0,0[.]000')
        self._fig_ohlc.xaxis.major_label_overrides = {
            i: date.strftime(self._xaxis_dt_format) for i, date in enumerate(self.data.index)
        }
        # Ajout des ToolTip sur les Bougies
        self._fig_ohlc.add_tools(HoverTool(
            renderers=[r1],
            tooltips=[
                ('open',  '@top1{%0.5f}'),
                ('high',  '@high1{%0.5f}'),
                ('low',  '@low1{%0.5f}'),
                ('close',  '@bottom1{%0.5f}'),
                ("datetime", "@Date1{" + self._xaxis_dt_format + "}"),
            ],
            formatters={
                '@Date1': 'datetime',
                '@top1': 'printf',   # use 'printf' formatter for 'adj close' field
                '@high1': 'printf',   # use 'printf' formatter for 'adj close' field
                '@low1': 'printf',   # use 'printf' formatter for 'adj close' field
                '@bottom1': 'printf',   # use 'printf' formatter for 'adj close' field

            },
            mode='vline'
            )
        )
        self._fig_ohlc.add_tools(HoverTool(
            renderers=[r2],
            tooltips=[
                ('open',  '@top2{%0.5f}'),
                ('high',  '@high2{%0.5f}'),
                ('low',  '@low2{%0.5f}'),
                ('close',  '@bottom2{%0.5f}'),
                ("datetime", "@Date2{" + self._xaxis_dt_format + "}"),
            ],
            formatters={
                '@Date2': 'datetime',
                '@top2': 'printf',   # use 'printf' formatter for 'adj close' field
                '@high2': 'printf',   # use 'printf' formatter for 'adj close' field
                '@low2': 'printf',   # use 'printf' formatter for 'adj close' field
                '@bottom2': 'printf',   # use 'printf' formatter for 'adj close' field

            },
            mode='vline'
            )
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
        self._fig_ohlc.legend.location = "top_left"

        self._fig_ohlc.x_range.follow = "end"
        # self._fig_ohlc.x_range.follow_interval = 100
        # self._fig_ohlc.x_range.range_padding = 0

        # Ajout du Graphique OHLC
        self._plots.append(self._fig_ohlc)

    def addVolume(self, height=50):
        """
        Ajout Du Volume
        """
        # Ajout du Panel
        self._fig_vol = figure(
            plot_height=height,
            x_range=self._fig_ohlc.x_range,
            x_axis_type=None,
            tools=self.tools,
            # sizing_mode='stretch_both',
            # active_drag='xpan',
            active_scroll='xwheel_zoom',
            toolbar_location="above",
            title=None
        )
        # Ajout des bars de Volmue
        self._fig_vol.vbar(x=self.data.index, top=self.data['volume'], width=0.9, color="#000000")
        self._fig_vol.yaxis.formatter = NumeralTickFormatter(format="0 a")
        # Ajout du label
        self._fig_vol.yaxis.axis_label = "VOLUME"

        # Ajout du Graphique VOLUME
        self._plots.append(self._fig_vol)

    def addSignals(self):
        """
        Ajout des Signaux de Trading
        """
        # Verification si presnece de la colonne signal
        if 'signal' not in self.data.columns.values:
            return
        # Add on a vertical line to indicate a trading signal here
        # vline = Span(location=df, dimension='height',line_color="green", line_width=2)
        # fig.renderers.extend([vline])
        # Set up the hover tooltip to display some useful data
        # Signaux ACHAT
        buy = self.data[self.data['signal'] > 0]
        self._fig_ohlc.scatter(
            buy.index,
            buy.low - (buy.low * 0.001),
            fill_color=self.BUY_SIG_COLOR,
            marker='triangle',
            line_color='black',
            size=10,
            legend_label="ACHAT"
        )
        # Signaux VENTE
        sell = self.data[self.data['signal'] < 0]
        self._fig_ohlc.scatter(
            sell.index,
            sell.high + (sell.high * 0.001),
            fill_color=self.SELL_SIG_COLOR,
            marker='inverted_triangle',
            line_color='black',
            size=10,
            legend_label="VENTE")

    def addSessions(self):
        """
        Ajout des Session de Trading
        """
        # Verification si presnece de la colonne sessions
        if 'session' not in self.data.columns.values:
            return

        # Ajout Indicateur OUVERTURE de Session
        OpenSession = self.data[
            (self.data['session'] == True)  # NOQA # isort:skip
            &
            (self.data['session'].diff() == True)
        ]
        for index, session in OpenSession.iterrows():
            openMarker = Span(
                location=index,
                dimension='height',
                line_color='green',
                line_dash='dashed',
                line_width=1
            )
            self._fig_ohlc.add_layout(openMarker)

        # Ajout Indicateur FERMETURE de Session
        CloseSession = self.data[
            (self.data['session'] == False)  # NOQA # isort:skip
            &
            (self.data['session'].diff() == True)
        ]
        for index, session in CloseSession.iterrows():
            closeMarker = Span(
                location=index,
                dimension='height',
                line_color='red',
                line_dash='dashed',
                line_width=1
            )
            self._fig_ohlc.add_layout(closeMarker)

    def addColorArea(self, col1, col2, color='blue'):
        """
        Coloration entre 2 Lignes
        """
        # Coloration entre ligne de prix et MM
        """
        inc_trend = self.data[self.data[col1] > self.data[col2]]
        dec_trend = self.data[self.data[col1] < self.data[col2]]
        self._fig_ohlc.varea(x=inc_trend.index, y1=inc_trend[col1], y2=inc_trend[col2], alpha=0.4, fill_color="green")
        self._fig_ohlc.varea(x=dec_trend.index, y1=dec_trend[col1], y2=dec_trend[col2], alpha=0.4, fill_color="red")
        """
        self._fig_ohlc.varea(x=self.data.index, y1=self.data[col1], y2=self.data[col2], alpha=0.4, fill_color=color)

    def ohlc_add_line(self, col, width=6, color="#f46d43", type="dashed"):
        """
        Ajout d'une ligne sur le graphique ohlc
        'solid','dashed','dotted','dotdash','dashdot'
        """
        self._fig_ohlc.line(
            x=self.data.index,
            y=self.data[col],
            line_color=color,
            line_width=width,
            line_alpha=0.6,
            legend_label=col,
            line_dash=type
        )

    def addToolTips(self):
        pass

    def addTrades(self, trades):
        """
        Ajout des Ordres sur le graphique
        """
        for index, row in trades.iterrows():
            # Zone du Trade ACHAT
            if row["direction"] == 1:
                self._fig_ohlc.quad(
                    top=row['tp'],
                    bottom=row['sl'],
                    left=row['enter_date'],
                    right=row['exit_date'],
                    color="#CCFF99" if row["tp_triggered"] is True else "#FF9999",
                    fill_alpha=0.6
                )
            if row["direction"] == -1:
                self._fig_ohlc.quad(
                    top=row['sl'],
                    bottom=row['tp'],
                    left=row['enter_date'],
                    right=row['exit_date'],
                    color="#CCFF99" if row["tp_triggered"] is True else "#FF9999",
                    fill_alpha=0.6
                )

            # SL
            self._fig_ohlc.quad(
                top=row['sl'],
                bottom=row['sl'],
                left=row['enter_date'],
                right=row['exit_date'],
                color="red",
                line_alpha=5,
                fill_alpha=0.6,
                line_dash="dotted"
            )
            # TP
            self._fig_ohlc.quad(
                top=row['tp'],
                bottom=row['tp'],
                left=row['enter_date'],
                line_alpha=5,
                right=row['exit_date'],
                color="darkgreen",
                fill_alpha=0.6,
                line_dash="dotted"
            )
            # ENTER
            self._fig_ohlc.quad(
                top=row['enter_price'],
                bottom=row['enter_price'],
                left=row['enter_date'],
                right=row['exit_date'],
                color="#000000",
                fill_alpha=0.6,
                line_dash="dotted"
            )

    def addRSI(self, limit_sell, limit_buy, height=10):
        """
        Ajout du RSI
        """
        # Creation du Panel
        self._fig_rsi = figure(
            plot_height=height,
            x_range=self._fig_ohlc.x_range,
            x_axis_type=None,
            tools=self.tools,
            # sizing_mode='stretch_both',
            # active_drag='xpan',
            active_scroll='xwheel_zoom',
            toolbar_location="above",
            title=None
        )

        # Ajout du RSI
        if 'RSI' in self.data.columns.values:
            self._fig_rsi.line(
                x=self.data.index,
                y=self.data['RSI'],
                line_color='black',
                line_width=1,
                line_alpha=0.6,
                # legend_label='RSI',
                line_dash='solid'
            )

        low_box = BoxAnnotation(top=limit_sell, fill_alpha=0.1, fill_color="red")
        self._fig_rsi.add_layout(low_box)
        high_box = BoxAnnotation(bottom=limit_buy, fill_alpha=0.1, fill_color="green")
        self._fig_rsi.add_layout(high_box)

        # Horizontal line
        hline = Span(location=50, dimension='width', line_color='black', line_width=0.5)
        self._fig_rsi.renderers.extend([hline])

        self._fig_rsi.y_range = Range1d(0, 100)
        self._fig_rsi.yaxis.ticker = [limit_sell, 50, limit_buy]
        self._fig_rsi.yaxis.formatter = PrintfTickFormatter(format="%f%%")
        self._fig_rsi.grid.grid_line_alpha = 0.3

        # Zone de Surachat
        # surachat_zone = self.data[self.data['RSI'] > limit_buy]
        # self._fig_rsi.varea(x=surachat_zone.index, y1=surachat_zone['RSI'], y2=limit_buy, alpha=0.4, fill_color="green")

        # Zone de SurVente
        # survente_zone = self.data[self.data['RSI'] < limit_sell]
        # self._fig_rsi.varea(x=survente_zone.index, y1=survente_zone['RSI'], y2=limit_sell, alpha=0.4, fill_color="red")

        # Ajout du label
        self._fig_rsi.yaxis.axis_label = "RSI"

        # Ajout du Graphique RSI
        self._plots.append(self._fig_rsi)

    def addBBANDS(self):
        """
        Ajout des Bandes de Bollinger
        """
        # Ajout de la Bandes HIGH
        if 'BB_HIGHER' in self.data.columns.values:
            self.ohlc_add_line(
                'BB_HIGHER', width=1, color="#CC6600", type="solid"
            )
        # Ajout de la Bandes MIDDLE
        if 'BB_MIDDLE' in self.data.columns.values:
            self.ohlc_add_line(
                'BB_MIDDLE', width=1, color="#CC6600", type="dashed"
            )

        # Ajout de la Bandes LOW
        if 'BB_LOWER' in self.data.columns.values:
            self.ohlc_add_line(
                'BB_LOWER', width=1, color="#CC6600", type="solid"
            )

        # Coloration entre lignes UP et LOW
        if 'BB_HIGHER' in self.data.columns.values and 'BB_LOWER' in self.data.columns.values:
            self.addColorArea('BB_HIGHER', 'BB_LOWER', color='#FFB266')
            # Band(base='date', lower='bolling_lower', upper='bolling_upper', source=stock, level='underlay',
            #    fill_alpha=0.5, line_width=1, line_color='black', fill_color=BLUE_LIGHT)

    def addICHIMOKU(self):
        """
        Ajout des Bandes de Bollinger
        """
        # Ajout de la TENKAN
        if 'TENKAN' in self.data.columns.values:
            self.ohlc_add_line(
                'TENKAN', width=2, color="#CC6600", type="solid"
            )
        # Ajout de la KIJUN
        if 'KIJUN' in self.data.columns.values:
            self.ohlc_add_line(
                'KIJUN', width=2, color="#00CC00", type="solid"
            )
        # Ajout de la SSA
        if 'SSA' in self.data.columns.values:
            self.ohlc_add_line(
                'SSA', width=1, color="#999900", type="dashed"
            )
        # Ajout de la SSB
        if 'SSB' in self.data.columns.values:
            self.ohlc_add_line(
                'SSB', width=1, color="#0066CC", type="dashed"
            )
        # Ajout de la CHIKOU
        if 'CHIKOU' in self.data.columns.values:
            self.ohlc_add_line(
                'CHIKOU', width=2, color="#000099", type="solid"
            )
        # Ajout Coloration Nuage
        self.addColorArea('SSA', 'SSB', color='#FFB266')
