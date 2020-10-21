#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# WSGI (Point d'entrée de l'application)
######################################################################################################
# Description : Lancement de l'application WEB pour gunicorn
# Date de Creation : 20/05/2020
######################################################################################################
# Globale
from core.Starter import create_app
from core.Config import cfg

app = create_app()

if __name__ == '__main__':
    app.run(debug=cfg._ENV[cfg._ENVIRONNEMENT]["DEBUG_MODE"])