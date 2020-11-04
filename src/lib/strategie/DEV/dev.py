#!/usr/bin/env python
# encoding: utf-8
import pandas as pd
import numpy as np
from lib.strategie.interface import StrategieInterface
from lib.ohlc import OhlcGraph
from lib.configuration import Configuration
from lib.indic.indic import IF


class StrategieDev(StrategieInterface):
    """
    Classe definissant une Strategie pour le Developpement
    """

    def __init__(self):
        """
        ====================================================================
        Initialisation Objet
        ====================================================================
        """
        # Constructeur du Model
        self._name = "DEV"
        super().__init__(name=self._name)
        # BBANDS
        self._BB_PERIOD = Configuration.from_filepath().get_param_strategy(self._name)["bb_period"]
        self._BB_DEVIATION = Configuration.from_filepath().get_param_strategy(self._name)["bb_deviation"]
        # RSI
        self._RSI_PERIOD = Configuration.from_filepath().get_param_strategy(self._name)["rsi_period"]
        self._RSI_LIMIT_OVER_BUY = Configuration.from_filepath().get_param_strategy(self._name)["rsi_limit_over_buy"]
        self._RSI_LIMIT_OVER_SELL = Configuration.from_filepath().get_param_strategy(self._name)["rsi_limit_over_sell"]

    def calc(self):
        """
        ====================================================================
        Calcul des Indicateurs
        ====================================================================
        """
        RSI = IF.RSI(self.prices, period=self._RSI_PERIOD)
        BBANDS = IF.BBANDS(self.prices, period=self._BB_PERIOD, std_multiplier=self._BB_DEVIATION)
        BBWIDTH = IF.BBWIDTH(self.prices, period=self._BB_PERIOD, std_multiplier=self._BB_DEVIATION)
        self.prices = pd.concat([self.prices, BBANDS, BBWIDTH, RSI], axis=1)

    def setTrend(self):
        """
        ====================================================================
        Determination de la tendance des Prix pour la Strategie
        ====================================================================
        """
        pass

    def find(self):
        """
        ====================================================================
        Recherche des Signaux de Trading
        ====================================================================
        """
        # Initialisation de la colonne
        self.prices['signal'] = 0
        # -------------------------------------------------------------------
        # ACHAT
        # -------------------------------------------------------------------
        self.prices['signal'] = np.where(
            (
                # Le RSI est au-dessus de limite de SURVENTE
                (self.prices["RSI"] > self._RSI_LIMIT_OVER_SELL)
                # Le prix evolue en dessous de la Bande de Bollinger Basse
                & (self.prices["close"] < self.prices["BB_LOWER"])

            ), 1, self.prices["signal"]  # Si OUI : On met un sinon on reprend la valeur de la colonne 'Signal'
        )

        # -------------------------------------------------------------------
        # VENTE
        # -------------------------------------------------------------------
        self.prices['signal'] = np.where(
            (
                # Le RSI est au-dessus de limite de SURACHAT
                (self.prices["RSI"] > self._RSI_LIMIT_OVER_BUY)
                # Le prix evolue au dessus de la Bande de Bollinger Haute
                & (self.prices["close"] > self.prices["BB_HIGHER"])

            ), -1, self.prices["signal"]  # Si OUI : On met un sinon on reprend la valeur de la colonne 'Signal'
        )

    def pos(self):
        """
        ====================================================================
        Calculer les niveaux d'arrêt et de limite
        ====================================================================
        """
        self.prices['sl'] = 0
        self.prices['tp'] = 0

    def plot(self):
        """
        ====================================================================
        Creation du Graphique pour la Strategie
        ====================================================================
        """
        objGraph = OhlcGraph(prices=self.prices)
        objGraph.ohlc(height=500)
        objGraph.addSignals()
        objGraph.addVolume(height=100)
        # Ajout Indicateurs
        objGraph.addBBANDS()
        objGraph.addRSI(self._RSI_LIMIT_OVER_SELL,  self._RSI_LIMIT_OVER_BUY, height=150)
        return objGraph
