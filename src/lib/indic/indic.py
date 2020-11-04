#!/usr/bin/env python
# encoding: utf-8
# https://github.com/peerchemist/finta/blob/master/finta/finta.py

import pandas as pd
import numpy as np
from pandas import DataFrame


class IF:

    __version__ = "1.0"

    @classmethod
    def SMA(cls, ohlc: DataFrame, period: int = 41, column: str = "close"):
        """
        Moyenne mobile simple - moyenne mobile dans le jargon des pandas. Aussi connu sous le nom de «MA».
        La moyenne mobile simple (SMA) est la plus élémentaire des moyennes mobiles utilisées pour le trading.
        """

        return pd.Series(
            ohlc[column]
            .rolling(window=period)
            .mean(),
            name="SMA{0}".format(period),
        )

    @classmethod
    def EMA(cls, ohlc: DataFrame, period: int = 9, column: str = "close"):
        """
        Moyenne mobile pondérée exponentielle - Comme tous les indicateurs de moyenne mobile, ils sont bien
        mieux adaptés aux marchés à tendance. Lorsque le marché est dans une tendance haussière forte et soutenue,
        la ligne d'indicateur EMA montrera également une tendance haussière et vice-versa pour une tendance baissière.
        Les EMA sont couramment utilisées en conjonction avec d'autres indicateurs pour confirmer les mouvements
        importants du marché et pour évaluer leur validité.
        """

        return pd.Series(
            ohlc[column]
            .ewm(span=period)
            .mean(),
            name="EMA{0}".format(period),
        )

    @classmethod
    def RSI(cls, ohlc: DataFrame, period: int = 14):
        """
        L'indice de force relative (RSI) est un oscillateur d'élan qui mesure la vitesse et le changement des mouvements de prix.
        Le RSI oscille entre zéro et 100. Traditionnellement, et selon Wilder, le RSI est considéré comme surachat lorsqu'il est supérieur
        à 70 et survendu lorsqu'il est inférieur à 30.
        Les signaux peuvent également être générés en recherchant des divergences, des oscillations d'échec et des croisements de ligne médiane.
        Le RSI peut également être utilisé pour identifier la tendance générale.
        """

        # get the price diff
        delta = ohlc["close"].diff()

        # positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # EMAs of ups and downs
        _gain = up.ewm(span=period).mean()
        _loss = down.abs().ewm(span=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")

    # ====================================================================================================================
    # BOLLINGER BANDS
    # ====================================================================================================================

    @classmethod
    def BBANDS(cls, ohlc: DataFrame, period: int = 20, MA=None, column: str = "close", std_multiplier: int = 2):
        """
        Développées par John Bollinger, les bandes de Bollinger® sont des bandes de volatilité placées au-dessus et au-dessous d'une moyenne mobile.
        La volatilité est basée sur l'écart type, qui change à mesure que la volatilité augmente et diminue.
        Les bandes s'élargissent automatiquement lorsque la volatilité augmente et se rétrécissent lorsque la volatilité diminue.
        Cette méthode permet la saisie d'une autre forme de moyenne mobile comme EMA ou KAMA autour de laquelle BBAND ​​sera formé.
        Passez la moyenne mobile souhaitée comme argument <MA>. Par exemple BBANDS (MA = TA.KAMA (20)).
         """

        std = ohlc[column].rolling(window=period).std()

        if not isinstance(MA, pd.core.series.Series):
            middle_band = pd.Series(cls.SMA(ohlc, period), name="BB_MIDDLE")
        else:
            middle_band = pd.Series(MA, name="BB_MIDDLE")

        upper_bb = pd.Series(middle_band + (std_multiplier * std), name="BB_HIGHER")
        lower_bb = pd.Series(middle_band - (std_multiplier * std), name="BB_LOWER")

        return pd.concat([upper_bb, middle_band, lower_bb], axis=1)

    @classmethod
    def BBWIDTH(cls, ohlc: DataFrame, period: int = 20, MA=None, column: str = "close", std_multiplier: int = 2):
        """
        La bande passante indique la largeur des bandes
        de Bollinger sur une base normalisée.
        """

        BB = IF.BBANDS(ohlc, period, MA, column, std_multiplier)

        return pd.Series(
            (BB["BB_HIGHER"] - BB["BB_LOWER"]) / BB["BB_MIDDLE"], name="BBWITH",
        )

    # ====================================================================================================================
    # ICHIMOKU
    # ====================================================================================================================

    @classmethod
    def ICHIMOKU(cls, ohlc: DataFrame, conversion_line_period=9, base_line_periods=26, laggin_span=52, displacement=26):
        # tenkan_window = 20
        # kijun_window = 60
        # senkou_span_b_window = 120
        # cloud_displacement = 30
        # chikou_shift = -30
        """
        # Dates are floats in mdates like 736740.0
        # the period is the difference of last two dates
        last_date = ohcl_df.index.iloc[-1]
        period = last_date - ohcl_dfindex.iloc[-2]

        # Add rows for N periods shift (cloud_displacement)
        ext_beginning = decimal.Decimal(last_date+period)
        ext_end = decimal.Decimal(last_date + ((period*cloud_displacement)+period))
        dates_ext = list(self.drange(ext_beginning, ext_end, str(period)))
        dates_ext_df = pd.DataFrame({"Datetime": dates_ext})
        dates_ext_df.index = dates_ext # also update the df index
        ohcl_df = ohcl_df.append(dates_ext_df)
        """
        # Tenkan
        tenkan_sen_high = ohlc['high'].rolling(window=conversion_line_period).max()
        tenkan_sen_low = ohlc['low'].rolling(window=conversion_line_period).min()
        tenkan_sen = pd.Series((tenkan_sen_high + tenkan_sen_low) / 2, name="TENKAN")

        # Kijun
        kijun_sen_high = ohlc['high'].rolling(window=base_line_periods).max()
        kijun_sen_low = ohlc['low'].rolling(window=base_line_periods).min()
        kijun_sen = pd.Series((kijun_sen_high + kijun_sen_low) / 2, name="KIJUN")

        # Senkou Span A
        leading_senkou_span_a = (tenkan_sen + kijun_sen) / 2
        senkou_span_a = pd.Series(leading_senkou_span_a.shift(displacement), name="SSA")

        # Senkou Span B
        leading_senkou_span_b = (ohlc['high'].rolling(window=laggin_span).max() + ohlc['low'].rolling(window=laggin_span).min()) / 2
        senkou_span_b = pd.Series(leading_senkou_span_b.shift(displacement), name="SSB")

        # Chikou
        chikou_span = pd.Series(ohlc['close'].shift(-displacement), name="CHIKOU")

        return pd.concat(
            [tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span], axis=1
        )

    # ====================================================================================================================
    # UTILITAIRES
    # ====================================================================================================================

    @classmethod
    def trending_up(cls, ohlc: DataFrame, col: str, period: int) -> pd.Series:
        """
        Renvoie une série booléenne si la série d'entrées a une tendance
        à la hausse sur les n dernières périodes.

        :param df: data
        :param period: range
        :return: result Series
        """
        return pd.Series(ohlc.diff(period) > 0, name="trending_up {}".format(period))

    @classmethod
    def trending_down(cls, ohlc: DataFrame, col: str, period: int) -> pd.Series:
        """
        Renvoie une série booléenne si la série d'entrée affiche une tendance
        à la hausse sur les n dernières périodes.

        :param df: DataFrame
        :param period: range
        :return: result Series
        """
        return pd.Series(ohlc[col].diff(period) < 0, name="trending_down {}".format(period))

    @classmethod
    def trend(cls, ohlc: DataFrame, col: str, period: int) -> pd.Series:
        """
        Renvoie une série booléenne si la série d'entrées a une tendance
        à la hausse sur les n dernières périodes.

        :param df: data
        :param period: range
        :return: result Series
        """

        # Determination des Tendances de Fonds
        # trend_up = cls.trending_up(ohlc, period)
        # trend_down = cls.trending_down(ohlc, period)

        decreasing = ohlc[col].diff(period) < 0
        increasing = ohlc[col].diff(period) > 0

        decreasing = decreasing.astype(int)
        increasing = increasing.astype(int)
        """
        # Offset
        if offset != 0:
            decreasing = decreasing.shift(offset)
            increasing = increasing.shift(offset)
        # Handle fills
        if 'fillna' in kwargs:
            decreasing.fillna(kwargs['fillna'], inplace=True)
            increasing.fillna(kwargs['fillna'], inplace=True)

        if 'fill_method' in kwargs:
            decreasing.fillna(method=kwargs['fill_method'], inplace=True)
            increasing.fillna(method=kwargs['fill_method'], inplace=True)
        """
        # Name and Categorize it
        decreasing.name = "DEC"
        decreasing.category = 'trend'
        increasing.name = "INC"
        increasing.category = 'trend'
        # Concatenation
        concat = decreasing.to_frame().join(increasing)
        # Creation Colonne Final
        concat["T_F"] = "N"
        concat["T_F"] = np.where(
            (
                (concat['DEC'] == 1)
            ), "B", concat["T_F"]  # Si OUI : On met un sinon on reprend la valeur de la colonne 'Signal'
        )
        concat["T_F"] = np.where(
            (
                (concat['INC'] == 1)
            ), "H", concat["T_F"]   # Si OUI : On met un sinon on reprend la valeur de la colonne 'Signal'
        )
        return concat["T_F"]

    @classmethod
    def cross(cls, series1: pd.Series, series2: pd.Series, above: bool = True) -> pd.Series:
        """
        Renvoie True si «series1» croise au dessus de «series2», si above est à True
        Renvoie True si «series1» croise au dessous de «series2», si above est à False
        """
        current = series1 > series2  # current is above
        previous = series1.shift(1) < series2.shift(1)     # previous is below
        # above if both are true, below if both are false
        cross = current & previous if above else ~current & ~previous
        # Nommage
        cross.name = f"{series1.name}_{'XA' if above else 'XB'}_{series2.name}"
        return cross
