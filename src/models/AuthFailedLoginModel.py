#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# ECHEC CONNEXION
######################################################################################################
# Description : Modele interaction avec Echec de Connexion
# Auteur : ileouleyuki
######################################################################################################
import logging
import datetime
from lib.sqliteadapter import SqliteAdapter
from models.AuthIpBlockedModel import AuthIpBlockedModel
from core.Config import cfg

# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)
######################################################################################################
# Requetes SQL
######################################################################################################
initial_sql = """CREATE TABLE IF NOT EXISTS {TABLE}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    last_failed_login integer,
                    failed_login_attempts integer DEFAULT 0 NOT NULL,
                    UNIQUE(ip,username)
                )"""
######################################################################################################
# Class AuthFailedLoginModel
######################################################################################################


class AuthFailedLoginModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = "mtb_auth_failed_login"
        # Creation de la table
        if not self.tblExists(table=self.table):
            print("la table {} n'existe pas".format(self.table))
            query = initial_sql.format(TABLE=self.table)
            ret = self.query(query)
            print(ret)

    ##################################################################################################
    # FAILED LOGIN
    ##################################################################################################
    def getFailedLoginByUser(self, username):
        query = """ SELECT * FROM {TABLE} WHERE username ='{USERNAME}' LIMIT 1;""".format(
            TABLE=self.table,
            USERNAME=username
        )
        result = self.get(query, None)
        if result is None:
            return None
        return result

    def incrementFailedLogins(self, username, failedLogin, userIp):
        if failedLogin is not None:
            query = """UPDATE {TABLE} SET
                    -- last_failed_login = strftime('%Y-%m-%d %H-%M-%S','now'),
                    last_failed_login = '{DATENOW}',
                    failed_login_attempts = failed_login_attempts + 1
                    WHERE username ='{USERNAME}';""".format(
                TABLE=self.table,
                DATENOW=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                USERNAME=username
            )
        else:
            query = """ INSERT INTO {TABLE} (username, ip, last_failed_login, failed_login_attempts)
                    VALUES ('{USERNAME}', '{IP}', '{LAST_FAILED_LOGIN}', 1)""".format(
                TABLE=self.table,
                IP=userIp,
                LAST_FAILED_LOGIN=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                USERNAME=username
            )
        ret = self.query(query)
        return ret

    def resetFailedLogins(self, username):
        query = """
                UPDATE {TABLE} SET
                last_failed_login = NULL,
                failed_login_attempts = 0
                WHERE username = '{USERNAME}'""".format(
                    TABLE=self.table,
                    USERNAME=username
                )

        ret = self.query(query)
        return ret

    def handleIpFailedLogin(self, userIP, username):
        """
        Ajoute un nouvel enregistrement (s'il n'existe pas) à la table ip_failed_logins,
        Bloquer également l'adresse IP si le nombre de tentatives est dépassé
        """
        query = "SELECT ip, username FROM {TABLE} WHERE ip = '{IP}' ".format(
            TABLE=self.table,
            IP=userIP
        )
        result = self.get(query, None)
        count = len(result) if result is not None else 0
        # Bloque l'IP en cas d'échec de tentatives de connexion
        # avec différents login/mdp (> = 5) à partir de la même adresse IP
        if count >= 5:
            AuthIpBlockedModel().blockIP(userIP)
        else:
            # Vérifie si ip_failed_logins a déjà un enregistrement avec l'ip + username actuel
            # sinon, insérez-le.
            query = """ INSERT INTO {TABLE} (ip, username) VALUES ('{IP}', '{USERNAME}') ON CONFLICT(ip, username) DO NOTHING""".format(
                TABLE=self.table,
                IP=userIP,
                USERNAME=username,
            )
        ret = self.query(query)

        return ret
