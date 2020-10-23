#!/usr/bin/env python
# encoding: utf-8
###############################################################################
# AUTH
###############################################################################
import time
import uuid
from models.AuthIpBlockedModel import AuthIpBlockedModel
from models.AuthFailedLoginModel import AuthFailedLoginModel
from models.AuthUsersModel import AuthUsersModel
from core.Exceptions import AppException
from core.Config import cfg
from core.Crypt import Crypt
from core.Session import Session
######################################################################################################
# CLASS
######################################################################################################


class Auth:
    def __init__():
        pass

    @staticmethod
    def isIpBlocked(ip=None):
        """
        Verifie si l'IP en parametre est presente dans la table des ip bloqués
        """
        # Verification IP
        if ip is None:
            raise AppException("[AUTH] - Aucune ip à verifier")
        # Initialisation du Modele
        mdl = AuthIpBlockedModel()
        # DEBUG - blocage de l'IP
        # mdl.blockIP(ip)
        # Verification
        return mdl.isIpBlocked(ip)

    def getFailedLoginByUser(username=None):
        """
        Retourne le nombre de Tentative de connexion echoué
        """
        # Verification USERNAME
        if username is None:
            raise AppException("[AUTH] - Aucune Identifiant à verifier")
        # Initialisation du Modele
        mdl = AuthFailedLoginModel()
        # Retourne le nombre de tentaive d'echec
        failedLogin = mdl.getFailedLoginByUser(username=username)
        if failedLogin is not None:
            if failedLogin["last_failed_login"] is not None and failedLogin["failed_login_attempts"] is not None:
                block_time = (10 * 60)  # 10 Minutes
                time_elapsed = time.time() - time.mktime(time.strptime(failedLogin["last_failed_login"], "%Y-%m-%d %H:%M:%S"))
                # TODO Si l'utilisateur est bloqué, mettre à jour les connexions échouées / mots de passe oubliés
                # à l'heure actuelle et éventuellement au nombre de tentatives à incrémenter,
                # mais, cela réinitialisera le last_time à chaque échec d'une tentative
                if (int(failedLogin["failed_login_attempts"]) >= 5 and time_elapsed < block_time):
                    # ici je ne peux pas définir un message d'erreur par défaut comme dans defaultMessages ()
                    # parce que le message d'erreur dépend de variables comme $ block_time & $ time_elapsed
                    return True
        return False

    def checkUser(username=None, password=None, ip=None):
        """
        Verifie la cohérenece login/password de l'utilisateur
        Si OK, alors creation de la Session
        """
        # Verification USERNAME
        if username is None:
            raise AppException("[AUTH] - Aucune Identifiant à verifier")
        # Verification PASSWORD
        if password is None:
            raise AppException("[AUTH] - Aucune Password à verifier")
        # Initialisation du Modele
        mdl = AuthUsersModel()
        # Recuperation des informations utilisateurs
        user = mdl.getUserByUsername(username)
        
        # Si l'utilisateur n'existe pas
        if user is None:
            return False
        # Mot de passe Incorrecte
        # if (user["password"] != Crypt.encode(cfg._APP_SECRET_KEY, password)):
        if (user["password"] != Crypt.encode(cfg._APP_SECRET_KEY, password)):
            # Si non valide, incrémenter le nombre de connexions ayant échoué
            mdlFailedLogon = AuthFailedLoginModel()
            mdlFailedLogon.incrementFailedLogins(username, mdlFailedLogon.getFailedLoginByUser(username), ip)
            
            # Egalement, vérifiez si l'adresse IP actuelle tente de se connecter à l'aide de plusieurs comptes,
            # Si c'est le cas, alors bloquez-le, sinon, ajoutez simplement un nouvel enregistrement à la base de données
            # TODO
            mdlFailedLogon.handleIpFailedLogin(ip, username)
            del mdlFailedLogon
            return False
        # Si le login est ok
        # Init Session
        idSession = uuid.uuid1()
        Session.setValue("id", idSession)
        Session.setValue("is_logged_in", True)
        Session.setValue("username", user["username"])
        Session.setValue("role", user["role"])
        Session.setValue("displayName", user["display"])
        # Enregistrement de last_connect + id de Session en bdd
        mdl.updateLastConn(username)
        mdl.updateIdSession(username, idSession)

        # Remise a zero des tentatives echoués
        AuthFailedLoginModel().resetFailedLogins(username)
        return True
