#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# UTILISATEURS
######################################################################################################
# Description : Modele interaction avec Utilisateurs
# Auteur : ileouleyuki
# Version : V1
# Date de Creation : 18/03/2020
######################################################################################################
import logging
from lib.sqliteadapter import SqliteAdapter
from models.AuthFailedLoginModel import AuthFailedLoginModel
from core.Config import cfg
from core.Crypt import Crypt
# Logger
logger = logging.getLogger(cfg._LOG_ACTIVITY_NAME)

######################################################################################################
# Requetes SQL
######################################################################################################
initial_sql = """CREATE TABLE IF NOT EXISTS {TABLE}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                display TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT,
                last_connect_at TIMESTAMP(6),
                created_at TEXT DEFAULT (datetime('now','localtime')),
                updated_at TIMESTAMP(6),
                session TEXT
            )"""
######################################################################################################
# Class AuthUsersModel
######################################################################################################


class AuthUsersModel(SqliteAdapter):

    table: str = None

    def __init__(self):
        # Recuperation du path du fichier
        filename = cfg._BDD_PATH
        # Initialisation objet parent
        super().__init__(filename)
        # Definition de la table
        self.table = "mtb_auth_users"
        # Creation de la table
        if not self.tblExists(table=self.table):
            logger.info("Table {} inexistante >> Creation".format(self.table))
            query = initial_sql.format(TABLE=self.table)
            self.query(query)
            # Ajouter utilisateur par default
            logger.info("Ajout utilisateur par default")
            self.insertUser(data={
                'username': "admin",
                'password': Crypt.encode(cfg._APP_SECRET_KEY, 'admin'),
                'display': "Administrateur",
                'role': 'ADMIN',
            })

    ##################################################################################################
    # USERS
    ##################################################################################################
    def getAllUsers(self, Limit=None):

        query = """SELECT {TBL_USERS}.*,
            last_failed_login,
            COALESCE(failed_login_attempts, 0) as failed_login_attempts
            from {TBL_USERS}
            left JOIN {TBL_FAIL} ON {TBL_USERS}.username = {TBL_FAIL}.username;""".format(
                TBL_USERS=self.table, TBL_FAIL=AuthFailedLoginModel().table
            )
        df = self.getToDataFrame(query, Limit)
        if df is None or df.empty:
            return None
        return df.to_dict("Record")

    def is_unique_username(self, value):
        return self.is_unique(self.table_users, "username", value)

    def updateUser(self, data):
        # Construction de la requete
        query = """UPDATE {TABLE} SET """.format(TABLE=self.table)
        fields = list()
        for key, value in data.items():
            if key.lower() == "id":
                continue
            if key.lower() == "csrftoken":
                continue
            if value is None or len(value) == 0:
                continue
            fields.append("{FIELD} = '{VALUE}' ".format(FIELD=key, VALUE=value))

        # Jointure de la chaine de caractere
        query += ", ".join(map(str, fields))
        # Ajout de la condition de mise à jour
        query += " WHERE id = {ID}".format(ID=data["id"])
        # Execution
        ret = self.query(query)
        return ret

    def insertUser(self, data):
        # Extraction col and values
        values = list()
        columns = list()
        for key, value in data.items():
            if key.lower() == "csrftoken":
                continue
            if value is None or len(value) == 0:
                continue
            columns.append(key)
            values.append(value)

        cols = '( ' + ', '.join(map(str, columns)) + ' )'
        values = '( "' + '", "'.join(map(str, values)) + '" )'
        # Construction de la requete
        query = "INSERT INTO {TABLE} {columns} values {values};".format(TABLE=self.table, columns=cols, values=values)
        # Execution
        ret = self.query(query)
        return ret

    def deleteUser(self, data):
        query = """ DELETE FROM {TABLE} where id='{ID}';""".format(TABLE=self.table, ID=data["id"])
        ret = self.query(query)
        return ret

    def getUserByUsername(self, username):
        query = """ SELECT username, password, role, display from {TABLE} where username='{USERNAME}';""".format(
            TABLE=self.table,
            USERNAME=username
        )
        result = self.get(query, None)
        if result is None:
            return None
        return result

    def getUserById(self, id):
        query = """ SELECT username, password, role, display from {TABLE} where id={ID};""".format(
            TABLE=self.table,
            ID=id
        )
        result = self.get(query, None)
        if result is None:
            return None
        return result

    def updateLastConn(self, username):
        query = """UPDATE {TABLE}
                SET last_connect_at = strftime('%Y-%m-%d %H:%M:%S','now', 'localtime')
                WHERE username='{USERNAME}';""".format(
                TABLE=self.table,
                USERNAME=username
            )
        # Execution
        ret = self.query(query)
        return ret

    def updateIdSession(self, username, session):
        query = """UPDATE {TABLE}
                SET session = "{SESSION}"
                WHERE username='{USERNAME}';""".format(
                TABLE=self.table,
                USERNAME=username,
                SESSION=session
            )
        # Execution
        ret = self.query(query)
        return ret
