#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# IP BLOQUE
######################################################################################################
# Description : Modele interaction avec Ip Bloqué
# Auteur : ileouleyuki
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
                    ip TEXT primary key NOT NULL,
                    created_at_utc TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    updated_at_utc TIMESTAMP(6)
                )"""
######################################################################################################
# Class AuthIpBlockedModel
######################################################################################################


class AuthIpBlockedModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = "mtb_auth_blocked_ip"
        # Creation de la table
        if not self.tblExists(table=self.table):
            logger.info("Table {} inexistante >> Creation".format(self.table))
            query = initial_sql.format(TABLE=self.table)
            self.query(query)

    ##################################################################################################
    # IP BLOCKED
    ##################################################################################################
    def isIpBlocked(self, userIP):
        """
        Determine si IP bloqué
        """
        query = """ SELECT ip FROM {TABLE} WHERE ip ='{IP}' LIMIT 1;""".format(
            TABLE=self.table,
            IP=userIP
        )
        result = self.get(query, None)
        if result is None:
            return False
        else:
            return True

    def blockIP(self, IP):
        """
        Ajouter adresse IP au blocage
        """
        query = """ INSERT INTO {TABLE} (ip) VALUES ('{IP}')""".format(
            TABLE=self.table,
            IP=IP
        )
        ret = self.query(query)
        return ret
