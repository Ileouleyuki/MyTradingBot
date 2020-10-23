#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> MARKETS
######################################################################################################
# Description : Routes pour les urls API lié au Marchés frontend
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import logging
# Flask
from flask import Blueprint, request, abort
# Perso
from core.Config import cfg
# from core.Exceptions import AppException
from core.Render import Render
from core.Decorateur import csrf_protect, login_required
from models.MarketsModel import MarketsModel

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
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Marchés', categorie="SUCCESS", data=data.to_dict("Record"))
    else:
        abort(400)
