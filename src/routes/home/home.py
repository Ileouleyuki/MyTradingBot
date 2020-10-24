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
import logging
import markdown.extensions.fenced_code
import markdown
# Flask
from flask import Blueprint, request, redirect, url_for
# Perso
from core.Config import cfg
from core.Render import Render
from core.Session import Session
from core.Auth import Auth
from core.Decorateur import login_required
# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

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
# Chemin GET pour atteindre /login quand on est connecte
# Page de Connexion
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Entrée dans les logs
        # Recuperation des Parametres Utilisateurs
        username = request.form['username']
        password = request.form['password']
        userIp = request.remote_addr
        # [ETAPE 1] - Verification si le user est bloqué par son IP
        if Auth.isIpBlocked(ip=userIp):
            return Render.htmlTemplate("login.html", data="Votre IP est bloqué")
        # [ETAPE 2] - Vérifier si l'utilisateur a précédemment échoué ses tentatives de connexion
        if Auth.getFailedLoginByUser(username=username):
            return Render.htmlTemplate("login.html", data="Vous avez dépassé le nombre de tentatives possibles, veuillez réessayer plus tard")
        # [ETAPE 3] - Obtenir l'utilisateur de la base de données
        if not Auth.checkUser(username=username, password=password, ip=userIp):
            return Render.htmlTemplate("login.html", data="Les Informations d'identification sont invalides. Veuillez réessayer.")
        else:
            # Redirection vers l'accueil
            print("Connexion reussi pour : {}".format(Session.getUserId()))
            return redirect(url_for('home.home'))
    else:
        return Render.htmlTemplate('login.html', data=error)

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /logout quand on est connecte
# Page de deconnexion
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/logout')
@login_required
def logout():
    # logger.info("Deconnexion pour : {}".format(Session.getUserId()))
    # Suppression de la Session Utilisateur
    Session.remove()

    # Redirection
    return redirect(url_for('home.index'))

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /home
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/home')
@login_required
def home():
    return Render.htmlTemplate('home/dashboard.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /home
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/test')
@login_required
def test():
    return Render.htmlTemplate('home/test.html')


# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /markets
# Page des Marchés
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/markets')
@login_required
def markets():
    return Render.htmlTemplate('home/markets.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /perf
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/perf')
@login_required
def perf():
    return Render.htmlTemplate('home/perf.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /orders
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/orders')
@login_required
def orders():
    return Render.htmlTemplate('home/orders.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /backtest
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/backtest')
@login_required
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
