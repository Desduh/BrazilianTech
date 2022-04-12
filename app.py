import dataclasses
from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb


app = Flask('_name_') 

#adicionei umas funções do MySQL como variaveis pra facilitar no futuro
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'Fatec.5009'
app.config['MYSQL_DB'] = 'usuarios_solicitacoes' 
#esse con parece reduntante em comparação com os configs em cima mas é necessario pra dar commit no bd
con = MySQLdb.connect( user="root", password="Fatec.5009", db="usuarios_solicitacoes")
mysql = MySQL(app)
check_user = ("SELECT * FROM usuarios WHERE email_usuario=%s")
check_password = ("SELECT * FROM usuarios WHERE senha_usuario=%s AND email_usuario=%s")
add_user = ('INSERT into usuarios (email_usuario,senha_usuario) VALUES (%s, %s)')
add_solicitacao = ('INSERT into chamado (solicitacao,email_usuario,data_inicio) VALUES (%s, %s, now())')
logado = False
#pra mudar entre login e cadastro vc muda as routes 
#quando for botar as paginas reais deve se tirar todos os "teste" na frente incluindo das funções
@app.route('/')
@app.route('/teladeinicio')
def teladeinicio():            
    return render_template('tela_de_inicio.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

@app.route('/telausuario.html')
def telausuario():
    if logado:
        return render_template('telausuario.html')
    else:
        return redirect('/cadastro.html')
#aqui é a parte de cadastro 
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
    #aqui ele checa se o email existe no bd
    if ciencia == 'yes':
        if feedback:
            #aqui ele mandaria uma msg de erro pelo html mas por enquanto ele só redireciona pra si mesmo
            return redirect('/login.html')
        #aqui ele confirma q as duas senhas são iguais
        elif senha != confirmacao_senha:
            #aqui ele mandaria uma msg de erro pelo html mas por enquanto ele só redireciona pra si mesmo
            return redirect('/cadastro.html')
        else:
            #caso tudo esteja em ordem ele lança pro bd e direciona para a tela principal
            cur.execute(add_user, [email, senha])
            con.commit()
            global logado
            logado = True
            return redirect('/telausuario.html')
    else:
        return redirect('/cadastro.html')
        
#aqui é a parte do login
@app.route('/login.html', methods= ['POST'])
def loginact():
    global email
    email= request.form['email']
    senha= request.form['senha']
    cur = mysql.connection.cursor()
    cur.execute(check_user, [email])
    feedback = cur.fetchall()
    #aqui ele checa se o email existe no bd
    if not feedback:
        #caso n tenha ele direciona para a area de cadastro
        return redirect('/cadastro.html')
    else:
        cur.execute(check_password, [senha, email])
        feedback = cur.fetchall()
        #aqui ele checa se a senha existe e esta atrelada ao email
        if feedback:
            #caso sim ele direciona para a pagina principal
            global logado
            logado = True
            return redirect('/telausuario.html')
        else:
            #aqui ele mandaria uma msg de erro pelo html mas por enquanto ele só redireciona pra si mesmo
            return redirect('/login.html')

@app.route('/telausuario.html', methods= ['POST'])
def telausuarioact():
    solicitacao = request.form['solicitacao']
    cur = con.cursor()
    cur.execute(add_solicitacao, [solicitacao, email])
    feedback = cur.fetchall()
    con.commit()
    return redirect ('/cadastro.html')