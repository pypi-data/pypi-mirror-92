"""
https://stackoverflow.com/a/60894948/3872976
"""

import logging

from django.db import OperationalError, InterfaceError, IntegrityError
from django.db.backends.mysql import base

logger = logging.getLogger('mysql_server_has_gone_away')

def check_mysql_gone_away(db_wrapper):
    def decorate(f):
        def wrapper(self, query, args=None):
            try:
                return f(self, query, args)
            except (OperationalError, InterfaceError) as e:
                logger.warn("MySQL server has gone away. Rerunning query: %s", query)
                if (
                    'MySQL server has gone away' in str(e) or
                    'Lost connection to MySQL server during query' in str(e)
                ):
                    db_wrapper.connection.close()
                    db_wrapper.connect()
                    self.cursor = db_wrapper.connection.cursor()
                    return f(self, query, args)
                # Map some error codes to IntegrityError, since they seem to be
                # misclassified and Django would prefer the more logical place.
                if e.args[0] in self.codes_for_integrityerror:
                    raise IntegrityError(*tuple(e.args))
                raise
        return wrapper

    return decorate


class DatabaseWrapper(base.DatabaseWrapper):

    def create_cursor(self, name=None):

        class CursorWrapper(base.CursorWrapper):

            @check_mysql_gone_away(self)
            def execute(self, query, args=None):
                return self.cursor.execute(query, args)

            @check_mysql_gone_away(self)
            def executemany(self, query, args):
                return self.cursor.executemany(query, args)

        cursor = self.connection.cursor()
        return CursorWrapper(cursor)
