import os
import sqlite3

from arithmo import app


class DB:
    def __init__(self):
        pass
        # Data base connection

    def connect_db(self):
        """Connects to the specific database."""
        rv = sqlite3.connect(app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(self.g, 'sqlite_db'):
            self.g.sqlite_db = self.connect_db()
        return self.g.sqlite_db

    @app.teardown_appcontext
    def close_db(self, error):
        """Closes the database again at the end of the request."""
        if hasattr(self.g, 'sqlite_db'):
            self.g.sqlite_db.close()

    def init_db(self):
        db = self.get_db()
        with app.open_resource(os.path.join(app.root_path + '/db', 'schema.sql'), mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    @app.cli.command('initdb')
    def initdb_command(self):
        """Initializes the database."""
        self.init_db()
        print('Initialized the database.')
