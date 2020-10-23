#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# SESSION
######################################################################################################
# Description : Interraction avec les Sessions
# Date de Creation : 06/05/2020
######################################################################################################
# Globale
import secrets
import time
# Flask
from flask import session
# Perso
from core.Utils import Utils

######################################################################################################
# CLASS
######################################################################################################


class Session:

    def __init__():
        pass

    @staticmethod
    def remove():
        """
        for key in session.keys():
            session.pop(key)
        """
        session.clear()

    @staticmethod
    def getAndDestroy(key):
        if key in session:
            val = session[key]
            del session[key]
            return val
        return None

    @staticmethod
    def getCsrfToken():
        return session["csrfToken"] if 'csrfToken' in session else None

    @staticmethod
    def getCsrfTokenTime():
        return session["csrfTokenTime"] if 'csrfTokenTime' in session else None

    @staticmethod
    def getPid():
        return session["pid"] if 'pid' in session else None

    @staticmethod
    def setPid():
        session["pid"] = Utils.generate_pid()

    @staticmethod
    def setValue(key, value):
        session[key] = value

    @staticmethod
    def getValue(key):
        return session[key] if key in session else None

    @staticmethod
    def getIsLoggedIn():
        return session["is_logged_in"] if 'is_logged_in' in session else False

    @staticmethod
    def getUserId():
        return session["username"] if 'username' in session else None

    @staticmethod
    def getUserRole():
        return session["role"] if 'role' in session else None

    @staticmethod
    def getUserDisplay():
        return session["displayName"] if 'displayName' in session else None

    def generateCsrfToken():
        """
        Obtenir un jeton CSRF et en générer un nouveau s'il a expiré
        """
        max_time = time.time() + (60 * 60 * 24)
        stored_time = Session.getCsrfTokenTime()
        csrfToken = Session.getCsrfToken()

        if (stored_time is None or csrfToken is None or max_time + stored_time <= time.time()):
            token = secrets.token_hex(nbytes=22)
            Session.setValue("csrfToken", token)
            Session.setValue("csrfTokenTime", time.time())
        return Session.getCsrfToken()
