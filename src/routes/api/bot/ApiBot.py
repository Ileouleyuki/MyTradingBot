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

_OPERATION = "Gestion du BOT"
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
            "entries": entries.to_dict("records"),
            'state': BOT.active
        }
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Bot', categorie="SUCCESS", data=data)
    else:
        abort(400)

# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour renvoyer les infos des Logs d'activité
# Activité de l'application
# ----------------------------------------------------------------------------------------------------


@api_bot_bp.route('/getState', methods=['POST'])
@login_required
def getState():
    if request.method == 'POST':
        return Render.jsonTemplate(_OPERATION, 'Statut du Bot', categorie="SUCCESS", data=BOT.active, silent=True)
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
        if BOT.active is True:
            BOT.stop()
            return Render.jsonTemplate(_OPERATION, 'Arret du Bot', categorie="SUCCESS", data=BOT.active)
        elif BOT.active is False:
            BOT.start()
            return Render.jsonTemplate(_OPERATION, 'Demarrage du Bot', categorie="SUCCESS", data=BOT.active)
        else:
            return Render.jsonTemplate(_OPERATION, '????', categorie="ERROR", data=BOT.active)
    else:
        abort(400)
