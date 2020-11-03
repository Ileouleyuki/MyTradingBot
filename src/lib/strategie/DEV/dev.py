#!/usr/bin/env python
# encoding: utf-8
from ..interface import StrategieInterface
from lib.ohlc import OhlcGraph


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
        super().__init__(name="DEV")

    def plot(self):
        """
        ====================================================================
        Creation du Graphique pour la Strategie
        ====================================================================
        """
        objGraph = OhlcGraph(prices=self.prices.tail(300))
        objGraph.ohlc(height=600)
        # objGraph.addSignals()
        # objGraph.addVolume(height=100)
        # Ajout Indicateurs
        # objGraph.addBBANDS()
        # objGraph.addRSI(self._RSI_LIMIT_OVER_SELL,  self._RSI_LIMIT_OVER_BUY, height=200)
        return objGraph
