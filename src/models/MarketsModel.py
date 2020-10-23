#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# %MARKETS
######################################################################################################
# Description : Modele interaction avec les Marchés
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
                    "symbol"	TEXT,
                    "currency"	TEXT,
                    "categoryName"	TEXT,
                    "currencyProfit"	TEXT,
                    "backtest" INT DEFAULT 0,
                    "trade" INT DEFAULT 0,
                    "quoteId"	INTEGER,
                    "quoteIdCross"	INTEGER,
                    "marginMode"	INTEGER,
                    "profitMode"	INTEGER,
                    "pipsPrecision"	INTEGER,
                    "contractSize"	INTEGER,
                    "exemode"	INTEGER,
                    "time"	TEXT,
                    "expiration"	TEXT,
                    "stopsLevel"	INTEGER,
                    "precision"	INTEGER,
                    "swapType"	INTEGER,
                    "stepRuleId"	INTEGER,
                    "type"	INTEGER,
                    "instantMaxVolume"	INTEGER,
                    "groupName"	TEXT,
                    "description"	TEXT,
                    "longOnly"	TEXT,
                    "trailingEnabled"	TEXT,
                    "marginHedgedStrong"	TEXT,
                    "swapEnable"	TEXT,
                    "percentage"	INTEGER,
                    "bid"	TEXT,
                    "ask"	TEXT,
                    "high"	TEXT,
                    "low"	TEXT,
                    "lotMin"	INTEGER,
                    "lotMax"	INTEGER,
                    "lotStep"	INTEGER,
                    "tickSize"	TEXT,
                    "tickValue"	TEXT,
                    "swapLong"	TEXT,
                    "swapShort"	TEXT,
                    "leverage"	INTEGER,
                    "spreadRaw"	TEXT,
                    "spreadTable"	INTEGER,
                    "starting"	TEXT,
                    "swap_rollover3days"	INTEGER,
                    "marginMaintenance"	INTEGER,
                    "marginHedged"	INTEGER,
                    "initialMargin"	INTEGER,
                    "currencyPair"	TEXT,
                    "shortSelling"	TEXT,
                    "timeString"	TEXT,
                    created_at_utc TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    updated_at_utc TIMESTAMP(6)
                )"""
######################################################################################################
# Class MarketsModel
######################################################################################################


class MarketsModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = "mtb_markets"
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
