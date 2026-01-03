# -*- coding: utf-8 -*-
"""
Utility
"""
import os
import sqlite3
import pyodbc
from rotatelogger import RotateLogger


def sql_failed():
    pass

class SQLiteUtils:
    base = os.path.dirname(__file__)
    def __init__(self,db='qcdata.db3'):
        self.connstr = os.path.join(self.base, db)
        self.logger = RotateLogger('SQL Lite',
                                   os.path.join(self.base, db + '_' +'log.txt'),
                                   10000000, 9, level='INFO')
    
    def fetch_one(self, query, *args):
        """
        execute select query, get one result
        """
        val = sql_failed
        try:
            conn = sqlite3.connect(self.connstr)
            cursor = conn.execute(query, args)
            val = cursor.fetchone()
        except sqlite3.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val

    def fetch_all(self, query, *args):
        """
        execute select query, get all result
        """
        val = sql_failed
        try:
            conn = sqlite3.connect(self.connstr)
            cursor = conn.execute(query, args)
            val = cursor.fetchall()
        except sqlite3.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val
    
    def commit(self, query, *args):
        """
        execute insert, update, delete query
        return False if failed
        """
        val = False
        try:
            conn = sqlite3.connect(self.connstr)
            conn.execute(query, args)
            conn.commit()
            val = True
        except sqlite3.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val

    def commit_many(self, query, data):
        """
        execute bulk insert query
        return False if failed
        """
        val = False
        try:
            conn = sqlite3.connect(self.connstr)
            cur = conn.cursor()
            cur.executemany(query, data)
            conn.commit()
            val = True
        except sqlite3.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val 


class SQLUtils:
    base = os.path.dirname(__file__)
    def __init__(self):
        self.connstr = ('DRIVER={SQL Server Native Client 11.0}; '
                       'SERVER=10.115.50.91; DATABASE=UC2_Vinmec; '
                       'UID=biorad; PWD=pkXDdUb8G6sC')
        self.logger = RotateLogger('SQL Server',
                                   os.path.join(self.base, 'dblog.txt'),
                                   10000000, 9, level='INFO')
        
    def fetch_one(self, query, *args):
        """
        execute select query, get one result
        """
        val = sql_failed
        try:
            conn = pyodbc.connect(self.connstr)
            cursor = conn.execute(query, *args)
            val = cursor.fetchone()
        except pyodbc.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val

    def fetch_all(self, query, *args):
        """
        execute select query, get all result
        """
        val = sql_failed
        try:
            conn = pyodbc.connect(self.connstr)
            cursor = conn.execute(query, *args)
            val = cursor.fetchall()
        except pyodbc.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val

    def commit(self, query, *args):
        """
        execute insert, update, delete query
        return False if failed
        """
        val = False
        try:
            conn = pyodbc.connect(self.connstr)
            conn.execute(query, *args)
            conn.commit()
            val = True
        except pyodbc.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val

    def commit_many(self, query, data):
        """
        execute bulk insert query
        return False if failed
        """
        val = False
        try:
            conn = pyodbc.connect(self.connstr)
            cur = conn.cursor()
            cur.executemany(query, data)
            conn.commit()
            val = True
        except pyodbc.Error:
            self.logger.exception('...')
        else:
            try:
                conn.close()
            except NameError:
                pass
        return val
