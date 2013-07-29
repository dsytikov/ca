# -*- coding: utf-8 -*-
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

DATABASE = 'D:\py\ca\ca.db'
#DATABASE = 'C:\py\ca\ca.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('CA_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, company, data_check, surname, name, patronymic, bday, address, result_check, resolve from candidats order by id asc')
    candidats = [dict(id=row[0], company=row[1], data_check=row[2], surname=row[3], name=row[4], patronymic=row[5], bday=row[6], address=row[7], \
    result_check=row[8], resolve=row[9]) for row in cur.fetchall()]
    return render_template('show_entries.html', candidats=candidats)

@app.route('/add')
def add_entry():
    return render_template('add.html')

@app.route('/edit/<id>')
def edit_entry(id):
    #db = get_db()
    #cur = g.db.execute('select * from candidats where id = ?', [id])
    #candidats = cur.fetchall()
	cur = g.db.execute('select id, company, data_check, surname, name, patronymic, bday, address, result_check, resolve from candidats where id = ?', [id])
	candidats = [dict(id=row[0], company=row[1], data_check=row[2], surname=row[3], name=row[4], patronymic=row[5], bday=row[6], address=row[7], \
	result_check=row[8], resolve=row[9]) for row in cur.fetchall()]
	return render_template('edit.html', candidats=candidats)

@app.route('/write', methods=['POST'])
def write_entry():
    if request.form['company'] == '' or \
    request.form['data_check'] == '' or \
    request.form['surname'] == '' or \
    request.form['name'] == '' or \
    request.form['patronymic'] == '' or \
    request.form['resolve'] == '':
        return redirect(url_for('add_entry'))
    g.db.execute('insert into candidats (company, data_check, surname, name, patronymic, bday, address, result_check, resolve) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            [request.form['company'], request.form['data_check'], request.form['surname'], request.form['name'], request.form['patronymic'], request.form['bday'], request.form['address'], request.form['result_check'], request.form['resolve']])
    g.db.commit()
    #flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
    
@app.route('/update', methods=['POST'])
def update_entry():
    '''if request.form['company'] == '' or \
    request.form['data_check'] == '' or \
    request.form['surname'] == '' or \
    request.form['name'] == '' or \
    request.form['patronymic'] == '' or \
    request.form['resolve'] == '':
        return redirect(url_for('add_entry'))'''
    g.db.execute('UPDATE candidats SET company=? WHERE id=?', (request.form['company'], request.form['id']))
    g.db.commit()
    return redirect(url_for('show_entries'))
    
if __name__ == '__main__':
    #init_db()
    app.run(host='0.0.0.0')
