#!/usr/bin/env python
# encoding: utf-8

from lib.configuration import Configuration


class Param(Configuration):

    def __init__(self):
        # Initialisation objet parent
        super().from_filepath()


######################################################################################################
# DEV
######################################################################################################
if __name__ == '__main__':
    # Recuperation du Fichier de Config
    config = Configuration.from_filepath()
    # Essai Lecture + Modification + Lecture (Propriété Existante)
    # print(config.get_spin_interval())
    # config.set_spin_interval("ESSAI2")
    # print(config.get_spin_interval())
    # Essai Lecture + Modification + Lecture (Propriété Inexistante)
    # print(config.get_time_zone())
    config.set_time_zone(True)
    print(config.get_time_zone())
