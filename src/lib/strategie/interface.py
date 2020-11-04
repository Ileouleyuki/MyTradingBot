#!/usr/bin/env python
# encoding: utf-8
import os
import datetime
import pandas as pd
from pandas import DataFrame
from lib.configuration import Configuration
from lib.xtb import XtbClient
from lib.exceptions import UnreachableException


class StrategieInterface:
    """
    Interface pour les Strategies implementant les methodes
    communes à toutes
    """

    def __init__(self, name="NOM"):
        """
        Initialisation Objet
        """
        # Recuperation de la Configuration
        self.config = Configuration.from_filepath()
        # Definition des Parametres
        self.name = name
        self.__prices = None

    @property
    def prices(self):
        """Retourne le DataFame de Prix"""
        return self.__prices

    @prices.setter
    def prices(self, value: str):
        """Definition du dataframe des Prix"""
        if value is not None and isinstance(value, DataFrame):
            self.__prices = value
        else:
            self.__prices = None

    def reset(self):
        """RAZ de l'analyse"""
        self.__prices = None

    def run(self, symbol, ut):
        """
        Lancement de l'analyse
        """
        # Recuperation des Prix
        self.fetch_data_prices(symbol=symbol, ut=ut)
        # Calcul des Indicateurs
        self.calc()
        # Definition de la Tendance
        self.setTrend()
        # Recherche de Signaux
        self.find()
        # Calcul des Positions
        self.pos()

    def fetch_data_prices(self, symbol, ut):
        """
        Fonction permettant de recuperer les prix d'un marché et de les
        mettre à jour en local si besoin
        """
        # Determination du path du fichier en local
        data_full_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "../..")
            ) + os.sep + "data" + os.sep + "{}-{}.csv".format(
                symbol.upper(),
                ut.upper()
            )

        # Chargement du fichier en local si existant
        if os.path.exists(data_full_path):
            prices = pd.read_csv(data_full_path, sep=";", float_precision='round_trip')  # Ouverture du Fichier
            # prices['Datetime'] = pd.to_datetime(prices['Datetime'], utc=False)           # Formatage des Dates
            prices = prices.set_index(['Datetime'])                                      # Definition DatetimeIndex
        else:
            prices = pd.DataFrame(
                # index=pd.to_datetime([], utc=True),
                columns=['open', 'high', 'low', 'close', 'volume']
            )
            prices.index.name = 'Datetime'
            prices = prices.fillna(0)

        # Definition du Nombre de bougies
        # à recuperer chez le Broker en fonction du TimeFrame
        if ut in ['M1', 'M5']:
            days = 30
        elif ut in ['M15', 'H1']:
            days = 100
        else:
            days = 365
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(
            days=days
        )

        # Initialisation Broker
        self._type = 'DEMO' if self.config.get_use_demo_account() is True else 'REEL'
        self._accId = self.config.get_credentials()[self._type.lower()]['account_id']
        self._mdp = self.config.get_credentials()[self._type.lower()]['password']
        broker = XtbClient(
            account_id=self._accId,
            password=self._mdp,
            type=self._type
        )
        try:
            # Ouverture Connexion
            broker.login()
            # Recuperation des Prix chez le Broker
            update_prices = broker.get_prices(
                symbol=symbol,
                period=ut,
                start=start.timestamp(),
                end=end.timestamp(),
                ticks=0
            )
        except UnreachableException:
            pass
        else:
            # Concatenation des 2 dataframes
            updated_prices = pd.concat([update_prices, prices])
            # Suppression des duplicates
            updated_prices.drop_duplicates(keep='first', inplace=True)
            # Reordonnancement par l'index
            updated_prices.sort_index(inplace=True)
            # Mise à jour des prix
            prices = updated_prices.copy(deep=True)
            # prices.index = pd.to_datetime(prices.index, utc=True)
            # prices.index = prices.index.tz_convert(self.config.get_time_zone())
            del updated_prices
        # Enregistrement en local
        prices.to_csv(data_full_path, index=True, sep=";")
        # Mise en Forme des Dates
        prices.index = pd.to_datetime(prices.index / 1000, unit='s', utc=True)
        prices.index = prices.index.tz_convert(self.config.get_time_zone())

        # Enregistrement des Points
        self.__prices = prices
        del prices

    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
    def calc(self):
        raise NotImplementedError('Methode nom implémenté pour la class : calc')

    def setTrend(self):
        raise NotImplementedError("Methode nom implémenté pour la class : setTrend")

    def find(self):
        raise NotImplementedError("Methode nom implémenté pour la class : find")

    def plot(self):
        raise NotImplementedError("Methode nom implémenté pour la class : plot")

    def pos(self):
        raise NotImplementedError("Methode nom implémenté pour la class : positions")
