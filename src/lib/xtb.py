#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# Adapteur de Connexion au broker XTB
######################################################################################################
######################################################################################################
# Description : Modèle d'interaction avec l'API du Broker XTB
# Auteur : Julien DENIS
######################################################################################################

import json
import logging
import time
import pandas as pd
import numpy as np
import datetime
from websocket import create_connection
from websocket._exceptions import WebSocketConnectionClosedException
from core.Utils import Utils
# from ...utils import Utils
# from ...configuration import Configuration
from lib.exceptions import NotLoggedException, TransactionRejected, UnreachableException
# from ...interfaces import Position


LOGIN_TIMEOUT = 120
MAX_TIME_INTERVAL = 0.200
PERIOD = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "M30": 30,
    "H1": 60,
    "H4": 240,
    "DAILY": 1440,
    "WEEKLY": 10080,
    "MONTHLY": 43200
}


def _get_data(command, **parameters):
    data = {
        "command": command,
    }
    if parameters:
        data['arguments'] = {}
        for (key, value) in parameters.items():
            data['arguments'][key] = value
    return data

# ===================================================================================================================
# CommandFailed
# ===================================================================================================================


class CommandFailed(Exception):
    pass

# ===================================================================================================================
# SocketError
# ===================================================================================================================


class SocketError(Exception):
    pass

# ===================================================================================================================
# Class XtbClient
# ===================================================================================================================


class XtbClient(object):
    """
    Classe permettant d'interagir avec l'API XTB
    """

    def __init__(self, account_id, password, type=['DEMO', 'REEL']):
        """Initialisation Objet"""
        logging.debug("[XTB] Initialisation Interface XTB...")

        # Enregistrement des parametres
        self._acc_type = type
        self._login_data = (
            account_id,
            password,
        )
        self.ws = None
        self._time_last_request = time.time() - MAX_TIME_INTERVAL
        self.status = "NOT_LOGGED"

    def _login_decorator(self, func, *args, **kwargs):
        if self.status == "NOT_LOGGED":
            raise NotLoggedException("[XTB] - Non loggué")
        try:
            return func(*args, **kwargs)
        except SocketError:
            self.login(self._login_data[0], self._login_data[1])
            return func(*args, **kwargs)
        except Exception:
            self.login(self._login_data[0], self._login_data[1])
            return func(*args, **kwargs)
        except ConnectionAbortedError as CnxAbtErr:
            raise NotLoggedException("[XTB] - Erreur de Connexion : {}".format(CnxAbtErr))

    def _send_command(self, dict_data):
        """
        Envoi d'une commande à l'API
        """
        time_interval = time.time() - self._time_last_request
        if time_interval < MAX_TIME_INTERVAL:
            time.sleep(MAX_TIME_INTERVAL - time_interval)
        try:
            self.ws.send(json.dumps(dict_data))
            time.sleep(0.5)
            response = self.ws.recv()
        except WebSocketConnectionClosedException:
            raise UnreachableException("[XTB] - Probleme Socket")
        except OSError:
            raise UnreachableException("[XTB] - Probleme Socket")
        self._time_last_request = time.time()
        res = json.loads(response)
        # Traitement des Codes Erreurs
        if res['status'] is False:
            if res['errorCode'] == 'BE005':
                raise NotLoggedException("[XTB] - Echec Identification")
            logging.error("-----------------------------")
            logging.error("[XTB] - {}".format(res['errorCode']))
            logging.error(res['errorDescr'])
            logging.error("-----------------------------")
            return None
        if 'returnData' in res.keys():
            return res['returnData']

    def _send_command_with_check(self, dict_data):
        """
        Envoi d'une commande à l'API avec verification de connexion
        """
        return self._login_decorator(self._send_command, dict_data)

    def login(self):
        """
        Commande de Connexion
        """
        params = _get_data("login", userId=self._login_data[0], password=self._login_data[1])
        url = "wss://ws.xtb.com/{}".format(self._acc_type.lower())
        if Utils.isConnected():
            self.ws = create_connection(url)
            response = self._send_command(params)
            # self._login_data = (user_id, password)
            self.status = "LOGGED"
            logging.debug("[XTB] - Connexion")
            return response
        else:
            raise UnreachableException("[XTB] - Injoignable")
        return None

    def logout(self):
        """
        Commande de deconnexion
        """
        if self.status == "NOT_LOGGED":
            return None
        data = _get_data("logout")
        response = self._send_command(data)
        self.status = "NOT_LOGGED"
        logging.debug("[XTB] Deconnexion")
        return response

    def get_server_time(self):
        """
        Commande : getServerTime
        Retourne la date du Serveur en UTC
        """
        params = _get_data("getServerTime")
        data = self._send_command_with_check(params)
        # return datetime.datetime.fromtimestamp(int(data['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        return datetime.datetime.utcfromtimestamp(int(data['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    def get_timeframes(self):
        """
        Retourne les TimeFrame Disponibles
        """
        return [*PERIOD]

    def get_events(self):
        """
        Commande : getCalendar
        Retourne la date du Serveur en UTC
        """
        params = _get_data("getCalendar")
        data = self._send_command_with_check(params)
        df_events = pd.json_normalize(data)
        # Index sur le Datetime
        df_events.index = pd.to_datetime(df_events['time'] / 1000, unit='s', utc=True)
        df_events.impact = pd.to_numeric(df_events.impact)
        """
        data_path_transac = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_events.csv'
        df_events.to_csv(data_path_transac, sep=';', encoding='utf-8-sig')
        import os
        os.startfile(data_path_transac)
        """
        return df_events

    def get_all_markets(self):
        """
        Commande : getAllSymbols
        Retourne tous les marchés chez XTB
        """
        params = _get_data("getAllSymbols")
        data = self._send_command_with_check(params)
        df_data = pd.json_normalize(data)
        return df_data

    def get_prices(self, symbol, period, start: int = None, end: int = None, ticks: int = 0):
        """
        Commande : getChartRangeRequest
        Recuperation des prix
        """
        # Definition des parametres
        args = {}
        args['period'] = PERIOD[period]
        args['symbol'] = symbol
        if start is None and end is None:
            end = datetime.datetime.utcnow()
            start = end - datetime.timedelta(days=100 if period not in ['M1', 'M5'] else 10)
            args['end'] = end.timestamp() * 1000
            args['start'] = start.timestamp() * 1000
        else:
            args['end'] = end * 1000
            args['start'] = start * 1000
        params = _get_data("getChartRangeRequest", info=args)
        # Execution de la requete
        data = self._send_command_with_check(params)
        # Verification des données
        if data is None or len(data['rateInfos']) == 0:
            return pd.DataFrame()
        # Transformation en DataFrame
        digits = int(data['digits'])
        df_data = pd.json_normalize(data['rateInfos'])
        df_data['open'] = df_data['open'] / 10**digits
        df_data['close'] = df_data['open'] + (df_data['close'] / 10**digits)
        df_data['high'] = df_data['open'] + (df_data['high'] / 10**digits)
        df_data['low'] = df_data['open'] + (df_data['low'] / 10**digits)
        df_data.rename(index=str, columns={'vol': 'volume'}, inplace=True)
        df_data.volume = df_data.volume.astype(np.int64)
        df_data = df_data.round({'open': digits, 'close': digits, 'high': digits, 'low': digits})
        df_data.index = pd.to_datetime(df_data['ctm'] / 1000, unit='s', utc=True)
        df_data.index = df_data.index.tz_convert(self.config.get_time_zone())
        df_data.index.name = "Datetime"
        df_data.drop(['ctmString', 'ctm'], 1, inplace=True)
        df_data = df_data.round(digits)
        # Filtrage
        if ticks > 0:
            df_data = df_data.tail(ticks)
        return df_data

    def get_market_info(self, market):
        """
        Commande : getSymbol
        Recuperation des infos du marché
        """
        # Definition des parametres
        params = _get_data("getSymbol", symbol=market.symbol)
        # Execution de la requete
        data = self._send_command_with_check(params)
        if data is None:
            return market
        # Transformation en DataFrame
        market.ask = data['ask']
        market.bid = data['bid']
        market.precision = int(data['precision'])
        market.pipsPrecision = int(data['pipsPrecision'])
        market.lotMin = data['lotMin']
        market.lotMax = data['lotMax']
        market.lotStep = data['lotStep']
        market.sizeOf1Lot = data['contractSize']
        market.spreadRaw = data['spreadRaw']
        market.stopsLevel = data['stopsLevel']
        market.swapLong = data["swapLong"]
        market.swapShort = data["swapShort"]
        market.leverage = data['leverage']
        # market.marginRate = data['marginRate']
        return market

    def getCurrentUserData(self):
        """
        Renvoie un tuple (solde, dépôt) pour le compte utilisé
        - Renvoie ** (Aucun, Aucun) ** si une erreur se produit autrement (solde, dépôt)
        """
        # Definition des parametres
        params = _get_data("getCurrentUserData")
        # Execution de la requete
        data = self._send_command_with_check(params)
        # Verification des données
        if data is None or len(data) == 0:
            return pd.DataFrame()
        # Transformation en DataFrame
        df_current = pd.json_normalize(data)
        return df_current

    def getInfoPortFolio(self):
        """
        Renvoi un dict avec les infos financieres du compte
        """
        # Definition des parametres
        params = _get_data("getMarginLevel")
        # Execution de la requete
        data = self._send_command_with_check(params)
        if data is not None:
            return data
        return None

    def get_account_balances(self):
        """
        Renvoie un tuple (solde, dépôt) pour le compte utilisé
        - Renvoie ** (Aucun, Aucun) ** si une erreur se produit autrement (solde, dépôt)
        """
        data = self.getInfoPortFolio()
        if data is not None:
            balance = data["balance"]
            deposit = data["margin"]
            return balance, deposit
        return None, None

    def get_account_used_perc(self):
        """
        Récupérer le pourcentage du solde disponible actuellement utilisé
        - Renvoie le pourcentage du compte utilisé sur le montant total disponible
        """
        balance, deposit = self.get_account_balances()
        if balance is None or deposit is None:
            return None
        return Utils.percentage(deposit, balance)

    def get_open_positions(self, openedOnly: bool = True):
        """
        Commande : getSymbol
        Recuperation des infos du marché
        """
        # Definition des parametres
        params = _get_data("getTrades", openedOnly=openedOnly)
        # Execution de la requete
        data = self._send_command_with_check(params)
        return self.formatTrades(data)

    def get_trading_hours(self, symbol):
        """
        Commande : getTradingHours
        Recuperation des infos d'ouverture du marché
        """
        # Definition des parametres
        params = _get_data("getTradingHours", symbols=symbol)
        # Execution de la requete
        data = self._send_command_with_check(params)
        if data is None:
            return None
        return data

    def is_market_open(self, symbol):
        """
        Verification que le marché est Ouvert
        """
        data = self.get_trading_hours(symbol)
        for tradingHour in data[0]['trading']:
            if (datetime.date.today().weekday() + 1) == tradingHour['day']:
                start = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 00)) + \
                        datetime.timedelta(milliseconds=int(tradingHour['fromT']))
                end = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 00)) + \
                    datetime.timedelta(milliseconds=int(tradingHour['toT']))
                if start < datetime.datetime.utcnow() < end:
                    return True
                else:
                    return False
        return False
        # nowStr = str(now_time.strftime('%H:%M'))

    def trade_transaction_status(self, order_id):
        """
        tradeTransactionStatus command
        """
        data = _get_data("tradeTransactionStatus", order=order_id)
        return self._send_command_with_check(data)

    def open_trade(self, pos=None):
        """
        open trade transaction
        """
        # Definition des parametres
        info = {
            'cmd': 2 if pos.direction == 'ACHAT' else 3,
            'symbol': pos.symbol,
            'type': 0,
            'volume': pos.size,
            'price': pos.level,
            'sl': pos.sl,
            'tp': pos.tp,
            "customComment": pos.comment,
        }
        params = _get_data("tradeTransaction", tradeTransInfo=info)
        # Execution de la requete
        response = self._send_command_with_check(params)
        # Verification du passage de l'ordre
        time.sleep(2)
        if response is None:
            raise TransactionRejected("[XTB] - Le passage de l'ordre de trading n'a pas renvoyé de numero")
        status = self.trade_transaction_status(response['order'])
        if status['requestStatus'] != 3:
            raise TransactionRejected(status)
        return response['order']

    def formatTrades(self, data):
        """
        Formatage des Trades renvoyé par le Broker
        """
        if len(data) > 0:
            # Transformation en DataFrame
            df_trades = pd.json_normalize(data)
            # Calcul du Delai
            if len(df_trades.close_time.value_counts()) > 0:
                df_trades['delai'] = (df_trades['close_time'] - df_trades['open_time']) / 1000
            else:
                df_trades['delai'] = (datetime.datetime.now().timestamp() - df_trades['open_time']) / 1000
            df_trades['delai'] = df_trades['delai'].apply(Utils.formatSeconds)
            # Calcul open_time_day
            df_trades['open_time_day'] = pd.to_datetime(
                df_trades['open_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%Y-%m-%d").astype(str)
            # Calcul open_time_month
            df_trades['open_time_month'] = pd.to_datetime(
                df_trades['open_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%Y-%m").astype(str)
            # Calcul open_time_week
            df_trades['open_time_week'] = pd.to_datetime(
                df_trades['open_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%Y-S%W").astype(str)

            # Calcul close_time_day
            df_trades['close_time_day'] = pd.to_datetime(
                df_trades['close_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%Y-%m-%d").astype(str)
            # Calcul close_time_month
            df_trades['close_time_month'] = pd.to_datetime(
                df_trades['close_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%d").astype(str)
            # Calcul close_time_week
            df_trades['close_time_week'] = pd.to_datetime(
                df_trades['close_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%d").astype(str)

            # TypeGain
            df_trades['type'] = np.where(
                (
                    (df_trades["profit"] > 0)
                ), "G", "P"
            )
            # Suppression des colonnes inutiles
            df_trades.drop([
                'cmd',
                'digits',
                'offset',
                'order2',
                'position',
                'nominalValue',
                # 'timestamp',
                'taxes',
                'open_timeString',
                'close_timeString',
                'expiration',
                'expirationString'
            ], axis=1, inplace=True)
            # Reordonnencement
            df_trades = df_trades.reindex(
                columns=[
                    'symbol',
                    'order',
                    'open_time_fmt',
                    'open_time_day',
                    'open_time_month',
                    'open_time_week',
                    'open_time',
                    'close_time_fmt',
                    'close_time_day',
                    'close_time_month',
                    'close_time_week',
                    'close_time',
                    'delai',
                    'open_price',
                    'close_price',
                    'spread',
                    'timestamp',
                    'volume',
                    'sl',
                    'tp',
                    'margin_rate',
                    'commission',
                    'profit',
                    'type',
                    'storage',
                    'closed',
                    'comment',
                    'customComment'
                ])
            # Formatage des Dates
            df_trades['open_time_fmt'] = pd.to_datetime(
                df_trades['open_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%a %d %b %Y (S%W) %H:%M:%S").astype(str)
            df_trades['close_time_fmt'] = pd.to_datetime(
                df_trades['close_time'] / 1000,
                unit='s',
                utc=True
            ).dt.strftime("%a %d %b %Y (S%W) %H:%M:%S").astype(str)
            # Determine direction
            df_trades['direction'] = np.where(df_trades['volume'] > 0, 'ACHAT', 'VENTE')
            # data_path_transac = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_trades.csv'
            # df_trades.to_csv(data_path_transac, sep=';', encoding='utf-8-sig')
            # import os
            # os.startfile(data_path_transac)
            return df_trades
        else:
            columns = [
                'symbol',
                'order',
                'open_time_fmt',
                'open_time_day',
                'open_time_month',
                'open_time_week',
                'open_time',
                'close_time_fmt',
                'close_time_day',
                'close_time_month',
                'close_time_week',
                'close_time',
                'delai',
                'open_price',
                'close_price',
                'spread',
                'volume',
                'sl',
                'tp',
                'margin_rate',
                'commission',
                'profit',
                'type',
                'storage',
                'closed',
                'comment',
                'customComment'
            ]
            return pd.DataFrame(columns=columns)

    def getTradesHistory(self, start: int = None, end: int = None):
        """
        Recuperation de l'Hoistorique des Trades
        """
        # Definition des parametres
        if start is None and end is None:
            end = datetime.date.utcnow()
            start = end - datetime.timedelta(days=5)
        else:
            end = datetime.datetime.fromtimestamp(end)
            start = datetime.datetime.fromtimestamp(start)
        logging.debug("[XTB] {:<12} : {}".format("Date DEBUT", start.strftime('%a %d %b %Y %H:%M:%S')))
        logging.debug("[XTB] {:<12} : {}".format("Date FIN", end.strftime('%a %d %b %Y %H:%M:%S')))
        logging.debug("[XTB] {:<12} : {}".format("Durée", end - start))

        params = _get_data("getTradesHistory", start=int(start.timestamp() * 1000), end=int(end.timestamp() * 1000))
        # Execution de la requete
        data = self._send_command_with_check(params)
        # DEBUG -- Sauvegarde CSV
        # df_orders = pd.json_normalize(data)
        # data_path_transac = 'orders.csv'
        # df_orders.to_csv(data_path_transac, sep=';', encoding='utf-8-sig')
        # Retour des données
        return data

    """
    def _close_trade_only(self, order_id):

            trade = self.trade_rec[order_id]
            self.LOGGER.debug(f"closing trade {order_id}")
            try:
                response = self.trade_transaction(
                    trade.symbol, 0, 2, trade.volume, order=trade.order_id,
                    price=trade.price)
            except CommandFailed as e:
                if e.err_code == 'BE51':  # order already closed
                    self.LOGGER.debug("BE51 error code noticed")
                    return 'BE51'
                else:
                    raise
            status = self.trade_transaction_status(
                response['order'])['requestStatus']
            self.LOGGER.debug(f"close_trade completed with status of {status}")
            if status != 3:
                raise TransactionRejected(status)
            return response

        def close_trade(self, trans):

            if isinstance(trans, Transaction):
                order_id = trans.order_id
            else:
                order_id = trans
            self.update_trades()
            return self._close_trade_only(order_id)

        def close_all_trades(self):

            self.update_trades()
            self.LOGGER.debug(f"closing {len(self.trade_rec)} trades")
            trade_ids = self.trade_rec.keys()
            for trade_id in trade_ids:
                self._close_trade_only(trade_id)
    """
