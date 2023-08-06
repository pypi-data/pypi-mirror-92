# -*- coding:utf-8 -*-
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A lightweight wrapper around MySQLdb.安装前准备：
1、sudo yum install mysql-devel python-devel python3-devel
2、sudo pip3 install mysqlclient== 1.4.6 DBUtils==1.3
3、DBUtils功能：https://www.cnblogs.com/oubo/archive/2011/08/12/2394554.html
"""

import copy
import MySQLdb.constants
import MySQLdb.converters
import MySQLdb.cursors

import logging
import time

MYSQL_HOST = 'localhost'
MYSQL_DB = 'spider'
MYSQL_USER = 'spider'
MYSQL_PASSWORD = 'spider'

class Connection(object):
    """A lightweight wrapper around MySQLdb DB-API connections.

    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage::

        db = database.Connection("localhost", "mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title

    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.

    We explicitly set the timezone to UTC and the character encoding to
    UTF-8 on all connections to avoid time zone and encoding errors.
    """
    def __init__(self, mysql_host = None, mysql_db = None, user = None, password = None, max_idle_time=7*3600):
        if mysql_host is None:
            self.host = MYSQL_HOST
        else:
            self.host = mysql_host
        if mysql_db is None:
            self.database = MYSQL_DB
        else:
            self.database = mysql_db
        if user is None:
            user = MYSQL_USER
        if password is None:
            password = MYSQL_PASSWORD
        self.max_idle_time = max_idle_time

        args = dict(conv=CONVERSIONS, use_unicode=True, charset="utf8",
                    db=self.database, init_command='SET time_zone = "+8:00"',
                    sql_mode="TRADITIONAL")
        if user is not None:
            args["user"] = user
        if password is not None:
            args["passwd"] = password

        # We accept a path to a MySQL socket file or a host(:port) string
        if "/" in self.host:
            args["unix_socket"] = host
        else:
            self.socket = None
            pair = self.host.split(":")
            if len(pair) == 2:
                args["host"] = pair[0]
                args["port"] = int(pair[1])
            else:
                args["host"] = self.host
                args["port"] = 3306

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        self.pool_con = None
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        logging.info('open')
        self.close()
        try:
           from DBUtils import PooledDB

           self.pool_con = PooledDB.PersistentDB(creator=MySQLdb, mincached=1, maxcached=10, maxshared=10,
               maxconnections=20, blocking=False, maxusage=500, **self._db_args)
        except:
           self._db = MySQLdb.connect(**self._db_args)
           self._db.autocommit(True)

    def iter(self, query, *parameters):
        """Returns an iterator for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(zip(column_names, row))
        finally:
            cursor.close()

    def query(self, query, *parameters):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters):
        """Returns the first row returned for the given query."""
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    # rowcount is a more reasonable default return value than lastrowid,
    # but for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()

        try:
            self._execute(cursor, query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def _ensure_connected(self):
        # Mysql by default closes client connections that are idle for
        # 8 hours, but the client library does not report this fact until
        # you try to perform a query and it fails.  Protect against this
        # case by preemptively closing and reopening the connection
        # if it has been idle for too long (7 hours by default).
        if (self._db is None or
            (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()
        #从连接池中取出连接
        if self.pool_con is not None:
            self._db = self.pool_con.connection()
            self._db.cursor().connection.autocommit(True)

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters):
        try:
            return cursor.execute(query, parameters)
        except OperationalError:
            logging.error("Error connecting to MySQL on %s", self.host)
            self.close()
            raise
        finally:
            cursor.close()


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


# Fix the access conversions to properly recognize unicode/binary
FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
FLAG = MySQLdb.constants.FLAG
CONVERSIONS = copy.copy(MySQLdb.converters.conversions)

field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
if 'VARCHAR' in vars(FIELD_TYPE):
    field_types.append(FIELD_TYPE.VARCHAR)

for field_type in field_types:
    # CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type] #Python2
    CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + [CONVERSIONS[field_type]] #Python3


# Alias some common MySQL exceptions
IntegrityError = MySQLdb.IntegrityError
OperationalError = MySQLdb.OperationalError
