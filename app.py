
from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL 

app = Flask('__name__')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fatec'
app.config['MYSQL_DB'] = 'usuarios_solicitacoes'

mysql = MySQL(app)


@app.route('/')
@app.route('/tela_de_inicio.html')
def tela_de_inicio():
    return render_template('tela de inicio.html')

@app.route('/cadastro.html')
def pag_cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro.html', methods= ['POST'])
def cadastro():
    email= request.form['email']
    senha= request.form['senha']
    confsenha = request.form['confirmacao_senha']
    ciencia = request.form['ciencia']
    if senha == confsenha:
        cur = mysql.connection.cursor()
        cur.execute('INSERT into usuarios (email_usuario,senha_usuario) VALUES (%s, %s)',(email, senha))
        mysql.connection.commit()
        cur.close()
        return redirect('/login.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route("/tela usuario.html")
def tela_usuario():
    return render_template('tela usuario.html')

@app.route("/tela executor.html")
def tela_executor():
    return render_template('tela executor.html')


if __name__ == "__main__":
    app.run()
