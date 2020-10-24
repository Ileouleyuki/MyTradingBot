#!/usr/bin/env python
# encoding: utf-8
###############################################################################
# LOGGING
###############################################################################

import sqlite3
import logging
import time

###############################################################################
# SQLiteHandler
###############################################################################

initial_sql = """CREATE TABLE IF NOT EXISTS {TABLE}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    TimeStampUtc TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    Source TEXT,
                    LogLevel INT,
                    LogLevelName TEXT,
                    Message TEXT,
                    Args TEXT,
                    Module TEXT,
                    FuncName TEXT,
                    LineNo INT,
                    Exception TEXT,
                    Process INT,
                    Thread TEXT,
                    ThreadName TEXT
               )"""

insertion_sql = """INSERT INTO {TABLE}(
                    Source,
                    LogLevel,
                    LogLevelName,
                    Message,
                    Args,
                    Module,
                    FuncName,
                    LineNo,
                    Exception,
                    Process,
                    Thread,
                    ThreadName
               )
               VALUES (
                    '%(name)s',
                    %(levelno)d,
                    '%(levelname)s',
                    "%(msg)s",
                    '%(args)s',
                    '%(module)s',
                    '%(funcName)s',
                    %(lineno)d,
                    '%(exc_text)s',
                    %(process)d,
                    '%(thread)s',
                    '%(threadName)s'
               );
               """


class SQLiteHandler(logging.Handler):
    """
    Gestionnaire de journalisation thread-safe pour SQLite.
    """

    def __init__(self, db='app.db', table='log'):
        """Initialisation Objet"""
        logging.Handler.__init__(self)
        self.db = db
        self.table = table
        conn = sqlite3.connect(self.db)
        conn.execute(initial_sql.format(TABLE=self.table))
        conn.commit()

    def format_time(self, record):
        """
        Formatage TimeStamp
        """
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):
        self.format(record)
        # self.format_time(record)
        print(record.msg)
        if record.exc_info:  # Pour exceptions
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            record.exc_text = record.exc_text.replace("'", '"')  # Remplacement des quotes provoqaunt une erreur
        else:
            record.exc_text = ""

        # Insert the log record
        sql = insertion_sql.format(TABLE=self.table) % record.__dict__
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()  # pas efficace, mais espérons-le thread-safe

###############################################################################
# SQLiteUrlHandler
###############################################################################


initial_url_sql = """CREATE TABLE IF NOT EXISTS {TABLE}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    TimeStampUtc TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                    ip TEXT,
                    user TEXT,
                    userId TEXT,
                    method TEXT,
                    scheme TEXT,
                    path TEXT,
                    api INTEGER DEFAULT 0,
                    status TEXT
               )"""

insertion_url_sql = """INSERT INTO {TABLE}(
                    ip,
                    user,
                    userId,
                    method,
                    scheme,
                    path,
                    status,
                    api
               )
               VALUES (
                    '{ip}',
                    '{user}',
                    '{userId}',
                    '{method}',
                    '{scheme}',
                    '{path}',
                    '{status}',
                    '{api}'
               );
               """


class SQLiteUrlHandler(logging.Handler):
    """
    Gestionnaire de journalisation thread-safe pour SQLite (Observateur)
    """

    def __init__(self, db='app.db', table='log'):
        """Initialisation Objet"""
        logging.Handler.__init__(self)
        self.db = db
        self.table = table
        conn = sqlite3.connect(self.db)
        conn.execute(initial_url_sql.format(TABLE=self.table))
        conn.commit()

    def format_time(self, record):
        """
        Formatage TimeStamp
        """
        record.dbtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

    def emit(self, record):

        # Split du message
        x = record.msg.split(" :: ")
        # Construction Requete
        sql = insertion_url_sql.format(
            TABLE=self.table,
            ip=x[0],
            user=x[1],
            userId=x[2],
            method=x[3],
            scheme=x[4],
            path=x[5],
            status=x[6],
            api=x[7]
        )
        # Insertion Requete
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()  # pas efficace, mais espérons-le thread-safe

        """
        self.format(record)
        self.format_time(record)
        if record.exc_info:  # Pour exceptions
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
            record.exc_text = record.exc_text.replace("'", '"')  # Remplacement des quotes provoqaunt une erreur
        else:
            record.exc_text = ""

        # Insert the log record
        sql = insertion_url_sql.format(TABLE=self.table) % record.__dict__
        conn = sqlite3.connect(self.db)
        conn.execute(sql)
        conn.commit()  # pas efficace, mais espérons-le thread-safe
        """
