#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# ADMINISTRATION
######################################################################################################
# Description : Routes pour l'administration
# Date de Creation : 06/05/2020
######################################################################################################
# Flask
from flask import Blueprint
# Perso

from core.Render import Render
from core.Decorateur import login_required, roles_accepted


######################################################################################################
# INITIALISATION
######################################################################################################
admin_bp = Blueprint('admin', __name__)

######################################################################################################
# ROUTES
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /users
# Gestion des Utilisateurs accesible pour les utilisateurs CONNECTE et ADMINISTRATEUR
# ----------------------------------------------------------------------------------------------------


@admin_bp.route('/users')
@login_required
@roles_accepted("ADMIN")
def users():
    return Render.htmlTemplate('admin/users.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre /watcher
# Gestion des Utilisateurs accesible pour les utilisateurs CONNECTE et ADMINISTRATEUR
# ----------------------------------------------------------------------------------------------------


@admin_bp.route('/watcher')
@login_required
@roles_accepted("ADMIN")
def watcher():
    return Render.htmlTemplate('admin/watcher.html')

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre l'activité de l'application'
# Affiche le template activité
# ----------------------------------------------------------------------------------------------------


@admin_bp.route('/activity')
@login_required
@roles_accepted("ADMIN")
def activity():
    # Rendu de la vue
    return Render.htmlTemplate("admin/activity.html", data=None)

# ----------------------------------------------------------------------------------------------------
# Chemin GET pour atteindre les parametres de l'application'
# Affiche le template des parametres
# ----------------------------------------------------------------------------------------------------


@admin_bp.route('/param')
@login_required
@roles_accepted("ADMIN")
def param():
    # Rendu de la vue
    return Render.htmlTemplate("admin/param.html", data=None)
