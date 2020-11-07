#!/usr/bin/env python
# encoding: utf-8
import time
import logging
import datetime
import threading
import pytz
from random import randint
# from time import sleep
from core.Config import cfg
# Lib
from lib.logger import SQLiteHandler
from lib.configuration import Configuration
from lib.strategie.factory import StgyFactory

# Models
from models.MarketsModel import MarketsModel

VERSION = "1.0.0"
LOGGER = logging.getLogger(cfg._LOG_BOT_NAME)


class Bot():
    def __init__(self):
        """
        =============================================================
        Initialisation Objet
        =============================================================
        """
        self._t = None
        self._active = False
        self.sleep_time = 5
        self.pid = randint(0000, 9999)
        # Setup LOGGING
        if cfg._LOG_BOT is True:
            LOGGER = logging.getLogger(cfg._LOG_BOT_NAME)
            LOGGER.setLevel(logging.DEBUG if cfg._ENV[cfg._ENVIRONNEMENT]["DEBUG_MODE"] else logging.INFO)
            # sqlite handler
            sh = SQLiteHandler(db=cfg._LOG_BOT_BDD_PATH, table=cfg._LOG_BOT_TABLE)
            sh.setLevel(logging.DEBUG)
            logging.getLogger().addHandler(sh)

    @property
    def active(self):
        """Accesseur de l'etat du Thread"""
        return self._active

    def start(self):
        """
        =============================================================
        Activation du Robot
        =============================================================
        """
        LOGGER.warning("ACTIVATION DU ROBOT {}".format(VERSION))
        LOGGER.debug("PID {}".format(self.pid))
        self._active = True
        if self._t is None:
            self._t = threading.Timer(self.wait_for(), self._run)
            self._t.start()
        else:
            LOGGER.error("Le BOT est déjà actif")

    def _run(self):
        LOGGER.debug("Debut du Traitement")
        if self.is_in_session_trading() is True:
            self.work()
        else:
            self.update()
        # Reprise d'une boucle de monitoring du thread
        self._t = threading.Timer(self.wait_for(), self._run)
        self._t.start()

    def stop(self):
        """
        =============================================================
        Desactivation du Robot
        =============================================================
        """
        if self._t is not None:
            self._active = False
            self._t.cancel()
            self._t = None
            LOGGER.error('ARRET DU ROBOT')

    # =================================================================================
    #
    #  ██████╗  ██████╗ ████████╗
    #  ██╔══██╗██╔═══██╗╚══██╔══╝
    #  ██████╔╝██║   ██║   ██║
    #  ██╔══██╗██║   ██║   ██║
    #  ██████╔╝╚██████╔╝   ██║
    #  ╚═════╝  ╚═════╝    ╚═╝
    #
    # =================================================================================

    def work(self):
        """
        =============================================================
        Traitement lors des Session de Trading
        =============================================================
        """
        LOGGER.debug('GO GO GO ')

    # --------------------------------------------------------------------------------

    def update(self):
        """
        =============================================================
        Traitement en dehors des Session de Trading
        =============================================================
        """
        LOGGER.debug('TODO -- Update des Ordres + Marchés')
    # --------------------------------------------------------------------------------

    def process_before_iteration(self):
        """
        =============================================================
        Effectuer des operations avant de parcourir les marchés
        - Verification si on est dans une Session de Trading
        - Récupérez les positions ouvertes sur les marchés
        - Recuperer les evenements economique
        =============================================================
        """
        # Recuperation de la configuration pour iteration
        self.used_stgy = Configuration.from_filepath().get_active_strategy()
        self.params = Configuration.from_filepath().get_param_strategy(self.used_stgy)
        # Initialiser le Broker à partir de la classe Factory
        # La Factory permet de créer le Broker à partir du fichier de configuration
        # self.broker = BrokerFactory(self.config).make()

        # Initialiser la Stratégie à partir de la classe Factory
        # La Factory permet de créer la Strategie à partir du fichier de configuration
        LOGGER.info("Initialisation de la Strategie : {}".format(self.used_stgy))
        self.strategy = StgyFactory(self.used_stgy).make()

        # Reinitialisation des positions + events
        self.positions = None
        self.orders = None
        self.events = None

    # --------------------------------------------------------------------------------

    def process_markets(self):
        """
        =============================================================
        Traiter les marchés à partir de la source de marché configurée
        =============================================================
        """
        # Recuperation des Marchés à Trader
        markets_to_trade = MarketsModel().get_to_trade()
        if markets_to_trade is None or markets_to_trade.empty:
            raise StopIteration('Aucun marchés à trader')
        # Parcours des Marchés
        LOGGER.info("Il y a {} marché(s) à analyser".format(len(markets_to_trade)))
        LOGGER.info("Debut Iteration des Marchés")
        for idx, item in markets_to_trade.iterrows():
            self.process_market(market=item)
        raise StopIteration("Fin iteration des Marchés")

    # --------------------------------------------------------------------------------

    def safety_checks(self, market):
        """
        =============================================================
        Effectuer quelques contrôles de sécurité avant d'exécuter la stratégie sur le prochain marché
        Renvoi des exceptions spécifiques si le marché n'est pas sûr
        =============================================================
        """
        pass

    # --------------------------------------------------------------------------------

    def process_market(self, market):
        """
        =============================================================
        Faites tourner la stratégie sur le marché
        =============================================================
        """
        LOGGER.warning("MARCHE : {}".format(market['symbol']))
        # Verification de Sécurité
        LOGGER.info("Verification de Sécurité")
        self.safety_checks(market)
        LOGGER.info("Analyse strategique du marché")
        # Recuperation des prix
        self.strategy.run(symbol=market['symbol'], ut=self.params['main_ut'])

    # --------------------------------------------------------------------------------

    def is_in_session_trading(self):
        """
        =============================================================
        Verification que nous sommes dans la periode de Trading defini en Configuraton
        Renvoie Vrai si on y est, Faux dans le cas contraire
        =============================================================
        """
        # [DEBUG] - Activation pour dev du weekend
        # return True
        # Verification jour ouvrables
        if datetime.datetime.today().weekday() > 4:
            return False
        # Recuperation des parametres de Session de Trading
        hour_start = Configuration.from_filepath().get_hour_start()
        hour_end = Configuration.from_filepath().get_hour_end()
        # Initialisation du moment
        tz = pytz.timezone(Configuration.from_filepath().get_time_zone())
        now_time = datetime.datetime.now(tz=tz)
        nowStr = str(now_time.strftime('%H:%M'))
        # Periode de trading defini en configuration
        if hour_end < hour_start:
            return nowStr >= hour_start or nowStr <= hour_end
        return hour_start <= nowStr <= hour_end

    # --------------------------------------------------------------------------------

    def wait_for(self):
        """
        =============================================================
        Attendez la durée spécifiée en  fonctions des parametres
        de Sessions de Trading :
            - Si on DANS : spin_interval
            - Si on HORS : Determination du temps d'attente restant
              avant le debut de la prochaine Sessions
        =============================================================
        """
        # Recuperation en config des valeurs utiles
        spin_interval = Configuration.from_filepath().get_spin_interval().lower()

        # Determination du Nombre de Secondes pour le spin_interval
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        spin_interval_secs = int(spin_interval[:-1]) * seconds_per_unit[spin_interval[-1]]

        if self.is_in_session_trading() is True:
            secs = spin_interval_secs
        else:
            from_time = datetime.datetime.now()
            # Determination de la date de prochaine ouverture
            today_opening = datetime.datetime.strptime(
                from_time.strftime('%Y-%m-%d') + " " + Configuration.from_filepath().get_hour_start(), '%Y-%m-%d %H:%M'
            )
            # Si on a depassé Minuit
            if from_time < today_opening and from_time.weekday() < 5:
                nextMarketOpening = today_opening
            else:
                # Si on est lundi, on ajoute 1 jour
                if from_time.weekday() == 0:
                    nextMarketOpening = today_opening + datetime.timedelta(days=1)
                # -- Si on est mardi, on ajoute 1 jour
                if from_time.weekday() == 1:
                    nextMarketOpening = today_opening + datetime.timedelta(days=1)
                # -- Si on est mercredi, on ajoute 1 jour
                if from_time.weekday() == 2:
                    nextMarketOpening = today_opening + datetime.timedelta(days=1)
                # -- Si on est jeudi, on ajoute 1 jour
                if from_time.weekday() == 3:
                    nextMarketOpening = today_opening + datetime.timedelta(days=1)
                # -- Si on est vendredi, on ajoute 3 jours
                if from_time.weekday() == 4:
                    nextMarketOpening = today_opening + datetime.timedelta(days=3)
                # -- Si on est samedi, on ajoute 2 jours
                if from_time.weekday() == 5:
                    nextMarketOpening = today_opening + datetime.timedelta(days=2)
                # -- Si on est dimanche, on ajoute 1 jour
                if from_time.weekday() == 6:
                    nextMarketOpening = today_opening + datetime.timedelta(days=1)
            # Affichage en LOG
            LOGGER.info("Prochaine Session de Trading : " + nextMarketOpening.strftime('%a %d %b %Y %H:%M:%S'))
            LOGGER.debug("Date à comparer : " + from_time.strftime('%a %d %b %Y %H:%M:%S'))
            # Calcul du nombre de secondes à attendre
            secs = (nextMarketOpening - from_time).total_seconds()

        # Formatage du Nombre de Secondes
        mins, seconds = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)

        # Formatage de la chaine de caractere
        fmt_str = ""
        if days > 0:
            fmt_str += "{} jrs ".format(int(days))
        if hours > 0:
            fmt_str += "{} hrs ".format(int(hours))
        if mins > 0:
            fmt_str += "{} mins ".format(int(mins))
        if seconds > 0:
            fmt_str += "{} secs ".format(int(seconds))

        # Renvoi du nombre de Secondes
        LOGGER.info("Patientez {} ...".format(fmt_str.strip()))
        return secs


if __name__ == '__main__':
    m1 = Bot()
    m1.start()
    time.sleep(1)
    m1.start()
    time.sleep(5)
    print('STOP')
    m1.stop()
    print("FIN")
