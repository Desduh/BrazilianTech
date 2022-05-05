import dataclasses
from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb


app = Flask('__name__') 
#configurações do Banco de Dados
app.config['MYSQL_HOST'] = 'localhost' #adicione o hostname
app.config['MYSQL_USER'] = 'root' #adicione o nome do seu usuário do MySQL
app.config['MYSQL_PASSWORD'] = 'fatec' #adicione a senha do seu usuário do MySQL
app.config['MYSQL_DB'] = 'usuarios_solicitacoes' 

#conexão com o Banco e fórmulas que serão utilizadas futuramente 
con = MySQLdb.connect( user="root", password="fatec", db="usuarios_solicitacoes")#adicione o nome e a senha do seu usuário do MySQL
mysql = MySQL(app)
check_user = ("SELECT * FROM usuarios WHERE email_usuario=%s")
check_password = ("SELECT * FROM usuarios WHERE senha_usuario=%s AND email_usuario=%s")
add_user = ('INSERT into usuarios (email_usuario,senha_usuario,funcao) VALUES (%s,%s,%s)')
add_solicitacao = ('INSERT into chamado (solicitacao,email_usuario,_status,problema,data_inicio) VALUES (%s,%s,%s,%s, now())')
add_resposta = ("UPDATE chamado SET resposta=%s, email_executor=%s, _status=%s, data_fechamento=now() WHERE codigo_solicitacao = %s")
historico = ("SELECT * FROM chamado WHERE email_usuario=%s ORDER BY data_inicio DESC;")
verifica_funcao = ("SELECT funcao FROM usuarios WHERE email_usuario =%s")

logado = False


@app.route('/')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')



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
        #caso não tenha e-mail cadastrado ele direciona para a área de cadastro
        return redirect('/cadastro.html')
    else:
        cur.execute(check_password, [senha, email])
        feedback = cur.fetchall()
        
        if feedback:
            global logado
            logado = True
            return redirect('/validacao')
        else:
            #aqui ele mandaria uma mensagem caso o e-mail e/ou senha estiverem incorretos mas por enquanto ele só redireciona pra si mesmo
            return redirect('/login.html')



@app.route('/validacao')
def validacao():
    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [email])
    funcao = cur.fetchall()

    for f in funcao:  
        if logado:
            if f[0] == 3: #validacao para ver se é o executor 
                return redirect('telaadm')
            elif f[0] == 2:
                return redirect('telaexecutor')
            else: 
                return redirect('telausuario')
        else:
            return redirect('/cadastro.html')



@app.route('/telaadm')
def telaadm():
    cur = mysql.connection.cursor()
    users = cur.execute("select * FROM chamado ORDER BY data_inicio DESC;")
    Details = cur.fetchall()
    cur = mysql.connection.cursor()  
    global email
    users = cur.execute(historico, [email])
    lista = cur.fetchall()
    return render_template("adm.html", Details=Details, lista=lista)

@app.route('/telaexecutor')
def telaexecutor():
    cur = mysql.connection.cursor()
    users = cur.execute("select * FROM chamado ORDER BY data_inicio DESC;")
    Details = cur.fetchall()
    return render_template("telaexecutor.html", Details=Details)

@app.route('/telausuario')
def hist():
    cur = mysql.connection.cursor()  
    global email
    users = cur.execute(historico, [email])
    lista = cur.fetchall()
    return render_template("telausuario.html", lista=lista)



@app.route('/solicitacao', methods= ['POST']) 
def solicitacao():
    #isso possibilita o usuario fazer a solicitacao
    solicitacao = request.form['solicitacao']
    problema = request.form['tipo']
    aberto = 'Aberto'
    cur = con.cursor()
    cur.execute(add_solicitacao, [solicitacao,email,aberto,problema])
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

@app.route('/aceitando/<id>', methods= ['POST']) 
def aceitar(id):
    #isso possibilita o executor responder a solicitacao
    resposta = request.form['aceito']
    status = 'Aceito'
    cur = con.cursor()
    cur.execute(add_resposta, [resposta,email,status,id])
    feedback = cur.fetchall
    con.commit()
    return redirect ("/telaexecutor#ab")

@app.route('/recusando/<id>', methods= ['POST']) 
def recusar(id):
    #isso possibilita o executor responder a solicitacao
    resposta = request.form['recusado']
    status = 'Negado'
    cur = con.cursor()
    cur.execute(add_resposta, [resposta,email,status,id])
    feedback = cur.fetchall
    con.commit()
    return redirect ("/telaexecutor#ab")