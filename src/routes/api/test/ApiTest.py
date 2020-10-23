#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> TEST
######################################################################################################
# Description : Routes pour les urls API lié au test frontend
# Date de Creation : 06/05/2020
######################################################################################################

# Globales
import time
import logging
# Flask
from flask import Blueprint, Response
# Perso
from core.Config import cfg
# from core.Exceptions import AppException
from core.Render import Render
from core.Session import Session
from core.Decorateur import csrf_protect   # login_required


# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)


######################################################################################################
# INITIALISATION
######################################################################################################
api_test_bp = Blueprint('api.test', __name__)

_OPERATION = "TEST"
######################################################################################################
# TEST
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin pour test Erreur JSON
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@api_test_bp.route('/testJSON', methods=['POST'])
# @login_required
@csrf_protect
def testJSON():
    Session.setPid()
    # raise AppException("TESSTTTTT ERRORS.LOG")
    return Render.jsonTemplate('TITRE', 'WOOHOO', categorie="INFO", code=200)

# ----------------------------------------------------------------------------------------------------
# Chemin pour test Erreur JSON
# Page Racine du Site
# ----------------------------------------------------------------------------------------------------


@api_test_bp.route('/testJSONProgress', methods=['POST'])
# @login_required
@csrf_protect
def testJSONProgress():

    def run(pid, user):
        try:
            x = 0
            while x <= 100:
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="TITLE")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="NORMAL")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="NORMAL")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="NORMAL")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="NORMAL")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="INFO")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="ERROR")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="SUCCESS")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="WARNING")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="DEFAULT")
                yield Render.sseTemplate(perc=x, message="TESTTASK" + str(x), operation=_OPERATION, categorie="ERROR_TASK")
                yield Render.sseTemplate(perc=x, message="TESTTASK" + str(x), operation=_OPERATION, categorie="SUCCESS_TASK")
                yield Render.sseTemplate(perc=x, message="TEST" + str(x), operation=_OPERATION, categorie="WARNING")
                x = x + 75
                # if x == 75:
                #     raise Exception("NOOOOOOOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNN")
            yield Render.sseTemplate(perc=100, message="Fin de traitement", operation="WOO HOO", categorie="SUCCESS")
        except Exception as error:
            logger.pid = pid
            logger.user = user
            logger.error('{APP_NAME} à rencontré une erreur (TRAITEMENT)'.format(APP_NAME=cfg._APP_NAME))
            logger.critical()
            yield Render.sseTemplate(perc=100, message=str(error), operation=_OPERATION, categorie="ERROR")
        finally:
            time.sleep(0.2)

    # return Render.jsonTemplate(_OPERATION, "ESSAI", categorie="WARNING", data=None)
    # raise Exception("NOOOOOOOOOOOOOOOOOOOOOONNNNNNNNNNNNNNNNN")
    Session.setPid()

    return Response(run(pid=Session.getPid(), user=Session.getUserDisplay()), mimetype='text/event-stream')
