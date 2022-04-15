import dataclasses
from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb


app = Flask('__name__') 
#configurações do Banco de Dados
app.config['MYSQL_HOST'] = 'localhost' #adicione o hostname
app.config['MYSQL_USER'] = 'root' #adicione o nome do seu usuário do MySQL
app.config['MYSQL_PASSWORD'] = 'Fatec.5009' #adicione a senha do seu usuário do MySQL
app.config['MYSQL_DB'] = 'usuarios_solicitacoes' 

#conexão com o Banco e fórmulas que serão utilizadas futuramente 
con = MySQLdb.connect( user="root", password="Fatec.5009", db="usuarios_solicitacoes")#adicione o nome e a senha do seu usuário do MySQL
mysql = MySQL(app)
check_user = ("SELECT * FROM usuarios WHERE email_usuario=%s")
check_password = ("SELECT * FROM usuarios WHERE senha_usuario=%s AND email_usuario=%s")
add_user = ('INSERT into usuarios (email_usuario,senha_usuario) VALUES (%s, %s)')
add_solicitacao = ('INSERT into chamado (solicitacao,email_usuario,data_inicio) VALUES (%s,%s, now())')
logado = False


@app.route('/')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

@app.route('/telausuario.html')
def telausuario():
    if logado:
        if email== 'executor@exec': #esse será o e-mail do executor
                cur = mysql.connection.cursor()
                users = cur.execute("select * from chamado")
                userDetails = cur.fetchall()
                return render_template("telaexecutor.html", userDetails=userDetails)
        else: 
            return render_template('telausuario.html')
    else:
        return redirect('/cadastro.html')

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
            #aqui ele mandaria uma mensagem para o html avisando que o e-mail inserido já possui uma conta mas por enquanto ele só direciona para a tela de login
            return redirect('/login.html')
        elif senha != confirmacao_senha:
            #aqui ele mandaria uma mensagem de erro para o html mas por enquanto ele só redireciona pra si mesmo
            return redirect('/cadastro.html')
        else:
            cur.execute(add_user, [email, senha])
            con.commit()
            global logado
            logado = True
            return redirect('/telausuario.html')
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
        #caso não tenha e-mail cadastrado ele direciona para a área de cadastro
        return redirect('/cadastro.html')
    else:
        cur.execute(check_password, [senha, email])
        feedback = cur.fetchall()
        
        if feedback:
            global logado
            logado = True
            return redirect('/telausuario.html')
        else:
            #aqui ele mandaria uma mensagem caso o e-mail e/ou senha estiverem incorretos mas por enquanto ele só redireciona pra si mesmo
            return redirect('/login.html')


@app.route('/telausuario.html', methods= ['POST'])
def telausuarioact():
    solicitacao = request.form['solicitacao']
    cur = con.cursor()
    cur.execute(add_solicitacao, [solicitacao, email])
    feedback = cur.fetchall
    con.commit()
    
    return redirect ('/telausuario.html')