#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# DASHBOARD
######################################################################################################
# Description : Aide aux calculs de performance de Trading
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import logging
import datetime
import pandas as pd
# Perso
from core.Config import cfg

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)


class DashBoard(object):
    """
    Permet de calculer des Statistiques sur les performances de Trading
    """
    def __init__(self, orders):
        self._end = None
        self._start = None
        self._period = None
        self._orders = orders
        pass

    def init(self, period):
        """Filtrage des Ordres"""
        self._period = period
        # >> QUOTIDIEN
        if period.upper() == 'DAILY':
            end = datetime.datetime.utcnow()
            start = datetime.datetime.utcnow()
        # >> HEBDOMADAIRE
        elif period.upper() == 'WEEKLY':
            end = datetime.datetime.utcnow()
            start = datetime.datetime.utcnow() - datetime.timedelta(days=datetime.datetime.utcnow().weekday())
        # >> MENSUEL
        elif period.upper() == 'MONTHLY':
            end = datetime.datetime.utcnow()
            start = "{ANNEE}-{MOIS}-01".format(
                ANNEE=datetime.datetime.now().strftime("%Y"),
                MOIS=int(datetime.datetime.now().strftime("%m"))
                # DAY=datetime.datetime.now().strftime("%d")
            )
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
        # >> ANNUEL
        elif period.upper() == 'YEAR':
            end = datetime.datetime.utcnow()
            start = "{ANNEE}-01-01".format(
                ANNEE=datetime.datetime.now().strftime("%Y")
                # MOIS=int(datetime.datetime.now().strftime("%m")),
                # DAY=datetime.datetime.now().strftime("%d")
            )
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
        # >> ?????
        else:
            # Purge des Ordres
            self._orders.truncate(before=-1, after=-1)

        # Formatage des Dates de Bornage
        self._end = end.replace(hour=23, minute=59, second=59, microsecond=0)
        self._start = start.replace(hour=0, minute=0, second=0, microsecond=0)

        logger.info("[DASHBOARD] {:<12} : {}".format("Date DEBUT", self._start.strftime('%a %d %b %Y %H:%M:%S')))
        logger.info("[DASHBOARD] {:<12} : {}".format("Date FIN", self._end.strftime('%a %d %b %Y %H:%M:%S')))
        end = int(self._end.timestamp() * 1000)
        start = int(self._start.timestamp() * 1000)

        # Filtrage des Ordres
        self._orders = self._orders[((self._orders['open_time'] > start) & (self._orders['open_time'] < end))]

    def period(self):
        """Retourne des precision sur la periode"""
        if self._period.upper() == 'DAILY':
            return datetime.datetime.now().strftime('%a %d %b %Y')
        elif self._period.upper() == 'WEEKLY':
            return datetime.datetime.now().strftime('S%V')
        elif self._period.upper() == 'MONTHLY':
            return datetime.datetime.now().strftime('%b')
        elif self._period.upper() == 'YEAR':
            return datetime.datetime.now().strftime('%Y')
        else:
            return 'INCONNU'

    def start(self):
        return self._start.strftime('%a %d %b %Y %H:%M:%S')

    def end(self):
        return self._end.strftime('%a %d %b %Y %H:%M:%S')

    # ------------------------------------------------------------
    # GP
    # ------------------------------------------------------------

    def gp_total(self):
        """Somme Total"""
        logging.info("gp_total")
        if len(self._orders) == 0:
            return 0
        return round(self._orders['profit'].sum(), 2)  # NOQA # isort:skip

    def evalu(self):
        """Evaluation"""
        tmp = self.gp_total()
        if tmp == 0:
            return 'NEUTRE'
        elif tmp > 0:
            return 'COOL'
        elif tmp < 0:
            return 'NOTCOOL'
        else:
            return ''

    def gp_lose(self):
        """Somme des Gains"""
        if len(self._orders) == 0:
            return 0
        return round(self._orders[self._orders.profit > 0]["profit"].sum(), 2)  # NOQA # isort:skip

    def gp_wins(self):
        """Somme des Pertes"""
        if len(self._orders) == 0:
            return 0
        return round(self._orders[self._orders.profit < 0]["profit"].sum(), 2)  # NOQA # isort:skip

    def gp_ratio_wins(self):
        """Ratio Gagnant"""
        if len(self._orders) == 0:
            return 0
        nb_trade_win = self.gp_wins()
        nb_trade_lose = self.gp_lose()

        return round( nb_trade_win * 100/ (nb_trade_win + nb_trade_lose))  # NOQA # isort:skip

    def gp_ratio_lose(self):
        """Ratio Perdant"""
        if len(self._orders) == 0:
            return 0
        nb_trade_win = self.gp_wins()
        nb_trade_lose = self.gp_lose()

        return round( nb_trade_lose * 100/ (nb_trade_win + nb_trade_lose))  # NOQA # isort:skip

    # ------------------------------------------------------------
    # TRADE
    # ------------------------------------------------------------

    def trade_total(self):
        """Calcul le nombre de Trade"""
        if len(self._orders) == 0:
            return 0
        return len(self._orders)  # NOQA # isort:skip

    def trade_wins(self):
        """Calcul le nombre de Trade Gagnant"""
        if len(self._orders) == 0:
            return 0
        return len(self._orders[self._orders.profit > 0])  # NOQA # isort:skip

    def trade_lose(self):
        """Calcul le nombre de Trade Perdant"""
        if len(self._orders) == 0:
            return 0
        return len(self._orders[self._orders.profit < 0])  # NOQA # isort:skip

    def trade_ratio_wins(self):
        """Ratio Gagnant"""
        if len(self._orders) == 0:
            return 0
        nb_trade_win = self.trade_wins()
        nb_trade_lose = self.trade_lose()

        return round( nb_trade_win * 100/ (nb_trade_win + nb_trade_lose))  # NOQA # isort:skip

    def trade_ratio_lose(self):
        """Ratio Perdant"""
        if len(self._orders) == 0:
            return 0
        nb_trade_win = self.trade_wins()
        nb_trade_lose = self.trade_lose()

        return round( nb_trade_lose * 100/ (nb_trade_win + nb_trade_lose))  # NOQA # isort:skip

    # ------------------------------------------------------------
    # GRAPHIQUE
    # ------------------------------------------------------------

    def getPerfTradeByDay(self):
        # Creation du DataFrame Vide
        idx = pd.date_range(self._start.strftime('%Y-%m-%d'), self._end.strftime('%Y-%m-%d'), freq='D').strftime('%Y-%m-%d')  # Week : W-MON
        # Determination du jour
        self._orders['open_time_day'] = pd.to_datetime(
            self._orders['open_time'] / 1000,
            unit='s',
            utc=True
        ).dt.strftime("%Y-%m-%d").astype(str)
        # Groupement de Trade GAGNANT par Jour
        df_nb_trd_win_by_day = self._orders[(
            self._orders['profit'] > 0
        )].groupby('open_time_day')['id'].agg(['count']).astype(int).rename(index=str, columns={"count": "NB_TRD_WIN"})
        # Groupement de Trade PERDANT par Jour
        df_nb_trd_lose_by_day = self._orders[(
            self._orders['profit'] < 0
        )].groupby('open_time_day')['id'].agg(['count']).astype(int).rename(index=str, columns={"count": "NB_TRD_LOSE"})
        # Concatenation des DataFrames
        final = pd.concat([
            df_nb_trd_win_by_day,
            df_nb_trd_lose_by_day
        ], axis=1, sort=True).fillna(0).astype(int)
        # Reindexation pour ajout dates manquantes
        final = final.reindex(idx, fill_value=0).reset_index()
        # Formatage des Dates
        final['index'] = pd.to_datetime(final["index"]).dt.strftime("%a %d %b %Y")
        return {
            'labels': final['index'].values.tolist(),
            'nb_trd_win': final.NB_TRD_WIN.values.tolist(),
            'nb_trd_lose': final.NB_TRD_LOSE.values.tolist(),
        }

    def getPerfGpByDay(self):
        # Creation du DataFrame Vide
        idx = pd.date_range(self._start.strftime('%Y-%m-%d'), self._end.strftime('%Y-%m-%d'), freq='D').strftime('%Y-%m-%d')  # Week : W-MON
        # Determination du jour
        self._orders['open_time_day'] = pd.to_datetime(
                self._orders['open_time'] / 1000,
                unit='s',
                utc=True
        ).dt.strftime("%Y-%m-%d").astype(str)

        # Groupement de Trade GAGNANT par Jour
        df_gp_trd_win_by_day = self._orders[(
            self._orders['profit'] > 0
        )].groupby('open_time_day')['profit'].agg(['sum']).rename(index=str, columns={"sum": "SUM_GP_WIN"})
        # Groupement de Trade PERDANT par Jour
        df_gp_trd_lose_by_day = self._orders[(
            self._orders['profit'] < 0
        )].groupby('open_time_day')['profit'].agg(['sum']).rename(index=str, columns={"sum": "SUM_GP_LOSE"})
        # concatenation des DataFrame
        final = pd.concat([
            df_gp_trd_win_by_day,
            df_gp_trd_lose_by_day
        ], axis=1, sort=True).fillna(0).round(2)
        # Reindexation pour ajout dates manquantes
        final = final.reindex(idx, fill_value=0).reset_index()
        # Formatage des Dates
        final['index'] = pd.to_datetime(final["index"]).dt.strftime("%a %d %b %Y")

        return {
            'labels': final['index'].values.tolist(),
            'nb_gp_win': final.SUM_GP_WIN.values.tolist(),
            'nb_gp_lose': final.SUM_GP_LOSE.values.tolist(),
        }

    @staticmethod
    def perf(history, group=None):
        """Performance"""
        # Definition du pareamtrage par default
        if group is None:
            group = "open_time_day"  # Group_Open_Week, Group_Open_Month
        elif group == "WEEK":
            group = "open_time_week"  # Group_Open_Date, Group_Open_Month
        elif group == "MONTH":
            group = "open_time_month"  # Group_Open_Date, Group_Open_Month
        # ---------------------------------------------------------
        # Creation du DataFrame Vide
        """
        df_final = pd.DataFrame({
            "index": pd.date_range(
                str(datetime.datetime.now().year) + '-01-01', str(datetime.datetime.now().year) + '-12-31',
                freq='D'  # Week : W-MON
            )
        })
        # df_final.index = pd.to_datetime(df_final['index'], format='%Y-%m-%d')
        """
        # ---------------------------------------------------------
        # Determination du Nombre de Trade TOTAL
        df_nb_trd_by_day = history[(
            history['type'].isin(["P", "G"])
            )].groupby(group)['type'].agg(['count']).rename(index=str, columns={"count": "NB_TRD"})
        # Determination du Nombre de Trade GAGNANT
        df_nb_trd_wins_by_day = history[(
            history['type'] == "G"
            )].groupby(group)['type'].agg(['count']).rename(index=str, columns={"count": "NB_TRD_WIN"})
        # Determination du Nombre de Trade PERDANT
        df_nb_trd_lose_by_day = history[(
            history['type'] == "P"
            )].groupby(group)['type'].agg(['count']).rename(index=str, columns={"count": "NB_TRD_LOSE"})
        # Determination de la Somme de GAIN
        df_sum_trd_wins_by_day = history[(
            history['type'] == "G"
            )].groupby(group)['profit'].agg(['sum']).rename(index=str, columns={"sum": "SUM_GAIN"})
        # Determination de la Somme de PERTE
        df_sum_trd_lose_by_day = history[(
            history['type'] == "P"
            )].groupby(group)['profit'].agg(['sum']).rename(index=str, columns={"sum": "SUM_PERTE"})
        # Determination de la Somme des GAINS + PERTE
        df_sum_trd_by_day = history[(
            history['type'].isin(["P", "G"])
            )].groupby(group)['profit'].agg(['sum']).rename(index=str, columns={"sum": "SUM_TOTAL"})
        # Determination de la Somme de COMMISSION
        df_sum_trd_commssion_by_day = history[(
            history['type'].isin(["P", "G"])
            )].groupby(group)['commission'].agg(['sum']).rename(index=str, columns={"sum": "SUM_COMISS"})
        # ---------------------------------------------------------
        # Concatenation
        final = pd.concat([
            df_nb_trd_by_day,
            df_nb_trd_wins_by_day,
            df_nb_trd_lose_by_day,
            df_sum_trd_wins_by_day,
            df_sum_trd_lose_by_day,
            df_sum_trd_by_day,
            df_sum_trd_commssion_by_day
        ], axis=1, sort=True).fillna(0)
        # ---------------------------------------------------------
        # Determination du Ratio GAIN
        final['RATIO_WIN'] = round((final['NB_TRD_WIN'] * 100) / final['NB_TRD'], 2)
        # Determination du Ratio PERTE
        final['RATIO_LOSE'] = round((final['NB_TRD_LOSE'] * 100) / final['NB_TRD'], 2)
        # Ratio Gain/pertes
        final['RATIO_GP'] = round((final['SUM_TOTAL'] / final['SUM_PERTE']), 2)
        # Evolution du Capital
        final['TMP_CAPITAL'] = 1000
        final.loc[:, 'EVOL_GP'] = final.loc[:, 'SUM_TOTAL'].cumsum()
        final.loc[:, 'EVOL_COM'] = final.loc[:, 'SUM_COMISS'].cumsum()
        final['CAPITAL'] = final['TMP_CAPITAL'] + final['EVOL_GP'] + final['EVOL_COM']
        final.drop(['EVOL_GP', 'TMP_CAPITAL', 'EVOL_COM'], axis=1, inplace=True)
        final.reset_index(inplace=True)
        return final

    """
    ## Pourcentage de trade GAGNANT
    grp_JRL_TRADING.insert(loc=2, column='PERC_TRD_GAGNANT', value=0)
    grp_JRL_TRADING['PERC_TRD_GAGNANT'] =
        round((grp_JRL_TRADING['NB_TRD_WIN'] * 100) / (grp_JRL_TRADING['NB_TRD_WIN'] + grp_JRL_TRADING['NB_TRD_LOST']),2)
    ## Niveau de Trading (Trade GAGNANT)
    grp_JRL_TRADING.insert(loc=3, column='NIVEAU_TRADING_TRD_WIN', value=0)
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['PERC_TRD_GAGNANT'] < 50)),'NIVEAU_TRADING_TRD_WIN'] = 1
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['PERC_TRD_GAGNANT'] >= 50) &(grp_JRL_TRADING['PERC_TRD_GAGNANT'] < 60) ),'NIVEAU_TRADING_TRD_WIN'] = 2
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['PERC_TRD_GAGNANT'] >= 60) &(grp_JRL_TRADING['PERC_TRD_GAGNANT'] < 70) ),'NIVEAU_TRADING_TRD_WIN'] = 3
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['PERC_TRD_GAGNANT'] >= 70) &(grp_JRL_TRADING['PERC_TRD_GAGNANT'] < 80) ),'NIVEAU_TRADING_TRD_WIN'] = 4
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['PERC_TRD_GAGNANT'] >= 80)),'NIVEAU_TRADING_TRD_WIN'] = 5
    ## Ratio Gain/pertes
    grp_JRL_TRADING['RATIO_GP'] = round(grp_JRL_TRADING['TOTAL_GAIN']  / grp_JRL_TRADING['TOTAL_PERTE'] , 2)
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['TOTAL_PERTE'] == 0)),'RATIO_GP'] = 100
    ## Niveau de Trading (RATIO GP)
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['RATIO_GP'] < 1.5)),'NIVEAU_TRADING_RATIO_GP'] = 1
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['RATIO_GP'] >= 1.5) &(grp_JRL_TRADING['RATIO_GP'] < 2) ),'NIVEAU_TRADING_RATIO_GP'] = 2
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['RATIO_GP'] >= 2) &(grp_JRL_TRADING['RATIO_GP'] < 3) ),'NIVEAU_TRADING_RATIO_GP'] = 3
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['RATIO_GP'] >= 3) &(grp_JRL_TRADING['RATIO_GP'] < 4) ),'NIVEAU_TRADING_RATIO_GP'] = 4
    grp_JRL_TRADING.loc[((grp_JRL_TRADING['RATIO_GP'] >= 4)),'NIVEAU_TRADING_RATIO_GP'] = 5
    ## GAIN/PERTE par Session
    grp_JRL_TRADING['GAIN_PERTE'] = round(grp_JRL_TRADING['TOTAL_GAIN'] +  grp_JRL_TRADING['TOTAL_PERTE'] , 2)
    #
    # # EVOLUTION du Capital
    grp_JRL_TRADING['TMP_CAPITAL'] = 10000
    grp_JRL_TRADING.loc[:, 'EVOL_GP'] = grp_JRL_TRADING.loc[:,'GAIN_PERTE'].cumsum()
    grp_JRL_TRADING['CAPITAL'] = grp_JRL_TRADING['TMP_CAPITAL'] + grp_JRL_TRADING['EVOL_GP']
    grp_JRL_TRADING.drop(['EVOL_GP','TMP_CAPITAL'],axis=1,inplace=True)
    ## Rentabilite
    grp_JRL_TRADING['RENTABILITE'] = round((((grp_JRL_TRADING['CAPITAL'] - 10000) / 10000) * 100 ),2)
    """

    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
    # ==================================================================================================================
