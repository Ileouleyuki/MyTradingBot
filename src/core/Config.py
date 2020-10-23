#!/usr/bin/env python
# encoding: utf-8
###############################################################################
# CONFIGUERATION
###############################################################################
import os


class cfg():
    # -------------------------------------------------------------------------
    # Parametres: APPLICATION
    # -------------------------------------------------------------------------
    # Parametres relatives aux informations applicatives :
    #   - Version
    #   - Nom
    #   - Auteur
    #   - ...
    # -------------------------------------------------------------------------
    # Informations
    _APP_VERSION = "1.1.0"
    _APP_NAME = "Warren"
    _APP_VERSION_INFO__ = tuple([int(num) for num in _APP_VERSION.split('.')])
    _APP_AUTEUR = "DENIS Julien (Ileouleyuki)"
    # Variable determinant la config de l'environnement : PROD ou DEV
    _ENVIRONNEMENT = "DEV"
    # Dict des configuration
    _ENV = {}
    # Passphrase necessaire à l'application
    _APP_SECRET_KEY = "C7pxfX6d273T9AZL2fJS93Bf966LY6m2t7WrfT9gimwdsnjmYQ98b97pNNX8G9XS"
    # Durée de vie des session en heures
    _APP_PERMANENT_SESSION_LIFETIME = 1
    # Definir le temps d'attente de deverouillage de la page apres chargement
    _JS_TIMEOUT_LOADER = 1000  # 1s
    # Definir la temporisation entre chaque message SSE
    _APP_TIMEOUT_BETWEEN_SSE = 0.2

    # -------------------------------------------------------------------------
    # Parametres: PATH
    # -------------------------------------------------------------------------
    # Parametres definissant les chemin necessaires au fonctionnement
    # de l'application :
    #   - BDD
    #   - Racine
    #   - Temporaire
    #   - ...
    # -------------------------------------------------------------------------
    # Chemin où se trouve ce propre fichier
    # _ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
    # Remonte d'un niveau par rapport à ce propre fichier (Repertoire Parent)
    _ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # Chemin Initiale (README.md, CHANGELOG.md)
    _INIT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    # PATH vers la BDD applicative contenant les utilisateurs
    _BDD_PATH = _ROOT_DIR + os.sep + "data" + os.sep + "app.db"
    # PATH vers le repertoire TEMP
    _TMP_PATH = _ROOT_DIR + os.sep + "tmp"
    # PATH vers le repertoire LOG
    _LOG_PATH = _INIT_DIR + os.sep + "logs"

    # -------------------------------------------------------------------------
    # Parametres: LOGGING
    # -------------------------------------------------------------------------
    # Parametres relatif au log applicatif, observateur et bot :
    # -------------------------------------------------------------------------
    # Parametres du journal de log (Activité)
    _LOG_ACTIVITY = True
    _LOG_ACTIVITY_BDD_PATH = _BDD_PATH
    _LOG_ACTIVITY_TABLE = "mtb_log_activity"
    _LOG_ACTIVITY_NAME = _APP_NAME + "Activity"
    # Parametres du journal de log (Observateur)
    _LOG_WATCHER = True
    _LOG_WATCHER_BDD_PATH = _BDD_PATH
    _LOG_WATCHER_TABLE = "mtb_log_watcher"
    _LOG_WATCHER_NAME = _APP_NAME + "Watcher"
    # Parametres du journal de log (Observateur)
    _LOG_BOT = True
    _LOG_BOT_BDD_PATH = _ROOT_DIR + os.sep + "data" + os.sep + "bot.db"
    _LOG_BOT_TABLE = "mtb_log_bot"
    _LOG_BOT_NAME = _APP_NAME + "Bot"

    # -------------------------------------------------------------------------
    # Configuration : DEVELOPPEMENT
    # -------------------------------------------------------------------------
    # Parametres definissant la configurantion de l'environement de DEV
    # necessaire :
    #   - Niveau de Debug
    #   - Chemin relatif des URL
    #   - ...
    # -------------------------------------------------------------------------
    _ENV["DEV"] = {}
    # Activer le mode DEBUG de Flask ?
    _ENV["DEV"]["DEBUG_MODE"] = True
    # Route pour redirection JS
    _ENV["DEV"]["JS_ROOT_DEV"] = 'http://127.0.0.1:5000/'
    # En DEV, on ne trace pas toutes les requetes
    _ENV["DEV"]["LOG_WATCHER"] = False
    _ENV["DEV"]["LOG_WATCHER_FILE"] = _LOG_PATH + os.sep + "watch.log"
    _ENV["DEV"]["LOG_WATCHER_NAME"] = "watcher"

    # -------------------------------------------------------------------------
    # Configuration : PRODUCTION
    # -------------------------------------------------------------------------
    # Parametres definissant la configurantion de l'environement de PROD
    # necessaire :
    #   - Niveau de Debug
    #   - Chemin relatif des URL
    #   - ...
    # -------------------------------------------------------------------------
    _ENV["PROD"] = {}
    # Activer le mode DEBUG de Flask ?
    _ENV["PROD"]["DEBUG_MODE"] = False
    # Route pour redirection JS
    _ENV["PROD"]["JS_ROOT_DEV"] = 'http://127.0.0.1/'
    # En PROD, on trace toute les requetes
    _ENV["PROD"]["LOG_WATCHER"] = True
    _ENV["PROD"]["LOG_WATCHER_FILE"] = _LOG_PATH + os.sep + "watch.log"
    _ENV["PROD"]["LOG_WATCHER_NAME"] = "watcher"
