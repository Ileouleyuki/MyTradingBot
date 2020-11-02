#!/usr/bin/env python
# encoding: utf-8

class AppException(Exception):
    """Erreur pour signaler une erreur gérér par le Script"""
    pass


class MarketClosedException(Exception):
    """Erreur pour signaler que le marché est actuellement fermé"""
    pass


class EventOnMarketException(Exception):
    """Erreur pour signaler qu'un evemenent eco arrive ou est passé"""
    pass


class NotInSessionTradingException(Exception):
    """Erreur pour signaler que nous ne sommes pas dans la Session de Trading"""
    pass


class NotSafeToTradeException(Exception):
    """Erreur pour signaler qu'il n'est pas sûr de trader"""
    pass


class StrategyException(Exception):
    """Erreur pour signaler les erreurs lié à la Stretegie"""
    pass


class DataNullException(Exception):
    """Erreur pour signaler que les prix sont inexploitables"""

# XTB API Exceptions


class UnreachableException(Exception):
    """Erreur pour signaler que le distinataire est Injoignaible"""
    pass


class NotLoggedException(Exception):
    """Erreur pour signaler une erreur de connexion avec le Broker"""
    pass


class TransactionRejected(Exception):
    """Erreur pour signaler un probleme de Transaction"""
    pass
