from flask import  Flask, render_template, request,url_for, redirect, flash
""" from flask.wrappers import Request
from flask_mysqldb import MySQL """
import sqlite3 as sql


app = Flask(__name__)

app.secret_key = "mysecretkey"


@app.route('/')
def index():
    con = sql.connect("flaskcontact.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',  contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        con = sql.connect("flaskcontact.db")
        cur = con.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES ('{}','{}','{}')".format (fullname, phone, email))
        con.commit()
        flash('Contact Added successfully')
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def edit_contact(id):
    con = sql.connect("flaskcontact.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = '{}'".format (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>' , methods = ['POST'])
def method_name(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        con = sql.connect("flaskcontact.db")
        cur = con.cursor()
        cur.execute("UPDATE contacts SET  fullname = '{}', email = '{}',  phone = '{}' WHERE id = '{}'".format(fullname, email, phone, id))
        con.commit()
        flash('Contact Update successfully')
    return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    con = sql.connect("flaskcontact.db")
    cur = con.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    con.commit()
    flash('Contact Removed Successfully')
    return redirect('/')

if __name__ == '__main__':
    app.run(port = 3000, debug= True)