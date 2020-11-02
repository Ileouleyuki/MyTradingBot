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
                    "newsCountry" TEXT,
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
                    created_at_utc TIMESTAMP(13) DEFAULT CURRENT_TIMESTAMP,
                    updated_at_utc TIMESTAMP(13),
                    UNIQUE(symbol)
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

    def upsert(self, record):
        """
        Insertion d'un enregistrement.
        Si Existant, alors on met à jour
        """
        query = """INSERT INTO {TABLE} (
                    symbol,
                    currency,
                    categoryName,
                    currencyProfit,
                    quoteId,
                    quoteIdCross,
                    marginMode,
                    profitMode,
                    pipsPrecision,
                    contractSize,
                    exemode,
                    time,
                    expiration,
                    stopsLevel,
                    precision,
                    swapType,
                    stepRuleId,
                    type,
                    instantMaxVolume,
                    groupName,
                    description,
                    longOnly,
                    trailingEnabled,
                    marginHedgedStrong,
                    swapEnable,
                    percentage,
                    bid,
                    ask,
                    high,
                    low,
                    lotMin,
                    lotMax,
                    lotStep,
                    tickSize,
                    tickValue,
                    swapLong,
                    swapShort,
                    leverage,
                    spreadRaw,
                    spreadTable,
                    starting,
                    swap_rollover3days,
                    marginMaintenance,
                    marginHedged,
                    initialMargin,
                    currencyPair,
                    shortSelling,
                    timeString
            ) VALUES (
                    {symbol},
                    {currency},
                    {categoryName},
                    {currencyProfit},
                    {quoteId},
                    {quoteIdCross},
                    {marginMode},
                    {profitMode},
                    {pipsPrecision},
                    {contractSize},
                    {exemode},
                    {time},
                    {expiration},
                    {stopsLevel},
                    {precision},
                    {swapType},
                    {stepRuleId},
                    {type},
                    {instantMaxVolume},
                    {groupName},
                    {description},
                    {longOnly},
                    {trailingEnabled},
                    {marginHedgedStrong},
                    {swapEnable},
                    {percentage},
                    {bid},
                    {ask},
                    {high},
                    {low},
                    {lotMin},
                    {lotMax},
                    {lotStep},
                    {tickSize},
                    {tickValue},
                    {swapLong},
                    {swapShort},
                    {leverage},
                    {spreadRaw},
                    {spreadTable},
                    {starting},
                    {swap_rollover3days},
                    {marginMaintenance},
                    {marginHedged},
                    {initialMargin},
                    {currencyPair},
                    {shortSelling},
                    {timeString}
            )
            ON CONFLICT (symbol) DO UPDATE SET
            symbol = {symbol},
            currency = {currency},
                    categoryName = {categoryName},
                    currencyProfit = {currencyProfit},
                    quoteId = {quoteId},
                    quoteIdCross = {quoteIdCross},
                    marginMode = {marginMode},
                    profitMode = {profitMode},
                    pipsPrecision = {pipsPrecision},
                    contractSize = {contractSize},
                    exemode = {exemode},
                    time = {time},
                    expiration = {expiration},
                    stopsLevel = {stopsLevel},
                    precision = {precision},
                    swapType = {swapType},
                    stepRuleId = {stepRuleId},
                    type = {type},
                    instantMaxVolume = {instantMaxVolume},
                    groupName = {groupName},
                    description = {description},
                    longOnly = {longOnly},
                    trailingEnabled = {trailingEnabled},
                    marginHedgedStrong = {marginHedgedStrong},
                    swapEnable = {swapEnable},
                    percentage = {percentage},
                    bid = {bid},
                    ask = {ask},
                    high = {high},
                    low = {low},
                    lotMin = {lotMin},
                    lotMax = {lotMax},
                    lotStep = {lotStep},
                    tickSize = {tickSize},
                    tickValue = {tickValue},
                    swapLong = {swapLong},
                    swapShort = {swapShort},
                    leverage = {leverage},
                    spreadRaw = {spreadRaw},
                    spreadTable = {spreadTable},
                    starting = {starting},
                    swap_rollover3days = {swap_rollover3days},
                    marginMaintenance = {marginMaintenance},
                    marginHedged = {marginHedged},
                    initialMargin = {initialMargin},
                    currencyPair = {currencyPair},
                    shortSelling = {shortSelling},
                    timeString =  {timeString},

            updated_at_utc = CURRENT_TIMESTAMP;
            """.format(
                TABLE=self.table,
                symbol="\"" + str(record["symbol"]) + "\"" if "symbol" in record and record["symbol"] is not None else 'NULL',
                currency="\"" + str(record["currency"]) + "\"" if "currency" in record and record["currency"] is not None else 'NULL',
                categoryName="\"" + str(record["categoryName"]) + "\"" if "categoryName" in record and record["categoryName"] is not None else 'NULL',
                currencyProfit="\"" + str(record["currencyProfit"]) + "\"" if "currencyProfit" in record and record["currencyProfit"] is not None else 'NULL',
                quoteId="\"" + str(record["quoteId"]) + "\"" if "quoteId" in record and record["quoteId"] is not None else 'NULL',
                quoteIdCross="\"" + str(record["quoteIdCross"]) + "\"" if "quoteIdCross" in record and record["quoteIdCross"] is not None else 'NULL',
                marginMode="\"" + str(record["marginMode"]) + "\"" if "marginMode" in record and record["marginMode"] is not None else 'NULL',
                profitMode="\"" + str(record["profitMode"]) + "\"" if "profitMode" in record and record["profitMode"] is not None else 'NULL',
                pipsPrecision="\"" + str(record["pipsPrecision"]) + "\"" if "pipsPrecision" in record and record["pipsPrecision"] is not None else 'NULL',
                contractSize="\"" + str(record["contractSize"]) + "\"" if "contractSize" in record and record["contractSize"] is not None else 'NULL',
                exemode="\"" + str(record["exemode"]) + "\"" if "exemode" in record and record["exemode"] is not None else 'NULL',
                time="\"" + str(record["time"]) + "\"" if "time" in record and record["time"] is not None else 'NULL',
                expiration="\"" + str(record["expiration"]) + "\"" if "expiration" in record and record["expiration"] is not None else 'NULL',
                stopsLevel="\"" + str(record["stopsLevel"]) + "\"" if "stopsLevel" in record and record["stopsLevel"] is not None else 'NULL',
                precision="\"" + str(record["precision"]) + "\"" if "precision" in record and record["precision"] is not None else 'NULL',
                swapType="\"" + str(record["swapType"]) + "\"" if "swapType" in record and record["swapType"] is not None else 'NULL',
                stepRuleId="\"" + str(record["stepRuleId"]) + "\"" if "stepRuleId" in record and record["stepRuleId"] is not None else 'NULL',
                type="\"" + str(record["type"]) + "\"" if "type" in record and record["type"] is not None else 'NULL',
                instantMaxVolume="\"" + str(record["instantMaxVolume"]) + "\"" if "instantMaxVolume" in record and record["instantMaxVolume"] is not None else 'NULL',
                groupName="\"" + str(record["groupName"]) + "\"" if "groupName" in record and record["groupName"] is not None else 'NULL',
                description="\"" + str(record["description"]) + "\"" if "description" in record and record["description"] is not None else 'NULL',
                longOnly="\"" + str(record["longOnly"]) + "\"" if "longOnly" in record and record["longOnly"] is not None else 'NULL',
                trailingEnabled="\"" + str(record["trailingEnabled"]) + "\"" if "trailingEnabled" in record and record["trailingEnabled"] is not None else 'NULL',
                marginHedgedStrong="\"" + str(record["marginHedgedStrong"]) + "\"" if "marginHedgedStrong" in record and record["marginHedgedStrong"] is not None else 'NULL',
                swapEnable="\"" + str(record["swapEnable"]) + "\"" if "swapEnable" in record and record["swapEnable"] is not None else 'NULL',
                percentage="\"" + str(record["percentage"]) + "\"" if "percentage" in record and record["percentage"] is not None else 'NULL',
                bid="\"" + str(record["bid"]) + "\"" if "bid" in record and record["bid"] is not None else 'NULL',
                ask="\"" + str(record["ask"]) + "\"" if "ask" in record and record["ask"] is not None else 'NULL',
                high="\"" + str(record["high"]) + "\"" if "high" in record and record["high"] is not None else 'NULL',
                low="\"" + str(record["low"]) + "\"" if "low" in record and record["low"] is not None else 'NULL',
                lotMin="\"" + str(record["lotMin"]) + "\"" if "lotMin" in record and record["lotMin"] is not None else 'NULL',
                lotMax="\"" + str(record["lotMax"]) + "\"" if "lotMax" in record and record["lotMax"] is not None else 'NULL',
                lotStep="\"" + str(record["lotStep"]) + "\"" if "lotStep" in record and record["lotStep"] is not None else 'NULL',
                tickSize="\"" + str(record["tickSize"]) + "\"" if "tickSize" in record and record["tickSize"] is not None else 'NULL',
                tickValue="\"" + str(record["tickValue"]) + "\"" if "tickValue" in record and record["tickValue"] is not None else 'NULL',
                swapLong="\"" + str(record["swapLong"]) + "\"" if "swapLong" in record and record["swapLong"] is not None else 'NULL',
                swapShort="\"" + str(record["swapShort"]) + "\"" if "swapShort" in record and record["swapShort"] is not None else 'NULL',
                leverage="\"" + str(record["leverage"]) + "\"" if "leverage" in record and record["leverage"] is not None else 'NULL',
                spreadRaw="\"" + str(record["spreadRaw"]) + "\"" if "spreadRaw" in record and record["spreadRaw"] is not None else 'NULL',
                spreadTable="\"" + str(record["spreadTable"]) + "\"" if "spreadTable" in record and record["spreadTable"] is not None else 'NULL',
                starting="\"" + str(record["starting"]) + "\"" if "starting" in record and record["starting"] is not None else 'NULL',
                swap_rollover3days="\"" + str(record["swap_rollover3days"]) + "\"" if "swap_rollover3days" in record and record["swap_rollover3days"] is not None else 'NULL',
                marginMaintenance="\"" + str(record["marginMaintenance"]) + "\"" if "marginMaintenance" in record and record["marginMaintenance"] is not None else 'NULL',
                marginHedged="\"" + str(record["marginHedged"]) + "\"" if "marginHedged" in record and record["marginHedged"] is not None else 'NULL',
                initialMargin="\"" + str(record["initialMargin"]) + "\"" if "initialMargin" in record and record["initialMargin"] is not None else 'NULL',
                currencyPair="\"" + str(record["currencyPair"]) + "\"" if "currencyPair" in record and record["currencyPair"] is not None else 'NULL',
                shortSelling="\"" + str(record["shortSelling"]) + "\"" if "shortSelling" in record and record["shortSelling"] is not None else 'NULL',
                timeString="\"" + str(record["timeString"]) + "\"" if "timeString" in record and record["timeString"] is not None else 'NULL',
            )
        # logging.debug(query)
        # logging.getLogger().info(sqlite3.sqlite_version)
        ret = self.query(query)
        return ret

    def getMarketById(self, id=None):
        query = """SELECT * from {TABLE} WHERE id = '{ID}' ;""".format(TABLE=self.table, ID=id)

        df = self.getToDataFrame(query)
        if df is None or df.empty:
            return None
        return df

    def update(self, data):
        # Construction de la requete
        query = self.updateQuery(self.table, data)
        # Execution
        ret = self.query(query)
        return ret
