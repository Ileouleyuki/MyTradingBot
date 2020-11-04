#!/usr/bin/env python
# encoding: utf-8
import logging
from threading import Timer
# from time import sleep
from core.Config import cfg
# Lib
from lib.logger import SQLiteHandler

VERSION = "1.0.0"
LOGGER = logging.getLogger(cfg._LOG_BOT_NAME)


class Bot(object):
    def __init__(self):
        self.sleep_time = 2
        # self.function = "query_db"
        self._t = None
        if cfg._LOG_BOT is True:
            LOGGER = logging.getLogger(cfg._LOG_BOT_NAME)
            LOGGER.setLevel(logging.DEBUG if cfg._ENV[cfg._ENVIRONNEMENT]["DEBUG_MODE"] else logging.INFO)
            # sqlite handler
            sh = SQLiteHandler(db=cfg._LOG_BOT_BDD_PATH, table=cfg._LOG_BOT_TABLE)
            sh.setLevel(logging.DEBUG)
            logging.getLogger(cfg._LOG_BOT_NAME).addHandler(sh)

    def start(self):
        LOGGER.info("Demarrage du Bot")
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        # self.function()
        self.runBot()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            LOGGER.info("Arret du Bot")
            self._t.cancel()
            self._t = None

    def runBot(self):
        # Initialisation du logger (Activité)
        LOGGER.info("IM QUERYING A DB")

    @property
    def state(self):
        if self._t is None:
            return 'STOP'
        else:
            return 'RUN'
