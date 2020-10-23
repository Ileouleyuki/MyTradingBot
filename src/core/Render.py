#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# RENDER
######################################################################################################
# Description : Interface pour le rendu des Vues et les reponse JSON
# Date de Creation : 06/05/2020
######################################################################################################
# Ajout du repertoire parent pour import
import datetime
import time
import json
# Flask
from flask import render_template, jsonify
# Perso
from core.Config import cfg
from core.Session import Session

# from lib.sysinfo import SysInfo


######################################################################################################
# CLASS
######################################################################################################


class Render:
    def __init__():
        pass
    # ------------------------------------------------------------------------------------------------

    def getInfo():
        """Retourne les informations necessaires au frontend"""
        info = {}
        # Utilisateur
        info["user"] = {
            'is_logged_in': Session.getValue("is_logged_in"),
            'displayName': Session.getValue("displayName"),
            'role': Session.getValue("role"),
            'username': Session.getValue("username")
        }
        # Application
        info["app"] = {
            'version': cfg._APP_VERSION,
            'name': cfg._APP_NAME,
            'auteur': cfg._APP_AUTEUR,
            'environ': cfg._ENVIRONNEMENT
        }
        # Javascript
        info["js"] = {
            'timeout': str(cfg._JS_TIMEOUT_LOADER),
            'csrfToken': Session.generateCsrfToken(),
            'root': cfg._ENV[cfg._ENVIRONNEMENT]["JS_ROOT_DEV"]
        }
        # System
        info["system"] = {
            'main': "TODO",  # SysInfo().getSystem(),
            'python': "TODO"  # SysInfo().getPython(),
        }
        # Compte
        info["compte"] = {
            # Courante
            'WorkOnCompte': Session.getValue("WorkOnCompte")
        }

        return info
    # ------------------------------------------------------------------------------------------------

    def htmlTemplate(path, data=None, code=200):
        """
        Renvoi le template defini par la variable PATH avec les datas
        """
        return render_template(path, info=Render.getInfo(), data=data), code

    # ------------------------------------------------------------------------------------------------

    def jsonTemplate(operation, message, categorie="INFO", data=None, code=200, silent=False):
        """
        Renvoi un message JSON structuré pour le Frontend avec son code HTTP correspondant
        Les types de Messages sont ["ERROR", "INFO", "WARNING", "SUCCESS", "CRITICAL", "DOWNLOAD"]
        Voir app.js pour traitement frontend
        """
        return jsonify({'oper': operation, 'mess': message, 'cat': categorie, 'data': data, 'silent': silent}), code

    # ------------------------------------------------------------------------------------------------

    def sseTemplate(perc, operation, message, categorie="NORMAL", data=None):
        """
        Renvoi un message SSE structuré pour le Frontend
        Les types de Messages sont ["ERROR", "INFO", "WARNING", "SUCCESS", "CRITICAL", "DOWNLOAD", "NORMAL","SUCCESS_TASK", "ERROR_TASK"]
        Voir app.js pour traitement frontend
        """
        resp = {}
        resp["perc"] = perc
        resp["date"] = str(datetime.datetime.now().strftime('%a %d %b %Y %H:%M:%S'))
        resp["oper"] = str(operation)
        resp["mess"] = message
        resp["cat"] = str(categorie)
        resp["data"] = data
        # Transforme JSON
        ret = " data: " + json.dumps(resp) + "\n\n###\n\n"
        # Temporisation
        time.sleep(cfg._APP_TIMEOUT_BETWEEN_SSE)

        return ret
