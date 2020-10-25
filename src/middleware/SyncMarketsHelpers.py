#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# HELPERS MARKETS
######################################################################################################
# Description : Middleware pour synchro des Marchés
# Auteur : ileouleyuki
######################################################################################################
import sys
import os
import inspect
# Ajout du repertoire au system pour facilter les import des modules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)
sys.path.append(os.path.dirname(__file__))


from lib.xtb import XtbClient    # NOQA # isort:skip
from models.MarketsModel import MarketsModel   # NOQA # isort:skip
from lib.configuration import Configuration  # NOQA # isort:skip

######################################################################################################
# Class SyncMarketsHelpers
######################################################################################################


class SyncMarketsHelpers(object):

    # ------------------------------------------------------------------------------------------------
    def __init__(self, account='DEMO'):
        """
        Initialisation de l'objet
        """
        # Enregistrement des variables utiles
        self._type = 'DEMO' if Configuration.from_filepath().get_use_demo_account() is True else 'REEL'
        self._accId = Configuration.from_filepath().get_credentials()[self._type.lower()]['account_id']
        self._mdp = Configuration.from_filepath().get_credentials()[self._type.lower()]['password']
        # Initialisation des variables necessaires
        self._broker = None
        self._mdl = None
        self._markets = None
        pass

    # ------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connxexion au Broker
        """
        # Initialisation Broker
        self._broker = XtbClient(
            account_id=self._accId,
            password=self._mdp,
            type=self._type
        )
        # Ouverture Connexion
        self._broker.login()
        pass

    # ------------------------------------------------------------------------------------------------

    def getMarkets(self):
        """
        Obtenir les Ordres
        """
        self._markets = self._broker.get_all_markets().to_dict("Records")
    # ------------------------------------------------------------------------------------------------

    def updateBdd(self):
        """
        Mise à jour de la BDD
        """
        # Initialisation du modele
        self._mdl = MarketsModel()
        for row in self._markets:
            self._mdl.upsert(record=row)
        pass

    # ------------------------------------------------------------------------------------------------
    def disconnect(self):
        """
        Deconnexion au broker
        """
        pass


######################################################################################################
# TEST
######################################################################################################
if __name__ == "__main__":
    print("DEBUT")
    testObj = SyncMarketsHelpers()
    testObj.connect()
    testObj.getMarkets()
    testObj.updateBdd()
    testObj.disconnect()
    print("FIN")
