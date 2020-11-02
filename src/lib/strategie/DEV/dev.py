#!/usr/bin/env python
# encoding: utf-8
from ..interface import StrategieInterface


class StrategieDev(StrategieInterface):
    """
    Classe definissant une Strategie pour le Developpement
    """

    def __init__(self):
        """
        ====================================================================
        Initialisation Objet
        ====================================================================
        """
        # Constructeur du Model
        super().__init__(name="DEV")
