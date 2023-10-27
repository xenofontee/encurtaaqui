from flask import Flask, g, request, redirect
import sqlite3
import random

app = Flask(__name__)

DATABASE = 'links.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# @app.route('/')
# def index():
#     return 'Hello, World'

@app.route('/shorten', methods=['POST'])
def shorten():
    db = get_db()
    cursor = db.cursor()
    url = request.form['url']
    cursor.execute('Insert Into links (url) Values (?)', (url,))
    db.commit()
    link_id = cursor.lastrowid
    short_link = f'http://localhost:5000/{link_id}'
    return short_link

@app.route('/<int:link_id>')
def redirect_to_url(link_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT url FROM links Where id = ?', (link_id,))
    result = cursor.fetchone()
    if result is None:
        return (404)
    url = result[0]
    return redirect(url, code=302)

if __name__ == '__main__':
    app.run()