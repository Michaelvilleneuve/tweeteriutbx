import logging
import os
import sqlite3
import time

from flask import Flask, request, render_template, session, flash, redirect, url_for, abort, g
from passlib.hash import sha256_crypt

#from Arduino import Arduino
#from Arithmo import TweeterDAO
#from Arithmo.ArithmoThread import ArithmoThread

HOST = '127.0.0.1'
PORT = 5000  # change to 80 in prod with sudo run

app = Flask(__name__)
app.config.from_object(__name__)  # Load config from this file.

app.config.update(dict(
    DATABASE=os.path.join(app.root_path + '/db', 'arithmo.sqlite'),
    SECRET_KEY='Asup3rScr37$#keYt0h4%rdtoF1nD'
))

log_level = os.environ.get("LOGLEVEL") or 'NOTSET'

# Create logger
Log = logging.getLogger('Tweetos')
Log.setLevel(log_level)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

file_handler = logging.FileHandler(
    os.path.dirname(os.path.abspath(__file__)) + '/logs/' + time.strftime("%d_%m_%Y") + '_tweetos-app.log')
file_handler.setLevel(log_level)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
Log.addHandler(console_handler)
Log.addHandler(file_handler)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def query_db(query):
    """Execute a sql query"""
    db = get_db()
    cur = db.execute(query)
    rv = cur.fetchall()
    #db.close()
    return rv[0]

def get_users_count():
    """Get number of users"""
    db = get_db()
    cur = db.execute('SELECT count(*) FROM users')
    userscount = cur.fetchone()
    #db.close()
    return userscount

def set_user(setUsername, setPassword):
    """Create a user"""
    db = get_db()
    db.execute('INSERT INTO users (pseudo, password) VALUES (\'' + setUsername + '\', \'' + setPassword + '\')')
    db.commit()
    #db.close()

def get_twitter():
    """Get informations from twitter table"""
    db = get_db()
    cur = db.execute('SELECT * FROM twitter')
    twitterData = cur.fetchone()
    #db.close()
    return twitterData

def set_twitter(setToken, setSecretToken):
    """Set informations in twitter table"""
    db = get_db()
    db.execute('INSERT INTO twitter (token_access, token_access_secret) VALUES (\'' + setToken + '\', \'' + setSecretToken + '\')')
    db.commit()

@app.route('/')
def hello_world():
    """Home/index"""
    countUsers = get_users_count()
    if countUsers[0] != 0:
        return render_template('welcome.html')
    else:
        flash('For your first utilisation, you need an account.')
        return render_template('setup.html')

@app.route('/api/tweeter', methods=['GET'])
def tweet_webhook():
    Log.info("Incoming message : %s", request.args)
    return 'Hello', 200

@app.route('/api/tweeter', methods=['POST'])
def tweet_request():
    Log.info("Incoming POST request from tweeter : %s", request.args)

@app.route('/setup', methods=['POST'])
def setup():
    """First connection"""
    logout()
    countUsers = get_users_count()
    if countUsers[0] == 0 and request.method == 'POST' and request.form['username'] != '' and request.form['password'] != '' and request.form['passwordvalidation'] != '' and request.form['password'] == request.form['passwordvalidation']:
        set_user(request.form['username'], encrypt_word(request.form['password']))
        session['logged_in'] = True
        flash('You have created your auth and were logged in now')
    return hello_world()

@app.route('/twitter', methods=['POST'])
def twitter():
    """Submit Twitter tokens informations in database"""
    countUsers = get_users_count()
    if countUsers[0] != 0 and request.method == 'POST' and session['logged_in'] == True and request.form['token'] != '' and  request.form['secrettoken'] != '':
        reset_twitter()
        set_twitter(request.form['token'], request.form['secrettoken'])
        flash('Data submitted.')
    else:
        flash('Error when submitting.')
    return hello_world()


@app.route('/login', methods=['POST'])
def login():
    """Log in the manage interface"""
    countUsers = get_users_count()
    if countUsers[0] != 0 and request.method == 'POST' and request.form['username'] != '' and request.form['password'] != '':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cur = db.execute('select * from users where pseudo = \'' + username + '\'')
        user = cur.fetchone()
        testPass = decrypt_word(password, user['password'])
        if user and user['pseudo'] == username and testPass == True:
            session['logged_in'] = True
            flash('You were logged in')
    return hello_world()

@app.route('/logout')
def logout():
    """Log out the manage interface"""
    session['logged_in'] = False
    session.pop('logged_in', None)
    for key in session.keys():
        session.pop[key]
    session.clear()
    flash('You were logged out')
    return hello_world()

def encrypt_word(wordClean):
    wordEncrypt = sha256_crypt.encrypt(wordClean)
    return wordEncrypt

def decrypt_word(wordClean, wordEncrypt):
    wordDecrypt = sha256_crypt.verify(wordClean, wordEncrypt)
    return wordDecrypt

def reset_twitter():
    db = get_db()
    db.execute('DELETE FROM twitter')
    db.commit()

def reset_all():
    logout()
    db = get_db()
    db.execute('DELETE FROM users')
    db.commit()
    db.execute('DELETE FROM twitter')
    db.commit()
    return hello_world()

def run():
    Log.info("Start server at host http://%s:%i", HOST, PORT)
    app.run(port=PORT, host=HOST)
    Log.info("Create Twitter api instance")
    # api = twitter.Api(consumer_key='plop')

if __name__ == '__main__':
    run()

