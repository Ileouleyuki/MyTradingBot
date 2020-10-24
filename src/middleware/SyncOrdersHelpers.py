#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# HELPERS ORDERS
######################################################################################################
# Description : Middleware pour synchro des Ordres
# Auteur : ileouleyuki
######################################################################################################
import sys
import datetime
import os
import inspect
# Ajout du repertoire au system pour facilter les import des modules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)
sys.path.append(os.path.dirname(__file__))


from lib.xtb import XtbClient    # NOQA # isort:skip
from models.OrdersModel import OrdersModel   # NOQA # isort:skip


######################################################################################################
# Class SyncOrdersHelpers
######################################################################################################


class SyncOrdersHelpers(object):

    # ------------------------------------------------------------------------------------------------
    def __init__(self, account='DEMO'):
        """
        Initialisation de l'objet
        """
        # Enregistrement des variables utiles
        self._type = 'DEMO'
        self._accId = '11473046'
        self._mdp = 'Uvzdhwa4crxhud*'
        # Initialisation des variables necessaires
        self._broker = None
        self._mdl = None
        self._orders = None
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
    def getRange(self):
        """
        Determination de la fourchette de date
        """
        # Recuperation des ordres pour garde fou
        self._end = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        start = "{ANNEE}-{MOIS}-{DAY}".format(
            ANNEE=datetime.datetime.now().strftime("%Y"),
            MOIS=int(datetime.datetime.now().strftime("%m")),
            DAY=datetime.datetime.now().strftime("%d")
        )
        self._start = datetime.datetime.strptime(start, '%Y-%m-%d') - datetime.timedelta(days=130)

        pass

    # ------------------------------------------------------------------------------------------------
    def getOrders(self):
        """
        Obtenir les Ordres
        """
        self._orders = self._broker.getTradesHistory(
            start=self._start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp(),
            end=self._end.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        )

    # ------------------------------------------------------------------------------------------------
    def updateBdd(self):
        """
        Mise à jour de la BDD
        """
        # Initialisation du modele
        self._mdl = OrdersModel()
        for row in self._orders:
            self._mdl.upsert(record=row, account=self._accId, type=self._type)
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
    testObj = SyncOrdersHelpers()
    testObj.connect()
    testObj.getRange()
    testObj.getOrders()
    testObj.updateBdd()
    testObj.disconnect()
    print("FIN")
