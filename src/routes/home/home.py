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
import numpy as np
# Flask
from flask import Blueprint, request, redirect, url_for, jsonify
# Perso
from core.Config import cfg
from core.Render import Render
from core.Session import Session
from core.Auth import Auth
from core.Decorateur import login_required

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models.sources import AjaxDataSource, CustomJS
# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

x = list(np.arange(0, 6, 0.1))
y = list(np.sin(x) + np.random.random(len(x)))

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
# Chemin GET pour atteindre /markets/{SYMBOL}
# Page d'edition du Marché
# ----------------------------------------------------------------------------------------------------


@home_bp.route('/markets')
@login_required
def markets():
    return Render.htmlTemplate('home/markets.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /markets/{SYMBOL}
# Page d'edition du Marché
# ----------------------------------------------------------------------------------------------------


def make_ajax_plot():
    adapter = CustomJS(code="""
        const result = {x: [], y: []}
        const pts = cb_data.response.points
        for (let i=0; i<pts.length; i++) {
            result.x.push(pts[i][0])
            result.y.push(pts[i][1])
        }
        return result
    """)
    # Definition de la Source AJAX
    source = AjaxDataSource(
        data_url=request.url_root + 'data/',
        polling_interval=500,
        adapter=adapter
    )
    # Creation de la Figure
    plot = figure(
        plot_height=210,
        sizing_mode='scale_width',
        # title="Streaming Noisy sin(x) via Ajax"
    )
    # Ajout de la Ligne
    plot.line('x', 'y', source=source)
    # Styles
    plot.background_fill_color = "#222222"
    plot.border_fill_color = "#222222"
    plot.outline_line_width = 7
    plot.outline_line_alpha = 0.3
    plot.outline_line_color = "#222222"
    # change just some things about the x-grid
    plot.xgrid.grid_line_color = "#ffffff"
    plot.xgrid.grid_line_alpha = 0.5
    plot.xgrid.grid_line_dash = [6, 4]
    # change just some things about the y-grid
    plot.ygrid.grid_line_color = "#ffffff"
    plot.ygrid.grid_line_alpha = 0.5
    plot.ygrid.grid_line_dash = [6, 4]
    # change just some things about the x-axis
    plot.xaxis.axis_label = "Temp"
    # plot.xaxis.axis_line_width = 3
    # plot.xaxis.axis_line_color = "red"

    # change just some things about the y-axis
    plot.yaxis.axis_label = "Pressure"
    plot.yaxis.major_label_text_color = "#ffffff"
    # plot.yaxis.major_label_orientation = "vertical"

    # plot.background_fill_alpha = 0.5

    plot.x_range.follow = "end"
    plot.x_range.follow_interval = 10
    script, div = components(plot)
    return script, div


@home_bp.route('/data/', methods=['POST'])
@login_required
def data():
    x.append(x[-1]+0.1)
    y.append(np.sin(x[-1])+np.random.random())
    return jsonify(points=list(zip(x, y)))


@home_bp.route('/markets/edit/<idCrypt>/')
@login_required
def marketsEdit(idCrypt):
    # Recuperation des ressources statiques Bokeh
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    # Construction du graphique
    script, div = make_ajax_plot()

    # Preparation des données de la page
    data = {
        'id': idCrypt,
        # Graphique
        'plot_div': div,
        'plot_script': script,
        'js_resources': js_resources,
        'css_resources': css_resources
    }
    # Renvoi de la page
    return Render.htmlTemplate('home/marketEdit.html', data=data)


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
