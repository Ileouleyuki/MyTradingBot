#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> BOT
######################################################################################################
# Description : Routes pour les urls API lié au Bot
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
from core.Utils import Utils
from core.Decorateur import csrf_protect, login_required, roles_accepted
from bot import Bot
# Models
from models.LogBotModel import LogBotModel

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

stop_run = False
BOT = Bot()
######################################################################################################
# INITIALISATION
######################################################################################################
api_bot_bp = Blueprint('api.bot', __name__)

_OPERATION = "BOT"
######################################################################################################
# ACTIVITY
######################################################################################################

# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour renvoyer les infos des Logs d'activité
# Activité de l'application
# ----------------------------------------------------------------------------------------------------


@api_bot_bp.route('/getActivityEntries', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def getActivityEntries():
    """Parse un fichier de log dans un DataFrame"""
    if request.method == 'POST':
        # Recuperation des infos
        entries = LogBotModel().getAll()
        data = {
            "entries": entries.to_dict("Record"),
            'state': BOT.state
        }
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Bot', categorie="SUCCESS", data=data)
    else:
        abort(400)

# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour renvoyer les infos des Logs d'activité
# Activité de l'application
# ----------------------------------------------------------------------------------------------------


@api_bot_bp.route('/run', methods=['POST'])
@login_required
def run():
    if request.method == 'POST':
        global stop_run
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        if data["toState"] == "1":
            BOT.start()
            # stop_run = False
            # manual_run()
            return Render.jsonTemplate(_OPERATION, 'RUN', categorie="SUCCESS")
        elif data["toState"] == "0":
            BOT.stop()
            return Render.jsonTemplate(_OPERATION, 'STOP', categorie="SUCCESS")
        else:
            return Render.jsonTemplate(_OPERATION, 'Impossible à determiner', categorie="ERROR")
        # Decryptage id
        # data["id"] = Crypt.decode(cfg._APP_SECRET_KEY, data["id"])
        # Recuperation des infos
        # MarketsModel().update(data)
        # Retour du message
    else:
        abort(400)
