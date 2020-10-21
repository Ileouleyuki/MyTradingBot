#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# UTILS
######################################################################################################
# Description : Classe de Snippets Utiles
# Date de Creation : 18/03/2020
######################################################################################################
# Globales
from random import randint
import datetime

######################################################################################################
# CLASS
######################################################################################################


class Utils:

    def __init__(self):
        pass
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def parseForm(formData):
        """Supprime le csrfToken"""
        if "csrfToken" in formData:
            del formData["csrfToken"]
        return formData
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def isBlank(myString):
        """Retourne True si la chaine est vide"""
        return not (myString and myString.strip())
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def isNotBlank(myString):
        """Retourne True si la chaine est non-vide"""
        return bool(myString and myString.strip())
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def generate_pid() -> int:
        """Genere un nombre aleatoire"""
        return randint(0, 9999999999999999)
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def generate_prefix() -> int:
        """Genere un nombre aleatoire"""
        # return randint(0, 9999999999999999)
        return str(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(randint(0, 99)))

    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def percentage_of(percent, whole):
        """Renvoie la valeur du pourcentage sur l'ensemble"""
        return (percent * whole) / 100.0
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def percentage(part, whole):
        """Renvoie la valeur en pourcentage de la pièce dans son ensemble"""
        return round(100 * float(part) / float(whole), 2)
    # ------------------------------------------------------------------------------------------------

    @staticmethod
    def isAjaxRequest(request):
        """Renvoie True si la request est de type AJAX"""
        request_xhr_key = request.headers.get('X-Requested-With')
        if request_xhr_key and request_xhr_key == 'XMLHttpRequest':
            return True
        # Si OK, on continue le traitement
        return False
