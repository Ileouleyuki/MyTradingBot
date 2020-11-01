#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# BOT
######################################################################################################
# Description : Le Bot de Trading
# Date de Creation : 20/05/2020
######################################################################################################
# Globale
import os
import time
import locale
import platform

COLUMNS, ROWS = 115, 25
VERSION = "1.0.0"

# ######################################################################################################
# Bot
# ######################################################################################################


class Bot:

    def __init__(self):
        pass

    def setup_logging(self):
        """
        Configuration du Logger Bot
        """
        pass

    def start(self):
        """
        Démarre la boucle principale de RobotTrader
        - Traiter les marchés à partir de la source du marché
        - Attendre le temps d'attente configuré
        - Recommencer
        """
        while True:
            print('test')
            time.sleep(1.0)

######################################################################################################
# Main
######################################################################################################


if __name__ == "__main__":
    # Redefinit le locale pour les dates
    if platform.system() == 'Linux':
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    else:
        locale.setlocale(locale.LC_TIME, "")
    # Purge de la console
    os.system('cls' if os.name == 'nt' else 'clear')
    # Demarrage du Bot
    print(" >>>\033[36m LANCEMENT DU BOT\033[0m")
    try:
        Bot().start()
    except KeyboardInterrupt:  # Ctrl-C
        print(("").ljust(COLUMNS, "-"))
        print("\033[31mInterruption Utilisateur : Ctrl-C\033[0m")
    except SystemExit:  # sys.exit()
        print(("").ljust(COLUMNS, "-"))
        print("\033[31mLe Programme a quitté de maniere inattendue\033[0m")
