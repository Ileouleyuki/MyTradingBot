#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# CONFIGURATION
######################################################################################################
# Description : Interaction avec la Configuration en JSON
# Date de Creation : 06/05/2020
######################################################################################################
# Globales
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from functools import reduce
import operator

DEFAULT_CONFIGURATION_PATH = os.path.realpath('.') + os.sep + "config" + os.sep + "config.json"
CONFIGURATION_ROOT = "trading_mate_root"

# FIXME Property should be of type JSON byt it requires typing to accepts recursive types
Property = Any
ConfigDict = Dict[str, Property]
CredentialDict = Dict[str, str]


class Configuration(object):

    config: ConfigDict

    def __init__(self, dictionary: ConfigDict):
        if not isinstance(dictionary, dict):
            raise ValueError("L'Arguement doit etre un Dict")
        self.config = self._parse_raw_config(dictionary)

    @staticmethod
    def from_filepath(filepath=None):
        filepath = filepath if filepath else DEFAULT_CONFIGURATION_PATH
        # Verification existance du Fichier
        if not os.path.isfile(filepath):
            raise Exception("Le fichier de Configuration n'existe pas : {}".format(filepath))
        # Ouverture du Fichier
        return Configuration(json.load(open(filepath)))

    def json(self):
        return self.config

    def _find_property(self, fields: List[str]):
        if CONFIGURATION_ROOT in fields:
            return self.config
        if type(fields) is not list or len(fields) < 1:
            raise ValueError("Impossible de trouver la propriété {} dans la configuration".format(fields))
        value = self.config[fields[0]]
        for f in fields[1:]:
            value = value[f]
        return value

    def getFromConfig(self, mapList):
        return reduce(operator.getitem, mapList, self.config)

    def setInConfig(self, mapList, value):
        self.getFromConfig(mapList[:-1])[mapList[-1]] = value

    def _set_property(self, fields: List[str], value):
        if CONFIGURATION_ROOT in fields:
            return self.config
        if type(fields) is not list or len(fields) < 1:
            raise ValueError("Impossible de trouver la propriété {} dans la configuration".format(fields))
        # Modification de la valeur
        self.setInConfig(fields, value)
        # Sauvegarde
        with open(DEFAULT_CONFIGURATION_PATH, 'w') as json_file:
            json.dump(self.config, json_file, indent=4, sort_keys=True)
            json_file.close()

    def _parse_raw_config(self, config_dict: ConfigDict):
        config_copy = config_dict
        for key, value in config_copy.items():
            if type(value) is dict:
                config_dict[key] = self._parse_raw_config(value)
            elif type(value) is list:
                for i in range(len(value)):
                    config_dict[key][i] = (
                        self._replace_placeholders(config_dict[key][i])
                        if type(config_dict[key][i]) is str
                        else config_dict[key][i]
                    )
            elif type(value) is str:
                config_dict[key] = self._replace_placeholders(config_dict[key])
        return config_dict

    def _replace_placeholders(self, string: str):
        string = string.replace("{home}", str(Path.home()))
        string = string.replace(
            "{timestamp}",
            datetime.now().isoformat().replace(":", "_").replace(".", "_"),
        )
        return string

    def get_raw_config(self):
        return self._find_property([CONFIGURATION_ROOT])

    ######################################################################################################
    # GENERALE
    ######################################################################################################
    def get_spin_interval(self):
        return self._find_property(["spin_interval"])

    def set_spin_interval(self, value):
        self._set_property(["spin_interval"], value)

    ######################################################################################################
    # TIME
    ######################################################################################################

    def get_time_zone(self):
        return self._find_property(["time", "time_zone"])

    def set_time_zone(self, value):
        return self._set_property(["time", "time_zone"], value)

    def get_hour_start(self):
        return self._find_property(["time", "hour_start"])

    def set_hour_start(self, value):
        return self._set_property(["time", "hour_start"], value)

    def get_hour_end(self):
        return self._find_property(["time", "hour_end"])

    def set_hour_end(self, value):
        return self._set_property(["time", "hour_end"], value)

    ######################################################################################################
    # BROKER
    ######################################################################################################

    def get_filepathCredentials(self):
        return self._find_property(["broker", "filepathCredentials"])

    def set_filepathCredentials(self, value):
        return self._set_property(["broker", "filepathCredentials"], value)

    def get_use_demo_account(self):
        return self._find_property(["broker", "use_demo_account"])

    def get_type_account(self):
        return 'DEMO' if self.get_use_demo_account() is True else 'REEL'

    def set_use_demo_account(self, value):
        return self._set_property(["broker", "use_demo_account"], value)

    def get_credentials_filepath(self):
        return self._find_property(
            ["broker", "filepathCredentials"]
        )

    def get_credentials(self) -> CredentialDict:
        with Path(self.get_credentials_filepath()).open(mode="r") as f:
            return json.load(f)

    ######################################################################################################
    # STRATEGIES
    ######################################################################################################

    def get_active_strategy(self):
        return self._find_property(["strategies", "active"])

    def get_param_strategy(self, name):
        return self._find_property(["strategies", name])

    def get_values_strategy(self):
        return self._find_property(["strategies", "values"])
