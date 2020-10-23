#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# API >> ADMINISTRATION
######################################################################################################
# Description : Routes pour les urls API lié à l'administration
# Date de Creation : 06/05/2020
######################################################################################################
import os
import logging
import pandas as pd
# Flask
from flask import Blueprint, request, abort
# Perso
from core.Config import cfg
from core.Render import Render
from core.Utils import Utils
from core.Crypt import Crypt
from core.Exceptions import SqliteAdapterException
from core.Decorateur import login_required, roles_accepted, csrf_protect
# from models.AuthModel import AuthModel
from models.AuthUsersModel import AuthUsersModel
from models.LogWatcherModel import LogWatcherModel
from models.LogActivityModel import LogActivityModel
# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

######################################################################################################
# INITIALISATION
######################################################################################################
api_admin_bp = Blueprint('api.admin', __name__)

_OPERATION = "ADMINISTRATION"

######################################################################################################
# UTILISATEURS
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour renvoyer la liste des Utilisateurs
# Renvoi la liste des Utilisateurs
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/getUsers', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def getUsers():
    """Recuperation des Utilisateurs"""
    if request.method == 'POST':
        # Recuperation des infos
        data = AuthUsersModel().getAllUsers()
        # Decryptage des mots des passe + Cryptage des id
        for item in data:
            item["password"] = Crypt.decode(cfg._APP_SECRET_KEY, item["password"])
            item["id"] = Crypt.encode(cfg._APP_SECRET_KEY, item["id"])
        # Renvoi de la reponse JSON
        return Render.jsonTemplate(_OPERATION, 'Chargement des Utilisateurs', categorie="SUCCESS", data=data)
    else:
        abort(400)

# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour debloquer un Utilisateur
# Deblocage Utilisateur
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/deblockUser', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def deblockUser():
    if request.method == 'POST':
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        # Decryptage id
        data["id"] = Crypt.decode(cfg._APP_SECRET_KEY, data["id"])
        # Recuperation utiisateur
        mdl = AuthUsersModel()
        user = mdl.getUserById(data["id"])
        # Execution du deblocage
        try:
            mdl.resetFailedLogins(user["username"])
        except SqliteAdapterException as errorSQL:
            return Render.jsonTemplate(_OPERATION, 'Deblocage Utilisateur Impossible : {}'.format(str(errorSQL)), categorie="ERROR")
        else:
            return Render.jsonTemplate(_OPERATION, 'Deblocage Utilisateur', categorie="SUCCESS")
    else:
        abort(400)

# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour mettre à jour un Utlisateur
# Mise à jour Utilisateur
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/updateUser', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def updateUser():
    if request.method == 'POST':
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        data["password"] = Crypt.encode(cfg._APP_SECRET_KEY, data["password"])
        data["id"] = Crypt.decode(cfg._APP_SECRET_KEY, data["id"])
        # Traitement en BDD
        mdl = AuthUsersModel(cfg._BDD_PATH)
        try:
            mdl.updateUser(data)
        except SqliteAdapterException as errorSQL:
            return Render.jsonTemplate(_OPERATION, 'Modification Utilisateur Impossible : {}'.format(str(errorSQL)), categorie="ERROR")
        else:
            return Render.jsonTemplate(_OPERATION, 'Modification Utilisateur', categorie="SUCCESS")
    else:
        abort(400)
# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour ajouter un Utlisateur
# Ajouter un Utilisateur
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/addUser', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def addUser():
    if request.method == 'POST':
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        # Cryptage des mots des passe + Decryptage des id
        data["password"] = Crypt.encode(cfg._APP_SECRET_KEY, data["password"])
        data["id"] = Crypt.decode(cfg._APP_SECRET_KEY, data["id"])
        mdl = AuthUsersModel(cfg._BDD_PATH)
        # Verification
        if mdl.is_unique_username(data["username"]) is False:
            return Render.jsonTemplate(_OPERATION, "Un utilisateur avec cet identifiant existe déjà", categorie="WARNING")
        # Traitement en BDD
        try:
            mdl.insertUser(data)
        except SqliteAdapterException as errorSQL:
            return Render.jsonTemplate(_OPERATION, 'Ajout Utilisateur Impossible : {}'.format(str(errorSQL)), categorie="ERROR")
        else:
            return Render.jsonTemplate(_OPERATION, 'Ajout Utilisateur', categorie="SUCCESS")
    else:
        abort(400)
# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour mettre à jour un Utlisateur
# Suppression Utilisateur
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/deleteUser', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def deleteUser():
    if request.method == 'POST':
        # Recuperation + traitement des données du formulaire
        data = Utils.parseForm(dict(request.form))
        # Decryptage id
        data["id"] = Crypt.decode(cfg._APP_SECRET_KEY, data["id"])
        mdl = AuthUsersModel(cfg._BDD_PATH)
        # Verification que la valeur username n'existe pas déjà
        try:
            mdl.deleteUser(data)
        except SqliteAdapterException as errorSQL:
            return Render.jsonTemplate(_OPERATION, 'Suppression Utilisateur Impossible : {}'.format(str(errorSQL)), categorie="ERROR")
        else:
            return Render.jsonTemplate(_OPERATION, 'Suppression Utilisateur', categorie="SUCCESS")
    else:
        abort(400)
######################################################################################################
# WATCHER
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour renvoyer les infos de l'observateur
# Observateur des requetes URL
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/getWatcherEntries', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def getWatcherEntries():
    if request.method == 'POST':
        # Recuperation des infos
        data = LogWatcherModel().getAll()
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Observateur URL', categorie="SUCCESS", data=data.to_dict("Record"))
    else:
        abort(400)

######################################################################################################
# ACTIVITE
######################################################################################################
# ----------------------------------------------------------------------------------------------------
# Chemin POST (XHR) pour renvoyer les infos des Logs d'activité
# Activité de l'application
# ----------------------------------------------------------------------------------------------------


@api_admin_bp.route('/getActivityEntries', methods=['POST'])
@login_required
@roles_accepted("ADMIN")
@csrf_protect
def getActivityEntries():
    """Parse un fichier de log dans un DataFrame"""
    if request.method == 'POST':
        # Recuperation des infos
        data = LogActivityModel().getAll()
        # Retour du message
        return Render.jsonTemplate(_OPERATION, 'Activité', categorie="SUCCESS", data=data.to_dict("Record"))
    else:
        abort(400)
