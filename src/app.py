﻿from concurrent.futures import Executor
import dataclasses
from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb
import functools


#CONGFIGURAÇÃO MYSQL/FLASK----------------------------------------------------CONGFIGURAÇÃO MYSQL/FLASK------------------------
app = Flask('__name__') 
app.config['MYSQL_HOST'] = 'localhost' #adicione o hostname
app.config['MYSQL_USER'] = 'root' #adicione o nome do seu usuário do MySQL
app.config['MYSQL_PASSWORD'] = 'fatec' #adicione a senha do seu usuário do MySQL
app.config['MYSQL_DB'] = 'usuarios_solicitacoes' 
con = MySQLdb.connect( user="root", password="fatec", db="usuarios_solicitacoes")#adicione o nome e a senha do seu usuário do MySQL
mysql = MySQL(app)
logado = False
app.secret_key = "fatec"



#FUNCÇÕES MYSQL----------------------------------------------------------------FUNCÇÕES MYSQL-------------------------------
#FUNÇÕES SELECT
check_user = ("SELECT * FROM usuarios WHERE email_usuario=%s")
check_password = ("SELECT * FROM usuarios WHERE senha_usuario=%s AND email_usuario=%s")
historico = ("SELECT * FROM chamado WHERE email_usuario=%s ORDER BY data_inicio DESC;")
verifica_funcao = ("SELECT funcao FROM usuarios WHERE email_usuario =%s")
quantia_exe = ("SELECT COUNT(*) FROM usuarios WHERE funcao = 2;")
quantia_chamado = ("SELECT COUNT(*) FROM chamado;")

#FUNÇÕES INSERT/UPDATE
add_user = ('INSERT into usuarios (email_usuario,senha_usuario,funcao) VALUES (%s,%s,%s)')
add_solicitacao = ('INSERT into chamado (solicitacao,email_usuario,executor,_status,problema,data_inicio) VALUES (%s,%s,%s,%s,%s, now())')
add_resposta = ("UPDATE chamado SET resposta=%s, _status=%s, data_fechamento=now() WHERE codigo_solicitacao = %s")
tornar_exe = ("UPDATE usuarios SET funcao=%s WHERE codigo_usuario = %s")
exe_cont = ('INSERT into distribuicao (executor,contador) VALUES (%s,%s)')




#FUNÇÕES DE AUTENTICAÇÃO-------------------------------------------------------FUNÇÕES DE AUTENTICAÇÃO-----------------------------
def check_func(func):
    if func in session['func']:
        return True
    else:
        return False

def check_id_user(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):        
        if not 'func' in session.keys():
            return redirect("/")
        elif check_func('1'):
            return view(**kwargs)
        return redirect("/")
    return wrapped_view

def check_id_exec(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):        
        if not 'func' in session.keys():
            return redirect("/login.html")
        elif check_func('2'):
            return view(**kwargs)
        return redirect("/login.html")
    return wrapped_view

def check_id_adm(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):        
        if not 'func' in session.keys():
            return redirect("/login.html")
        elif check_func('3'):
            return view(**kwargs)
        return redirect("/login.html")
    return wrapped_view




#LOGIN/CADASTRO----------------------------------------------------------------LOGIN/CADASTRO-------------------------------
#ROTAS
@app.route('/')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

#FUNÇÕES
@app.route('/cadastro.html', methods= ['POST'])
def cadastroact():
    global email
    email= request.form['email']
    senha= request.form['senha']
    confirmacao_senha= request.form['confirmacao_senha']
    ciencia= request.form.get('ciencia')
    cur = con.cursor()
    cur.execute(check_user, [email])
    feedback = cur.fetchall()
    
    if ciencia == 'yes':
        if feedback:
            return redirect('/login.html')
        elif senha != confirmacao_senha:
            return redirect('/cadastro.html')
        else:
            cur.execute(add_user, [email, senha, 1])
            con.commit()
            global logado
            logado = True
            return redirect('/validacao')
    else:
        return redirect('/cadastro.html')


@app.route('/login.html', methods= ['POST'])
def loginact():
    global email
    email= request.form['email']
    senha= request.form['senha']
    cur = mysql.connection.cursor()
    cur.execute(check_user, [email])
    feedback = cur.fetchall()
    
    if not feedback:
        return redirect('/cadastro.html')
    else:
        cur.execute(check_password, [senha, email])
        feedback = cur.fetchall()
        
        if feedback:
            global logado
            logado = True
            return redirect('/validacao')
        else:
            return redirect('/login.html')


@app.route('/validacao')
def validacao():
    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [email])
    funcao = cur.fetchall()

    for f in funcao:  #função no sentido de qual a função do usuario
        if logado:
            if f[0] == 3: #validacao para ver se é o executor 
                session['func'] = str(f[0])
                return redirect('telaadm')
            elif f[0] == 2:
                session['func'] = str(f[0])
                return redirect('telaexecutor')
            else: 
                session['func'] = str(f[0])
                return redirect('telausuario')
        else:
            return redirect('/cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login.html")




#PAGINAS DE USUARIO/EXECUTOR/ADIMINISTRADOR------------------------------------PAGINAS DE USUARIO/EXECUTOR/ADIMINISTRADOR-----------------------------------------------------------
@app.route('/telaadm')
@check_id_adm
def telaadm():
    cur = mysql.connection.cursor()
    cur.execute("select * FROM usuarios;")
    usuarios = cur.fetchall()

    cur.execute("select * FROM chamado ORDER BY data_inicio DESC;") #pegar todas infos dos chamados 
    Details = cur.fetchall()
    
    cur.execute(historico, [email])
    lista = cur.fetchall()

    cur.execute("select _status FROM chamado ORDER BY data_inicio DESC;")
    chamados = cur.fetchall()
    aberto = 0
    fechado = 0
    for k in chamados:
        list(k)
        if k[0] == 'Aberto':
            aberto = aberto + 1
        else:
            fechado = fechado + 1
    per_cham = [aberto,fechado]

    return render_template("adm.html", usuarios=usuarios, Details=Details, lista=lista, per_cham=per_cham)


@app.route('/telaexecutor')
@check_id_exec
def telaexecutor():
    cur = mysql.connection.cursor()
    cur.execute("select codigo_usuario FROM usuarios where email_usuario=%s;", [email])
    funcao = int(str(cur.fetchall()).strip('(,)'))


    cur.execute("select * FROM chamado where executor=%s ORDER BY data_inicio DESC;",[funcao])
    Details = cur.fetchall()
    return render_template("telaexecutor.html", Details=Details)

@app.route('/telausuario')
@check_id_user
def hist():
    cur = mysql.connection.cursor()  
    users = cur.execute(historico, [email])
    lista = cur.fetchall()
    return render_template("telausuario.html", lista=lista)



#FUNÇÕES DE CHAMADO------------------------------------------------------------FUNÇÕES DE CHAMADO-----------------------------------
@app.route('/solicitacao', methods= ['POST']) 
def solicitacao():
    #isso possibilita o usuario fazer a solicitacao
    cur = mysql.connection.cursor()  
    a = cur.execute(quantia_exe)
    qta_exe = int(str(cur.fetchall()).strip('(,)'))
  
    cur.execute(quantia_chamado)
    qta_cha = int(str(cur.fetchall()).strip('(,)')) +1

    if qta_exe == 0:
        qta_exe = 1
    else:
        qta_exe = qta_exe
    cont = qta_cha % qta_exe

    cur.execute("SELECT executor FROM distribuicao WHERE contador=%s;", [cont])
    executor = int(str(cur.fetchall()).strip('(,)'))

    solicitacao = request.form['solicitacao']
    problema = request.form['tipo']
    aberto = 'Aberto'
    cur = con.cursor()
    cur.execute(add_solicitacao, [solicitacao,email,executor,aberto,problema])
    feedback = cur.fetchall
    con.commit()

    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [email])
    funcao = cur.fetchall()

    for f in funcao: 
        if f[0] == 3:
            return redirect ('/telaadm')
        else:
            return redirect ('/telausuario')


@app.route('/resposta/<id>', methods= ['POST']) 
def resposta(id):
    #isso possibilita o executor ou o adm responder a solicitacao
    resposta = request.form['resposta']
    status = request.form['status']

    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [email])
    funcao = cur.fetchall()

    if resposta == '':
        for f in funcao: 
            if f[0] == 3:
                return redirect ('/telaadm#ab')
            else:
                return redirect ('/telaexecutor#ab')

    cur = con.cursor()
    cur.execute(add_resposta, [resposta,status,id])
    feedback = cur.fetchall
    con.commit()

    for f in funcao: 
        if f[0] == 3:
            return redirect ('/telaadm#ab')
        else:
            return redirect ('/telaexecutor#ab')



#FUNÇÕES DE ADM PROMOVER/REBAIXAR----------------------------------------------FUNÇÕES DE ADM PROMOVER/REBAIXAR-------------------------------------------------
@app.route('/tornarexe/<id>', methods= ['POST']) 
def usuarios(id):
    #isso possibilita o adm tornar um usuario em executor
    cur = con.cursor()
    cur.execute(tornar_exe, [2,id])
    feedback = cur.fetchall
    con.commit()

    cur = mysql.connection.cursor()  
    a = cur.execute(quantia_exe)
    qta_exe = int(str(cur.fetchall()).strip('(,)')) -1
    
    cur = con.cursor()
    cur.execute(exe_cont, [id,qta_exe])
    feedback = cur.fetchall
    con.commit()
    return redirect ("/telaadm#usuarios")


@app.route('/tornaruser/<id>', methods= ['POST']) 
def executor(id):
    #isso possibilita o adm tornar um executor em usuario
    cur = con.cursor()
    cur.execute(tornar_exe, [1,id])
    feedback = cur.fetchall
    con.commit()
    return redirect ("/telaadm#usuarios")

