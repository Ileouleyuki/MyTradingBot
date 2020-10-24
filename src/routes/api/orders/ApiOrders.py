#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> ORDRES
######################################################################################################
# Description : Routes pour les urls API lié au Ordres frontend
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import time
import logging
# Flask
from flask import Blueprint, request, abort, Response
# Perso
from core.Config import cfg
# from core.Exceptions import AppException
from core.Session import Session
from core.Render import Render
from core.Decorateur import csrf_protect, login_required
from core.Utils import Utils
from models.OrdersModel import OrdersModel
from middleware.SyncOrdersHelpers import SyncOrdersHelpers
# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

######################################################################################################
# INITIALISATION
######################################################################################################
api_orders_bp = Blueprint('api.orders', __name__)

_OPERATION = "ORDRES"
######################################################################################################
# URLS
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin pour recuperer les Ordres en BDD
# Tous les Marchés
# ----------------------------------------------------------------------------------------------------


@api_orders_bp.route('/getOrders', methods=['POST'])
@login_required
@csrf_protect
def getAll():
    """Parse un fichier de log dans un DataFrame"""
    if request.method == 'POST':
        # Recuperation des infos
        data = OrdersModel().getAll()
        # Formatage des Delais
        data['delai'] = data['delai'].apply(Utils.formatSeconds)
        # df["id"] = df.apply(lambda x: Crypt.encode(cfg._APP_SECRET_KEY, x['id']), axis=1)
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Ordres', categorie="SUCCESS", data=data.to_dict("records"))
    else:
        abort(400)

# ----------------------------------------------------------------------------------------------------
# Chemin pour Synchroniser les Ordres chez le Broker
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@api_orders_bp.route('/SyncOrders', methods=['POST'])
@login_required
@csrf_protect
def SyncOrders():
    def run(user):
        # Initialisation des Parametres + Variables
        _OPERATION = "Synchronisation des Ordres"
        logger.info("Lancement de la Synchronisation des ordres par : {}".format(user))
        SyncOrdersHelpersObj = None
        try:
            # ========================================================================================
            yield Render.sseTemplate(perc=1, message="Demarrage de la synchronisation des Ordres", operation=_OPERATION, categorie="NORMAL")
            SyncOrdersHelpersObj = SyncOrdersHelpers()
            # Initialisation du Broker
            yield Render.sseTemplate(perc=25, message="Connexion au Broker", operation=_OPERATION, categorie="TITLE")
            SyncOrdersHelpersObj.connect()
            # Recuperation de la date du dernier Ordre
            yield Render.sseTemplate(perc=50, message="Determination de la Periode de Recuperation", operation=_OPERATION, categorie="TITLE")
            SyncOrdersHelpersObj.getRange()
            # Obtenir les Ordres
            yield Render.sseTemplate(perc=75, message="Recuperation des ordres", operation=_OPERATION, categorie="TITLE")
            SyncOrdersHelpersObj.getOrders()
            # Mise à jour dela BDD
            yield Render.sseTemplate(perc=85, message="Mise à jour de la BDD", operation=_OPERATION, categorie="TITLE")
            SyncOrdersHelpersObj.updateBdd()
            # Fin de Traitement
            SyncOrdersHelpersObj.disconnect()
            yield Render.sseTemplate(perc=100, message="Fin de Syncronisation des Ordres", operation=_OPERATION, categorie="SUCCESS")
        except Exception as error:
            logger.exception(error)
            yield Render.sseTemplate(perc=100, message=str(error), operation=_OPERATION, categorie="ERROR")
        finally:

            time.sleep(0.2)

    # return Render.jsonTemplate(_OPERATION, "ESSAI", categorie="WARNING", data=None)
    # raise Exception("NOOOOOOOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNN")
    # Session.setPid()

    return Response(run(user=Session.getUserDisplay()), mimetype='text/event-stream')
