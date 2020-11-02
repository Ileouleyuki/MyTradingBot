#!/usr/bin/env python
# encoding: utf-8

from lib.configuration import Configuration
from lib.strategie.factory import StgyFactory

######################################################################################################
# DEV
######################################################################################################
if __name__ == '__main__':
    # Recuperation de la Configuration
    config = Configuration.from_filepath()
    # Recuperation de la Configuration
    # print(config.get_active_strategy())
    # print(config.get_param_strategy(name=config.get_active_strategy()))
    # print(config.get_values_strategy())

    # Creation de la Strategie
    stgyObj = StgyFactory("DEV").make()
    print(stgyObj.name)

    # Recuperation des prix
    stgyObj.fetch_data_prices(symbol='EURUSD', ut='H1')

    # Affichage des prix
    print(stgyObj.prices)
