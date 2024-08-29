from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'agenda.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    contatos = conn.execute('SELECT * FROM  pessoa').fetchall()
    conn.close()
    return render_template('index.html', contatos = contatos)

@app.route('/delete/<int:idpessoa>')
def delete_contact(idpessoa):
    conn = get_db_connection()
    conn.execute('DELETE FROM pessoa WHERE idpessoa = ?', (idpessoa,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add', methods=('GET', 'POST'))
def add_contect():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        conn = get_db_connection()
        conn.execute('INSERT INTO pessoa (nome, telefone, email) VALUES(?, ?, ?)', (nome, telefone, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_contact.html')

if __name__ == '__main__':
    app.run(debug=True)