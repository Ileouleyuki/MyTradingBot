#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# DECORATEUR
######################################################################################################
# Description : Decorateur applicatif necessaire pour le fonctionnement de l'application
# Date de Creation : 06/05/2020
######################################################################################################
# Globale
from functools import wraps
# Flask
from flask import abort, request
# Perso
from core.Session import Session

######################################################################################################
# DECORATEUR
######################################################################################################


def login_required(f):
    """
    Verification si l'utilisateur est connecté
    """
    @wraps(f)
    # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
    def wrap(*args, **kwargs):
        if not Session.getIsLoggedIn():
            abort(401)
        return f(*args, **kwargs)
    return wrap

# ----------------------------------------------------------------------------------------------------


def roles_accepted(*role_names):
    """
    Verification si l'utilisateur est abilité à acceder via son role
    """
    # convertir la liste en une liste contenant cette liste.
    # Parce que roles_accepted (a, b) nécessite A ET B
    # alors que roles_accepted ([a, b]) nécessite A OU B
    def wrapper(view_function):
        @wraps(view_function)    # Indique aux débogueurs que c'est un wrapper de fonction
        def decorator(*args, **kwargs):
            # Si l'utilisateur est ADMIN, alors on accepte (Par default, les administrateurs à le droit d'acceder à tout)
            if Session.getUserRole() == "ADMIN":
                return view_function(*args, **kwargs)
            # Si l'utilisateur different de ADMIN, alors on verifie que le role est accepté
            if Session.getUserRole() not in role_names:
                abort(403)
            # C'est OK d'appeler la vue
            return view_function(*args, **kwargs)
        return decorator
    return wrapper

# ----------------------------------------------------------------------------------------------------


def csrf_protect(f):
    """
    Valider le jeton CSRF
    Le jeton CSRF peut être transmis avec les formulaires et les liens soumis associés aux opérations sensibles côté serveur.
    On ne valide le CSRF que pour la methode POST
    """
    @wraps(f)
    # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
    def wrap(*args, **kwargs):
        if request.method == "POST" and "csrfToken" in request.form:
            sendToken = request.form.get("csrfToken", None)
        else:
            return f(*args, **kwargs)
        if sendToken is None or sendToken != Session.getCsrfToken():
            # "Attaque CSRF "," Utilisateur : " . Session::getUserId () . " jeton CSRF non valide " . $userToken, __FILE__, __LINE__);
            abort(405)
        # Si tout est ok, on supprime le csrfToken du formulaire
        return f(*args, **kwargs)
    return wrap
