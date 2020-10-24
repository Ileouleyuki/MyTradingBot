#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> DASHBOARD
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
from core.Utils import Utils
from core.Exceptions import AppException
from core.Decorateur import csrf_protect, login_required
from models.OrdersModel import OrdersModel
from lib.dashboard import DashBoard


# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)


######################################################################################################
# INITIALISATION
######################################################################################################
api_dashboard_bp = Blueprint('api.dashboard', __name__)

_OPERATION = "DASHBOARD"

######################################################################################################
# URLS
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin pour recuperer le rapport du DashBoard
# Tous les Marchés
# ----------------------------------------------------------------------------------------------------


@api_dashboard_bp.route('/getReport', methods=['POST'])
@login_required
@csrf_protect
def getReport():
    """Parse un fichier de log dans un DataFrame"""
    if request.method == 'POST':
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        if 'period' not in data:
            raise AppException("Le parametre de Periode n'est pas disponible")
        if data['period'] not in ('DAILY', 'WEEKLY', 'MONTHLY', 'YEAR'):
            raise AppException("Le parametre de Periode n'est pas disponible")
        # Recuperation des Ordres
        orders = OrdersModel().getAll()
        # Init Dahboard
        dashObj = DashBoard(orders)
        dashObj.init(data['period'])

        # Creation du Dict de données du DashBoard
        ret = {}
        # HEADER
        ret['period_detail'] = dashObj.period()
        ret['period_start_fmt'] = dashObj.start()
        ret['period_end_fmt'] = dashObj.end()
        ret['capital_today'] = 0
        ret['gp_total'] = dashObj.gp_total()
        ret['gp_lose'] = dashObj.gp_lose()
        ret['gp_wins'] = dashObj.gp_wins()
        # ret['gp_ratio_lose'] = dashObj.gp_ratio_lose(orders)
        # ret['gp_ratio_wins'] = dashObj.gp_ratio_wins(orders)
        ret['trade_total'] = dashObj.trade_total()
        ret['trade_lose'] = dashObj.trade_lose()
        ret['trade_wins'] = dashObj.trade_wins()
        ret['trade_ratio_lose'] = dashObj.trade_ratio_lose()
        ret['trade_ratio_wins'] = dashObj.trade_ratio_wins()
        ret['evaluation'] = dashObj.evalu()
        # [GRAPH] - Performance des Trades
        ret['PerfTradeDataGraph'] = dashObj.getPerfTradeByDay()
        ret['PerfGpDataGraph'] = dashObj.getPerfGpByDay()
        # Recuperation des infos
        # data = OrdersModel().getAll()
        # Retour du message
        del dashObj
        return Render.jsonTemplate(_OPERATION, 'Données Dashboard', categorie="SUCCESS", data=ret, silent=True)
    else:
        abort(400)
