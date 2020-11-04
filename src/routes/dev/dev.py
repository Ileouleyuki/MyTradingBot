#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# DEV
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


from models.OrdersModel import OrdersModel
from lib.strategie.factory import StgyFactory

from bokeh.embed import components
from bokeh.resources import INLINE

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

######################################################################################################
# INITIALISATION
######################################################################################################
dev_bp = Blueprint('dev', __name__, template_folder="templates")

######################################################################################################
# ROUTES
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /dev
# Page de Dev
# ----------------------------------------------------------------------------------------------------


@dev_bp.route('/dev')
@login_required
def dev():
    # Recuperation des ressources statiques Bokeh
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    # Creation de la Strategie
    stgyObj = StgyFactory("DEV").make()
    # Recuperation des prix
    stgyObj.run(symbol='EURUSD', ut='H1')
    # Recuperation des Ordres
    df_orders = OrdersModel().getOrdersBySymbol(symbol='EURUSD')

    # Construction du Graphique avec Ordres
    graph = stgyObj.plot()
    graph.addOrders(df_orders)
    script, div = components(graph.save())
    # Preparation des données de la page
    data = {
        # Graphique
        'plot_div': div,
        'plot_script': script,
        'js_resources': js_resources,
        'css_resources': css_resources
    }
    return Render.htmlTemplate('dev/dev.html', data=data)
