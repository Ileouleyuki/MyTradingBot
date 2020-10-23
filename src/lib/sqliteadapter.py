#!/usr/bin/env python
# encoding: utf-8
######################################################################################################
# Adapteur de Connexion SQLITE
######################################################################################################
######################################################################################################
# Description : Modèle d'interaction générique à utiliser comme classe parent pour les models.
# Auteur : Julien DENIS
######################################################################################################
import sqlite3
import os
import pandas as pd

from core.Exceptions import SqliteAdapterException

######################################################################################################
# Class
######################################################################################################


class SqliteAdapter:
    # -----------------------------------------------------------------------------------------------
    def __init__(self, filepath=None):
        """
        Initialisation de l'objet
        """
        if filepath is not None:
            self.dbfilename = filepath
            if os.path.exists(self.dbfilename) is False:
                raise FileNotFoundError("Le fichier de BDD n'existe pas : {}".format(self.dbfilename))
        else:
            self.dbfilename = ":memory"

        # Enregistrement du PATH en variable private
        self.conn = None
        self.cursor = None
        self.open()

    # -----------------------------------------------------------------------------------------------
    def open(self):
        """
        Ouverture de la connection SQLITE
        """
        try:
            self.conn = sqlite3.connect(self.dbfilename)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise SqliteAdapterException("[SQLITE] = Erreur de connection à la BDD : " + str(e))

    # -----------------------------------------------------------------------------------------------
    def close(self):
        """
        Fermeture de la connection SQLITE
        """
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
    # -----------------------------------------------------------------------------------------------

    def __enter__(self):
        return self

    # -----------------------------------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # -----------------------------------------------------------------------------------------------

    def query(self, sql):
        """
        Execute une requete
        """
        try:
            self.open()  # On ouvre
            ret = self.cursor.execute(sql)  # On execute
            nbRow = ret.rowcount
            self.conn.commit()
            if nbRow > 0:
                return True
            else:
                return False
        except Exception as err:
            raise SqliteAdapterException("[SQLITE] - Échec de la requête SQL : \n{}\nERREUR : {}".format(sql, str(err)))

    # -----------------------------------------------------------------------------------------------

    def get(self, sql, limit=None):
        """
        Execute une requete de selection et renvoi un dict
        """
        try:
            self.open()  # On ouvre
            self.cursor.execute(sql)  # On execute
            rows = self.cursor.fetchall()  # On extrait
            if len(rows) == 0:
                data = None
            else:
                data = dict(zip([c[0] for c in self.cursor.description], rows[0]))
            if limit is not None and isinstance(limit, int) is True:
                rows = {k: data[k] for k in list(data.keys())[:limit]}  # On limite
            return data  # On convertit en dict
        except Exception as err:
            raise SqliteAdapterException(
                "[SQLITE] - Échec de la requête SQL de Selection : \n{}\nERREUR : {}".format(sql, str(err))
            )

    # -----------------------------------------------------------------------------------------------

    def getToDataFrame(self, sql, limit=None):
        """
        Execute une requete de selection
        """
        try:
            self.open()  # On ouvre
            # fetch data
            df = pd.read_sql_query(sql, self.conn)
            if limit is not None:
                return df.tail(limit)
            else:
                return df
        except Exception as err:
            raise SqliteAdapterException(
                "[SQLITE] - Impossible de Recuperer les données dans un DataFrame : \n{}\nERREUR : {}".format(sql, str(err))
            )
    # -----------------------------------------------------------------------------------------------

    def vacuum(self):
        """
        VACUUM la base de données pour supprimer toutes les données inutiles
        """
        try:
            self.open()
            ret = self.query("VACUUM")
            self.close()
            return ret
        except Exception as err:
            raise SqliteAdapterException("[SQLITE] - Echec de la maintenance : {}".format(str(err)))

    # -----------------------------------------------------------------------------------------------

    def get_tables(self):
        """
        Liste les tables
        """
        self.open()
        ret = self.get("SELECT name FROM sqlite_master;")
        return ret

    # -----------------------------------------------------------------------------------------------

    def tblExists(self, table='sqlite_sequence'):
        """
        Verifie si la table existe
        """
        self.open()
        ret = self.get("SELECT name FROM sqlite_master where name = '{table}'".format(table=table))
        if ret is not None:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------------------

    def drop_table(self, table):
        """
        Suppression d'une table
        """
        sql = """DROP TABLE IF EXISTS {TABLE}""".format(TABLE=table)
        ret = self.query(sql)
        return ret

    # -----------------------------------------------------------------------------------------------

    def count(self, table):
        ret = self.get("""SELECT COUNT(*) AS TOTAL FROM {TABLE}""".format(TABLE=table))["TOTAL"]
        return ret

    # -----------------------------------------------------------------------------------------------

    def is_unique(self, table, field, value):
        """
        Verifie si la valeur est deja presente
        """
        sql = """SELECT COUNT(*) as "TOTAL" FROM {TABLE} WHERE {FIELD}='{VALUE}'""".format(TABLE=table, FIELD=field, VALUE=value)
        ret = self.getToDataFrame(sql).to_dict("Record")
        return False if int(ret[0]["TOTAL"]) > 0 else True

    """
    ## -------------------------------------------------------------------------------------------------------------------------------
    ## Requete de selection sur la BDD mais retourne 1 resultat
    #  @param sql, Requete SQL.
    ## -------------------------------------------------------------------------------------------------------------------------------
    def getSelectSQLToDict(self, sql):
        try:
            self.open() # -- On ouvre
            self.cursor.execute(sql)
            # fetch data
            return self.cursor.fetchone()
        except Exception as e:
            logging.error("BDD SqLite (SELECT) =" +  str(e))
            return None
    ## -------------------------------------------------------------------------------------------------------------------------------
    ## Requete de selection sur la BDD mais retourne 1 resultat
    #  @param sql, Requete SQL.
    ## -------------------------------------------------------------------------------------------------------------------------------
    def getSelectSQLToDataFrame(self, sql, limit=None):
        try:
            self.open() # -- On ouvre
            # fetch data
            df = pd.read_sql_query(sql, self.conn)
            if limit is not None:
                return df.tail(limit)
            else:
                return df
        except Exception as e:
            logging.error("BDD SqLite (SELECT) =" +  str(e))
            return pd.DataFrame()
    ## -------------------------------------------------------------------------------------------------------------------------------
    ## Execution du simple requete (SELECT, UPDATE, INSERT, DELETE, ...)
    #  @param sql, Requete SQL.
    ## -------------------------------------------------------------------------------------------------------------------------------
    def getExecuteSQL(self, sql):
        try:
            self.open() # -- On ouvre
            ret = self.cursor.execute(sql) # -- On execute
            nbRow = ret.rowcount
            self.conn.commit()
            if nbRow  > 0:
                return True
            else:
                return False
        except Exception as e:
            logging.error("BDD SqLite (EXEC) =" +  str(e))
            return False
    ## -------------------------------------------------------------------------------------------------------------------------------
    ## Execution du simple requete (DROP, ...)
    #  @param sql, Requete SQL.
    ## -------------------------------------------------------------------------------------------------------------------------------
    def getExecuteQuerySQL(self, sql):
        try:
            self.open() # -- On ouvre
            ret = self.cursor.execute(sql) # -- On execute
            nbRow = ret.rowcount
            self.conn.commit()
            return True
        except Exception as e:
            logging.error("BDD SqLite (EXEC) =" +  str(e))
            return False
    ## -------------------------------------------------------------------------------------------------------------------------------
    ## Requete de mise à jour (UPDATE) sur la BDD
    #  @param table The name of the database's table to query from.
    #  @param columns The string of columns, comma-separated, to fetch.
    #  @param condition la chaine de condition WHERE
    #  @param id Optionally, a limit of items to fetch.
    ## -------------------------------------------------------------------------------------------------------------------------------
    def update(self,table,columns,data,id):
        value = "\"" + str(data) + "\"" if  data is not None else 'NULL'
        self.open()
        sql = "UPDATE {0} SET {1} = {2},updatedAt = strftime('%Y-%m-%d %H-%M-%S','now') WHERE id = '{3}'".format(table,columns,value,id)
        ret = self.getExecuteSQL(sql)
        self.close()
        return ret
    """
