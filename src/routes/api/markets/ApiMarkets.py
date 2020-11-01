#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> MARKETS
######################################################################################################
# Description : Routes pour les urls API lié au Marchés frontend
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import time
import logging
# Flask
from flask import Blueprint, request, abort, Response
# Perso
from core.Session import Session
from core.Config import cfg
# from core.Exceptions import AppException
from core.Render import Render
from core.Crypt import Crypt
from core.Utils import Utils
from core.Decorateur import csrf_protect, login_required
from models.MarketsModel import MarketsModel
from helpers.SyncMarketsHelpers import SyncMarketsHelpers

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)


######################################################################################################
# INITIALISATION
######################################################################################################
api_markets_bp = Blueprint('api.markets', __name__)

_OPERATION = "TEST"
######################################################################################################
# URLS
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin pour recuperer les Marchés
# Tous les Marchés
# ----------------------------------------------------------------------------------------------------


@api_markets_bp.route('/getAll', methods=['POST'])
@login_required
@csrf_protect
def getAll():
    """Parse un fichier de log dans un DataFrame"""
    if request.method == 'POST':
        # Recuperation des infos
        data = MarketsModel().getAll()
        # Cryptage des id
        data["id"] = data.apply(lambda x: Crypt.encode(cfg._APP_SECRET_KEY, x['id']), axis=1)
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Marchés', categorie="SUCCESS", data=data.to_dict("records"))
    else:
        abort(400)

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /markets/edit/{symbols}
# Page des Marchés
# ----------------------------------------------------------------------------------------------------


@api_markets_bp.route('/markets/edit', methods=['POST'])
@login_required
def getMarketById():
    if request.method == 'POST':
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        # Decryptage id
        idDecrypt = Crypt.decode(cfg._APP_SECRET_KEY, data["id"])
        # Recuperation des infos
        df = MarketsModel().getMarketById(idDecrypt)
        data = {}
        data["info"] = {}
        data["info"] = df.to_dict("Records")
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Marchés', categorie="SUCCESS", data=data)
    else:
        abort(400)

    return Render.htmlTemplate('home/marketEdit.html')
# ----------------------------------------------------------------------------------------------------
# Chemin pour Synchroniser les Marchés chez le Broker
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@api_markets_bp.route('/SyncMarkets', methods=['POST'])
@login_required
@csrf_protect
def SyncMarkets():
    def run(user):
        # Initialisation des Parametres + Variables
        _OPERATION = "Synchronisation des Marchés"
        logger.info("Lancement de la Synchronisation des Marchés par : {}".format(user))
        SyncMarketsHelpersObj = None
        try:
            # ========================================================================================
            yield Render.sseTemplate(perc=1, message="Demarrage de la synchronisation des Marchés", operation=_OPERATION, categorie="NORMAL")
            SyncMarketsHelpersObj = SyncMarketsHelpers()
            # Initialisation du Broker
            yield Render.sseTemplate(perc=25, message="Connexion au Broker", operation=_OPERATION, categorie="TITLE")
            SyncMarketsHelpersObj.connect()
            # Obtenir les Marchés
            yield Render.sseTemplate(perc=50, message="Recuperation des Marchés", operation=_OPERATION, categorie="TITLE")
            SyncMarketsHelpersObj.getMarkets()
            # Mise à jour dela BDD
            yield Render.sseTemplate(perc=75, message="Mise à jour de la BDD (Traitement Long)", operation=_OPERATION, categorie="TITLE")
            SyncMarketsHelpersObj.updateBdd()
            # Fin de Traitement
            SyncMarketsHelpersObj.disconnect()
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
