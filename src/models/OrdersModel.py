#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# ORDERS
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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account TEXT,
                    context TEXT,
                    cmd	INTEGER,
                    orderOpen	INTEGER,
                    digits	INTEGER,
                    offset	INTEGER,
                    orderClose	INTEGER,
                    position	INTEGER,
                    symbol	TEXT,
                    comment	TEXT,
                    customComment	TEXT,
                    commission	REAL,
                    storage	REAL,
                    margin_rate	REAL,
                    close_price	REAL,
                    open_price	REAL,
                    nominalValue	TEXT,
                    profit	REAL,
                    volume	REAL,
                    sl	REAL,
                    tp	REAL,
                    closed	TEXT,
                    timestamp	TIMESTAMP(13),
                    spread	INTEGER,
                    taxes	REAL,
                    open_time	TIMESTAMP(13),
                    open_timeString	TEXT,
                    close_time	TIMESTAMP(13),
                    close_timeString	TEXT,
                    expiration	TEXT,
                    expirationString	TEXT,
                    created_at_utc TIMESTAMP(13) DEFAULT CURRENT_TIMESTAMP,
                    updated_at_utc TIMESTAMP(13),
                    UNIQUE(account, orderOpen)
                )"""
######################################################################################################
# Class OrdersModel
######################################################################################################


class OrdersModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = "mtb_orders"
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
        query = """SELECT
                id,
                symbol,
                -- orders.order,
                open_time,
                close_time,
                (close_time - open_time) as delai,
                open_price,
                close_price,
                volume,
                sl,
                tp,
                commission,
                profit,
                trim(coalesce(comment, '') || ' ' || customComment) as comment
                from {TABLE}""".format(
                    TABLE=self.table
                )
        df = self.getToDataFrame(query, Limit)
        return df

    def upsert(self, record, account, type):
        """
        Insertion d'un ordres. Si Existant, alors on met à jour
        """
        query = """INSERT INTO {TABLE} (
                    account,
                    context,
                    cmd,
                    orderOpen,
                    digits,
                    offset,
                    orderClose,
                    position,
                    symbol,
                    comment,
                    customComment,
                    commission,
                    storage,
                    margin_rate,
                    close_price,
                    open_price,
                    nominalValue,
                    profit,
                    volume,
                    sl,
                    tp,
                    closed,
                    timestamp,
                    spread,
                    taxes,
                    open_time,
                    open_timeString,
                    close_time,
                    close_timeString,
                    expiration,
                    expirationString

            ) VALUES (
                    {account},
                    {context},
                    {cmd},
                    {orderOpen},
                    {digits},
                    {offset},
                    {orderClose},
                    {position},
                    {symbol},
                    {comment},
                    {customComment},
                    {commission},
                    {storage},
                    {margin_rate},
                    {close_price},
                    {open_price},
                    {nominalValue},
                    {profit},
                    {volume},
                    {sl},
                    {tp},
                    {closed},
                    {timestamp},
                    {spread},
                    {taxes},
                    {open_time},
                    {open_timeString},
                    {close_time},
                    {close_timeString},
                    {expiration},
                    {expirationString}
            )
            ON CONFLICT (account,orderOpen) DO UPDATE SET
            symbol = {symbol},
            context = {context},
            cmd = {cmd},
            digits = {digits},
            offset = {offset},
            orderClose= {orderClose},
            position= {position},
            comment = {comment},
            customComment = {customComment},
            commission = {commission},
            storage = {storage},
            margin_rate = {margin_rate},
            close_price = {close_price},
            open_price = {open_price},
            nominalValue = {nominalValue},
            profit = {profit},
            volume = {volume},
            sl = {sl},
            tp = {tp},
            closed = {closed},
            timestamp = {timestamp},
            spread = {spread},
            taxes = {taxes},
            open_time = {open_time},
            open_timeString = {open_timeString},
            close_time = {close_time},
            close_timeString = {close_timeString},
            expiration = {expiration},
            expirationString = {expirationString},
            updated_at_utc = CURRENT_TIMESTAMP;
            """.format(
                TABLE=self.table,
                account="\"" + str(account) + "\"" if account is not None else 'NULL',
                context="\"" + str(type) + "\"" if type is not None else 'NULL',
                cmd="\"" + str(record["cmd"]) + "\"" if "cmd" in record and record["cmd"] is not None and record["cmd"] != "nan" else 'NULL',
                orderOpen="\"" + str(record["order"]) + "\"" if "order" in record and record["order"] is not None and record["order"] != "nan" else 'NULL',
                symbol="\"" + str(record["symbol"]) + "\"" if "symbol" in record and record["symbol"] is not None else 'NULL',
                digits="\"" + str(record["digits"]) + "\"" if "digits" in record and record["digits"] is not None and record["digits"] != "nan" else 'NULL',
                offset="\"" + str(record["offset"]) + "\"" if "offset" in record and record["offset"] is not None and record["offset"] != "nan" else 'NULL',
                orderClose="\"" + str(record["orderClose"]) + "\"" if "orderClose" in record and record["orderClose"] is not None and record["orderClose"] != "nan" else 'NULL',
                position="\"" + str(record["position"]) + "\"" if "position" in record and record["position"] is not None and record["position"] != "nan" else 'NULL',
                comment="\"" + str(record["comment"]) + "\"" if "comment" in record and record["comment"] is not None and record["comment"] != "nan" else 'NULL',
                customComment="\"" + str(record["customComment"]) + "\"" if "customComment" in record and record["customComment"] is not None and record["customComment"] != "nan" else 'NULL',
                commission="\"" + str(record["commission"]) + "\"" if "commission" in record and record["commission"] is not None and record["commission"] != "nan" else 'NULL',
                storage="\"" + str(record["storage"]) + "\"" if "storage" in record and record["storage"] is not None and record["storage"] != "nan" else 'NULL',
                margin_rate="\"" + str(record["margin_rate"]) + "\"" if "margin_rate" in record and record["margin_rate"] is not None and record["margin_rate"] != "nan" else 'NULL',
                close_price="\"" + str(record["close_price"]) + "\"" if "close_price" in record and record["close_price"] is not None and record["close_price"] != "nan" else 'NULL',
                open_price="\"" + str(record["open_price"]) + "\"" if "open_price" in record and record["open_price"] is not None and record["open_price"] != "nan" else 'NULL',
                nominalValue="\"" + str(record["nominalValue"]) + "\"" if "nominalValue" in record and record["nominalValue"] is not None and record["nominalValue"] != "nan" else 'NULL',
                profit="\"" + str(record["profit"]) + "\"" if "profit" in record and record["profit"] is not None and record["profit"] != "nan" else 'NULL',
                volume="\"" + str(record["volume"]) + "\"" if "volume" in record and record["volume"] is not None and record["volume"] != "nan" else 'NULL',
                sl="\"" + str(record["sl"]) + "\"" if "sl" in record and record["sl"] is not None and record["sl"] != "nan" else 'NULL',
                tp="\"" + str(record["tp"]) + "\"" if "tp" in record and record["tp"] is not None and record["tp"] != "nan" else 'NULL',
                closed="\"" + str(record["closed"]) + "\"" if "closed" in record and record["closed"] is not None and record["closed"] != "nan" else 'NULL',
                timestamp="\"" + str(record["timestamp"]) + "\"" if "timestamp" in record and record["timestamp"] is not None and record["timestamp"] != "nan" else 'NULL',
                spread="\"" + str(record["spread"]) + "\"" if "spread" in record and record["spread"] is not None and record["spread"] != "nan" else 'NULL',
                taxes="\"" + str(record["taxes"]) + "\"" if "taxes" in record and record["taxes"] is not None and record["taxes"] != "nan" else 'NULL',
                open_time="\"" + str(record["open_time"]) + "\"" if "open_time" in record and record["open_time"] is not None and record["open_time"] != "nan" else 'NULL',
                open_timeString="\"" + str(record["open_timeString"]) + "\"" if "open_timeString" in record and record["open_timeString"] is not None and record["open_timeString"] != "nan" else 'NULL',
                close_time="\"" + str(record["close_time"]) + "\"" if "close_time" in record and record["close_time"] is not None and record["close_time"] != "nan" else 'NULL',
                close_timeString="\"" + str(record["close_timeString"]) + "\"" if "close_timeString" in record and record["close_timeString"] is not None and record["close_timeString"] != "nan" else 'NULL',
                expiration="\"" + str(record["expiration"]) + "\"" if "expiration" in record and record["expiration"] is not None and record["expiration"] != "nan" else 'NULL',
                expirationString="\"" + str(record["expirationString"]) + "\"" if "expirationString" in record and record["expirationString"] is not None and record["expirationString"] != "nan" else 'NULL'
            )
        # logging.debug(query)
        # logging.getLogger().info(sqlite3.sqlite_version)
        ret = self.query(query)
        return ret
