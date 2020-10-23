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
import logging
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

    def updateParam(self, data):
        # Construction de la requete
        query = """UPDATE {TABLE} SET """.format(TABLE=self.table)
        fields = list()
        for key, value in data.items():
            if key.lower() == "id":
                continue
            if key.lower() == "csrftoken":
                continue
            if value is None or len(value) == 0:
                continue
            fields.append("{FIELD} = '{VALUE}' ".format(FIELD=key, VALUE=value))

        # Jointure de la chaine de caractere
        query += ", ".join(map(str, fields))
        # Ajout de la condition de mise à jour
        query += " WHERE id = {ID}".format(ID=data["id"])
        # Execution
        ret = self.query(query)
        return ret

    def insertParam(self, data):
        # Extraction col and values
        values = list()
        columns = list()
        for key, value in data.items():
            if key.lower() == "csrftoken":
                continue
            if value is None or len(value) == 0:
                continue
            columns.append(key)
            values.append(value)

        cols = '( ' + ', '.join(map(str, columns)) + ' )'
        values = '( "' + '", "'.join(map(str, values)) + '" )'
        # Construction de la requete
        query = "INSERT INTO {TABLE} {columns} values {values};".format(TABLE=self.table, columns=cols, values=values)
        # Execution
        ret = self.query(query)
        return ret
