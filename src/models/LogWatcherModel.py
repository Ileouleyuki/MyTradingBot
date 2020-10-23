#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# WATCHER
######################################################################################################
# Description : Modele interaction avec Observateur URLs
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
# Class AuthUsersModel
######################################################################################################


class LogWatcherModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._LOG_WATCHER_BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = cfg._LOG_WATCHER_TABLE

    ##################################################################################################
    # ENTRIES
    ##################################################################################################
    def getAll(self, Limit=None):
        """
        Retourne toutes les entrées de la table
        """
        query = """SELECT * from {TABLE} order by TimeStampUtc desc""".format(
                TABLE=self.table
            )
        df = self.getToDataFrame(query, Limit)
        return df
