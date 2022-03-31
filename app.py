
from flask import Flask, render_template, url_for

app = Flask('__name__')


@app.route('/')
@app.route('/tela_de_inicio.html')
def tela_de_inicio():
    return render_template('tela de inicio.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')
