#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# PARAMETRES
######################################################################################################
# Description : Modele interaction avec les parametres du Bot
# Auteur : ileouleyuki
# Version : V1
# Date de Creation : 18/03/2020
######################################################################################################
import os
import json
from pathlib import Path
import logging

"""
import sys
import inspect
# Ajout du repertoire au system pour facilter les import des modules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)
sys.path.append(os.path.dirname(__file__))
"""
from lib.sqliteadapter import SqliteAdapter
from core.Config import cfg

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)
######################################################################################################
# Requetes SQL
######################################################################################################
initial_sql = """CREATE TABLE IF NOT EXISTS {TABLE}(
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "code"	TEXT,
                    "libelle"	TEXT,
                    "value" TEXT,
                    created_at_utc TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    updated_at_utc TIMESTAMP(6),
                    UNIQUE(code)
                )"""
######################################################################################################
# Class ParamModel
######################################################################################################


class ParamModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = "mtb_param"
        # Creation de la table
        if not self.tblExists(table=self.table):
            logger.info("Table {} inexistante >> Creation".format(self.table))
            query = initial_sql.format(TABLE=self.table)
            self.query(query)
            logger.info('Integration des parametres par default')
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")) + os.sep + 'install' + os.sep + 'param.sql'
            self.queryFile(path, param={'table': self.table})

    ##################################################################################################
    # ENTRIES
    ##################################################################################################
    def getAll(self, Limit=None):
        """
        Retourne toutes les entrées de la table
        """
        query = """SELECT * from {TABLE}""".format(
                TABLE=self.table
            )
        df = self.getToDataFrame(query, Limit)
        return df

    def getParam(self, code):
        """
        Retourne la valeur du parametre defini par son code
        """
        query = """SELECT code, value from {TABLE} where code = "{CODE}" """.format(
                TABLE=self.table,
                CODE=code
            )
        # Execution
        ret = self.get(query)
        # Retour
        if ret is not None:
            return ret['value']
        return ret

    def getBotConfig(self):
        """
        Retourne la Config pour le Bot
        """
        query = """SELECT code, value from {TABLE} """.format(TABLE=self.table)
        # Recuperation Config en BDD
        config = self.getToDataFrame(query).to_dict('Records')
        # Conversion en dictionnaire : key : code et value : value
        ConfigDict = {}
        for element in config:
            ConfigDict[element['code']] = element['value']
        # Recuperation des identifiants
        credentials = self.getCredentials()
        # Concatenation des 2 Dict
        return {**ConfigDict, **credentials}

    def getCredentials(self):
        """
        Obtenir les Identifiants de Compte
        """
        ret = None
        # Determination du path
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + os.sep + 'data' + os.sep + 'xtb.json'
        # Verification existance du Fichier
        if not os.path.isfile(path):
            logger.error("Le fichier de Configuration n'existe pas : {}".format(path))
            return ret
        with Path(path).open(mode="r") as f:
            ret = json.load(f)
        return ret

    def updateParam(self, data):
        # Construction de la requete
        sql = self.updateQuery(table=self.table, data=data)
        # Execution
        ret = self.query(sql)
        return ret

    def insertParam(self, data):
        # Construction de la requete
        sql = self.insertQuery(table=self.table, data=data)
        # Execution
        ret = self.query(sql)
        return ret

######################################################################################################
# TEST
######################################################################################################


if __name__ == "__main__":
    print("DEBUT")
    testObj = ParamModel()

    ret = testObj.getParam('time_zone')
    print(ret)

    ret = testObj.getCredentials()
    print(ret)

    ret = testObj.getBotConfig()
    print(ret)
