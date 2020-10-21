#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# HOME
######################################################################################################
# Description : Routes par default
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import os
import markdown.extensions.fenced_code
import markdown
# Flask
from flask import Blueprint
# Perso
from core.Config import cfg
from core.Render import Render
from core.Logger import Logger

# Logger
logger = Logger()

######################################################################################################
# INITIALISATION
######################################################################################################
home_bp = Blueprint('home', __name__, template_folder="templates")

######################################################################################################
# ROUTES
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/')
@home_bp.route('/index')
def index():
    return Render.htmlTemplate('home/index.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /home
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/home')
def home():
    return Render.htmlTemplate('home/home.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /home
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/test')
def test():
    return Render.htmlTemplate('home/test.html')


# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /markets
# Page des Marchés
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/markets')
def markets():
    return Render.htmlTemplate('home/markets.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /perf
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/perf')
def perf():
    return Render.htmlTemplate('home/perf.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /orders
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/orders')
def orders():
    return Render.htmlTemplate('home/orders.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /backtest
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/backtest')
def backtest():
    return Render.htmlTemplate('home/backtest.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /changelog
# Page des Changements
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/changelog')
def changelog():
    # Ouverture du fichier
    readme_file = open(cfg._INIT_DIR + os.sep + "CHANGELOG.md", "r", encoding="UTF-8")
    # Conversion du Markdown
    md_template_string = markdown.markdown(readme_file.read(), extensions=["fenced_code"])
    # Affichage template
    return Render.htmlTemplate('home/changelog.html', data={"markdown": md_template_string})
