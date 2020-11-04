#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# BOT
######################################################################################################
# Description : Routes par default
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import logging
# Flask
from flask import Blueprint
# Perso
from core.Config import cfg
from core.Render import Render
from core.Decorateur import login_required

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

######################################################################################################
# INITIALISATION
######################################################################################################
bot_bp = Blueprint('bot', __name__, template_folder="templates")

######################################################################################################
# ROUTES
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /bot
# Page Activité du Bot
# ----------------------------------------------------------------------------------------------------


@bot_bp.route('/bot')
@login_required
def bot():
    return Render.htmlTemplate('bot/index.html')
