#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# LOGGER
######################################################################################################
# Description : Class pour gestion du log des activités
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import os
import sys
import datetime
import pandas as pd
import traceback
# Perso
from core.Config import cfg
######################################################################################################
# CLASS
######################################################################################################


class Logger:
    def __init__(self):
        """Initialisation"""
        # Parametres
        self.__isActive = cfg.LOG_ACTIVITY
        self.__file = cfg.LOG_ACTIVITY_FILE
        self.__size = cfg.LOG_ACTIVITY_SIZE
        self.__pid = None
        self.__user = None
        self.__fileError = cfg.LOG_ACTIVITY_ERROR_FILE
        self.__sizeError = cfg.LOG_ACTIVITY_ERROR_SIZE
        # Verification
        if not os.path.exists(self.__file) and self.__isActive is True:
            with open(self.__file, 'w+', encoding="utf-8") as activity:
                pass
            activity.close()
        if not os.path.exists(self.__fileError) and self.__isActive is True:
            with open(self.__fileError, 'w+', encoding="utf-8") as activity:
                pass
            activity.close()

    # ------------------------------------------------------------------------------------------------

    def write(self, message, level=["INFO", "DEBUG", "ERROR", "CRITICAL", "SUCCESS"]):
        """Ajoute une entrée au fichier"""
        # Ouverture
        file_obj = open(self.__file, "a+", encoding="utf-8")
        # Ecriture
        file_obj.write("{DATE} :: {LEVEL: <10s} :: {USER} :: {PID} :: {MESSAGE}\n".format(
                DATE=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                LEVEL=level.upper(),
                USER=self.__user,
                PID=str(self.__pid) if self.__pid is not None else "",
                MESSAGE=message
        ))
        # Fermeture
        file_obj.close()

    # ------------------------------------------------------------------------------------------------

    @property
    def pid(self):
        """Obtenir le PID"""
        return self.__pid

    @pid.setter
    def pid(self, value):
        """Definir le PID"""
        self.__pid = value

    @property
    def user(self):
        """Obtenir le USER"""
        return self.__user

    @user.setter
    def user(self, value):
        """Definir le USER"""
        self.__user = value
    # ------------------------------------------------------------------------------------------------

    def read(self):
        """Retourne le contenu du fichier dans un Dict"""
        if os.path.exists(self.__file) is False:
            raise Exception("Le Fichier des ACTIVITE n'existe pas : {}".format(self.__file))
        # Construction DataFrame
        dfLog = pd.read_csv(
            self.__file,
            sep="::",
            names=['date', 'niveau', 'user', 'pid', 'message'],
            engine='python',
            encoding='UTF-8'
        )
        # Conversion de la date en DateTime
        # dfLog['date'] = pd.to_datetime(dfLog['date'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime(
        #    "%a %d %b %Y (S%W) %H:%M:%S"
        #    )
        # Trier le Dataframe
        dfLog.sort_values("date", axis=0, ascending=False, inplace=True, na_position='last')
        # Filtrer le DataFrame
        # df_masked = df[(df.date > '2012-04-01') & (df.date < '2012-04-04')]
        return dfLog.to_dict("Record")
    # ------------------------------------------------------------------------------------------------

    def readError(self):
        """Retourne le contenu du fichier Erreurs dans un Dict"""
        if os.path.exists(self.__fileError) is False:
            raise Exception("Le Fichier des ERREURS n'existe pas : {}".format(self.__file))
        # Lecture du fichier
        """
        with open(self.__fileError, "r") as fileErr:
            for line in fileErr:
                if line == "#############################################################################\n"

                str = line.split()
                print(str)
        """
        file = open(self.__fileError, mode='r')
        content = file.read()
        ret = content.split("#############################################################################")
        # Split du content par le separateur

        # Construction DataFrame
        # dfLog = pd.read_csv(
        #    self.__fileError,
        #    sep="#############################################################################",
        #    names=['erreur'],
        #    engine='python',
        #    encoding='UTF-8'
        # )
        # Conversion de la date en DateTime
        # dfLog['date'] = pd.to_datetime(dfLog['date'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime(
        #    "%a %d %b %Y (S%W) %H:%M:%S"
        #    )
        # Trier le Dataframe
        # dfLog.sort_values("date", axis=0, ascending=False, inplace=True, na_position='last')
        # Filtrer le DataFrame
        # df_masked = df[(df.date > '2012-04-01') & (df.date < '2012-04-04')]
        return ret
    # ------------------------------------------------------------------------------------------------

    def info(self, message):
        """Ecriture INFO"""
        self.write(message, level="INFO")

    # ------------------------------------------------------------------------------------------------

    def error(self, message):
        """Ecriture ERROR"""
        self.write(message, level="ERROR")

    # ------------------------------------------------------------------------------------------------

    def debug(self, message):
        """Ecriture DEBUG si le Debug Mode est actif"""
        if cfg._ENV[cfg._ENVIRONNEMENT]["DEBUG_MODE"] is True:
            self.write(message, level="DEBUG")

    # ------------------------------------------------------------------------------------------------

    def critical(self, nom=None, message=None, trace=None):
        """
        Ecriture CRITICAL dans fichiers d'erreurs
        """
        # Recuperation ERREUR et trace dans Activité
        exc_type, exc_value, exc_tb = sys.exc_info()

        # self.error('{NAME} >>> {MESSAGE}'.format(NAME=exc_type.__name__, MESSAGE=exc_value))

        # Ouverture
        file_obj = open(self.__fileError, "a", encoding="utf-8")
        # Formatage
        ErrorTxt = "=============================================================================\n"
        ErrorTxt += "ERREUR EXECUTION DANS LEO\n"
        ErrorTxt += "=============================================================================\n"
        ErrorTxt += "-----------------------------------------------------------------------------\n"
        ErrorTxt += "DATE".ljust(25, " ") + ": {DATE: <10s}\n".format(DATE=datetime.datetime.now().strftime("%a %d %b %Y %H:%M:%S"))
        ErrorTxt += "NIVEAU".ljust(25, " ") + ": CRITIQUE\n"
        ErrorTxt += "UTILISATEUR".ljust(25, " ") + ": {USER: <10s}\n".format(USER=str(self.__user) if self.__user is not None else "")
        ErrorTxt += "PID".ljust(25, " ") + ": {PID: <10s}\n".format(PID=str(self.__pid) if self.__pid is not None else "")
        ErrorTxt += "NOM".ljust(25, " ") + ": {NOM: <10s}\n".format(NOM=exc_type.__name__)
        ErrorTxt += "MESSAGE".ljust(25, " ") + ": {MESSAGE: <10s}\n".format(MESSAGE=str(exc_value))
        ErrorTxt += "-----------------------------------------------------------------------------\n"
        ErrorTxt += "TRACEBACK\n"
        ErrorTxt += "-----------------------------------------------------------------------------\n"
        ErrorTxt += traceback.format_exc()
        ErrorTxt += "-----------------------------------------------------------------------------\n"
        # Separateur
        ErrorTxt += "#############################################################################\n"
        # Ajout
        file_obj.write(ErrorTxt)
        # Fermeture
        file_obj.close()

    # ------------------------------------------------------------------------------------------------

    def success(self, message):
        """Ecriture SUCCESS"""
        self.write(message, level="SUCCESS")
        self.__pid = None
