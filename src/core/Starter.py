#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# APPLICATION
######################################################################################################
# Description : Parametrage et Lancement de l'application WEB
# Date de Creation : 06/05/2020
######################################################################################################
# https://github.com/gothinkster/flask-realworld-example-app/blob/master/conduit/settings.py


# Globale
import os
import locale
import sys
import datetime
from flask import Flask, request

# Perso
from core.Config import cfg
from core.Render import Render
from core.Session import Session
from core.Logger import Logger

# Routes
from routes.home.home import home_bp
from routes.api.test.ApiTest import api_test_bp
######################################################################################################
# MAIN
######################################################################################################


def create_app():
    """Une fabrique d'applications"""
    # -- Redefinit le locale pour les dates
    locale.setlocale(locale.LC_TIME, "")
    if cfg._ENVIRONNEMENT not in ('DEV', 'PROD', 'HORSPROD'):
        print("Votre definition de la variable de configuration ENVIRONNEMENT est incorrecte : {}".format(cfg._ENVIRONNEMENT))
        sys.exit(1)
    # Creation du repertoire TMP
    if not os.path.exists(cfg._TMP_PATH):
        os.makedirs(cfg._TMP_PATH)
    # Creation du repertoire LOGS
    if not os.path.exists(cfg._LOG_PATH):
        os.makedirs(cfg._LOG_PATH)
    # Creation du fichier WATCHER
    if not os.path.exists(cfg._ENV[cfg._ENVIRONNEMENT]["LOG_WATCHER_FILE"]) and cfg._ENV[cfg._ENVIRONNEMENT]["LOG_WATCHER"] is True:
        with open(cfg._ENV[cfg._ENVIRONNEMENT]["LOG_WATCHER_FILE"], 'w'):
            pass
    # Instanciation de l'app
    tmpl_dir = cfg._ROOT_DIR + os .sep + 'templates'
    static_dir = cfg._ROOT_DIR + os .sep + 'static'
    app = Flask(
        __name__,
        static_folder=static_dir,
        template_folder=tmpl_dir
    )

    # Parametrage de Flask
    app.config['SECRET_KEY'] = cfg._APP_SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=cfg._APP_PERMANENT_SESSION_LIFETIME)
    # app.config['UPLOAD_FOLDER'] = cfg._UPLOAD_PATH

    # Enregistrements des routes
    register_blueprints(app)

    # Enregistrements des ErrorsHandlers
    register_errorhandlers(app)

    # Enregitrement du Watcher (Observateur des URL)
    register_watcher(app)

    return app

######################################################################################################
# ROUTES
######################################################################################################


def register_blueprints(app):
    """
    Enregistrer les Flask blueprints.
    Definition BluePrints (Enregistrements des Routes)
    """
    # Frontend
    app.register_blueprint(home_bp, url_prefix='/')

    # API
    app.register_blueprint(api_test_bp, url_prefix='/test')


######################################################################################################
# ERRORS
######################################################################################################


def register_errorhandlers(app):
    """
    Enregistrer les gestionnaire d'erreurs
    Definition des Errors Handlers
    """
    @app.errorhandler(400)
    def bad_request(error):
        if request.path.startswith("/api/"):
            return Render.jsonTemplate(
                operation='Mauvaise Requete',
                message="La requête n'a pas pu être comprise par le serveur",
                categorie="ERROR",
                code=error.code
            )
        return Render.htmlTemplate("errors/{}.html".format(error.code), data=None, code=error.code)

    @app.errorhandler(401)
    def unauthentified(error):
        if request.path.startswith("/api/"):
            return Render.jsonTemplate(
                operation='Utilisateur deconnecté',
                message='Acces refusé par le serveur',
                categorie="ERROR",
                code=error.code
            )
        return Render.htmlTemplate("errors/{}.html".format(error.code), data=None, code=error.code)

    @app.errorhandler(403)
    def unauthorised(error):
        if request.path.startswith("/api/"):
            return Render.jsonTemplate(
                operation='Accés Interdit',
                message='Accés interdit à cette fonctionnalité',
                categorie="ERROR",
                code=error.code
            )
        return Render.htmlTemplate("errors/{}.html".format(error.code), data=None, code=error.code)

    @app.errorhandler(404)
    def page_not_found_error(error):
        if request.path.startswith("/api/"):
            return Render.jsonTemplate(
                operation='Chemin inconnu',
                message="L'URL est inconnu : {}".format(request.path),
                categorie="ERROR",
                code=error.code
            )
        return Render.htmlTemplate("errors/{}.html".format(error.code), data=None, code=error.code)

    @app.errorhandler(405)
    def incorrect_request(error):
        if request.path.startswith("/api/"):
            return Render.jsonTemplate(
                operation='OOPS !! Une erreur est arrivé',
                message='Methode Non Autorisé ou CSRF Incorrecte',
                categorie="ERROR",
                code=error.code
            )
        return Render.htmlTemplate("errors/{}.html".format(error.code), data=None, code=error.code)

    @app.errorhandler(Exception)
    def exceptions(e):
        logger = Logger()
        logger.pid = Session.getPid()
        logger.user = Session.getUserDisplay()
        # ----------------------------------------------------
        # Trace dans l'activité d'une erreur dans activity.log
        logger.error('{APP_NAME} à rencontré une erreur'.format(APP_NAME=cfg._APP_NAME))
        # ----------------------------------------------------
        # Trace de l'exception dans un fichier à part
        # Recuperation ERREUR et trace dans Activité
        exc_type, exc_value, exc_tb = sys.exc_info()
        # import traceback
        # traceback.print_exc()
        logger.critical(
            nom=exc_type.__name__,
            message=str(exc_value),
            trace=exc_tb
        )
        # Renvoi Erreur
        if request.path.startswith("/api/"):
            return Render.jsonTemplate(
                operation='OOPS !! Une erreur est arrivé',
                message='{MESSAGE}'.format(MESSAGE=exc_value),
                categorie="ERROR",
                code=500
            )
        return Render.htmlTemplate("errors/{}.html".format(str(500)), data=None, code=500)

######################################################################################################
# WATCHER
######################################################################################################


def register_watcher(app):
    @app.after_request
    def after_request(response):
        """Tracage des requetes URL."""
        # Cela évite la duplication du registre dans le journal,
        # puisque ce 500 est déjà connecté via @app.errorhandler.
        if (
            response.status_code != 500
            and not request.full_path.startswith('/static')
            and cfg._ENV[cfg._ENVIRONNEMENT]["LOG_WATCHER"] is True
        ):
            file_object = open(cfg._ENV[cfg._ENVIRONNEMENT]["LOG_WATCHER_FILE"], "a+")
            file_object.write("{} :: {} :: {} :: {} :: {} :: {} :: {} :: {}\n".format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                        request.remote_addr,
                        Session.getUserDisplay() if Session.getUserDisplay() is not None else "",
                        Session.getUserId() if Session.getUserId() is not None else "",
                        request.method,
                        request.scheme,
                        request.full_path,
                        response.status
            ))
            file_object.close()
        return response
