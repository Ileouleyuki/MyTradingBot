#!/usr/bin/env python
# encoding: utf-8

from ..configuration import Configuration
# STRATEGIES
from .DEV.dev import StrategieDev


class StgyFactory:
    """
    Classe permttant d'initialiser les Strategies
    """

    def __init__(self, name=None):
        """
        Initialisation Objet
        """
        # Recuperation de la Configuration
        self.config = Configuration.from_filepath()
        # Validation de la strategie
        if name is None or name not in self.config.get_values_strategy():
            raise Exception("La Strategie {NOM} n'existe pas".format(NOM=name))
        # Enregistrement des Variables
        self.name = name

    def make(self):
        """
        Créez et renvoyez une instance de la classe Strategy telle que configurée dans le
        fichier de configuration
        """
        # Initialisation de la Strategie défini
        # >>> Strategie : DEV
        if self.name.strip() == "DEV":
            return StrategieDev()
        # >>> Strategie : INCONNU
        else:
            raise ValueError("Strategie non-prise en charge: {}".format(self.__config.get_trading_interface()))
