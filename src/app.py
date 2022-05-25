from concurrent.futures import Executor
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
check_user = ("SELECT * FROM usuarios WHERE email=%s")
check_password = ("SELECT * FROM usuarios WHERE senha=%s AND email=%s")
historico = ("SELECT * FROM solicitacao WHERE codigo_usuario_cli=%s ORDER BY data_abertura DESC;")
verifica_funcao = ("SELECT funcao FROM usuarios WHERE codigo_usuario =%s")
quantia_tec = ("SELECT COUNT(*) FROM usuarios WHERE funcao = 2;")
quantia_chamado = ("SELECT COUNT(*) FROM solicitacao;")

#FUNÇÕES INSERT/UPDATE
add_user = ('INSERT into usuarios (email,senha,funcao) VALUES (%s,%s,%s)')
add_solicitacao = ('INSERT into solicitacao (descricao,codigo_usuario_cli,codigo_usuario,_status,tipo_problema,data_abertura) VALUES (%s,%s,%s,%s,%s, now())')
add_resposta = ("UPDATE solicitacao SET resposta=%s, _status=%s, data_fechamento=now() WHERE codigo_solicitacao = %s")
tornar_tec = ("UPDATE usuarios SET funcao=%s WHERE codigo_usuario = %s")
tec_cont = ("UPDATE usuarios SET contador_solicitacao=%s WHERE codigo_usuario = %s")
check_cod_usu = ("select codigo_usuario FROM usuarios where email=%s;")




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

def check_id_tec(view):
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
    global cod

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
            cur = mysql.connection.cursor()
            cur.execute(check_cod_usu, [email])
            cod = int(str(cur.fetchall()).strip('(,)'))
            global logado
            logado = True
            return redirect('/validacao')
    else:
        return redirect('/cadastro.html')


@app.route('/login.html', methods= ['POST'])
def loginact():
    global cod

    email= request.form['email']
    senha= request.form['senha']
    cur = mysql.connection.cursor()
    cur.execute(check_user, [email])
    feedback = cur.fetchall()
    
    if feedback != ():

        cur = mysql.connection.cursor()
        cur.execute(check_cod_usu, [email])
        cod = int(str(cur.fetchall()).strip('(,)'))
        
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
                aviso = "*Senha errada, tente novamente"
                return render_template('/login.html', aviso=aviso)
            
    else:
        aviso ="*Email informado não possui conta, crie uma!"
        return render_template('/cadastro.html', aviso=aviso)


@app.route('/validacao')
def validacao():
    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [cod])
    funcao = cur.fetchall()

    for f in funcao:  #função no sentido de qual a função do usuario
        if logado:
            if f[0] == 3: #validacao para ver se é o técnico
                session['func'] = str(f[0])
                return redirect('telaadm')
            elif f[0] == 2:
                session['func'] = str(f[0])
                return redirect('telatecnico')
            else: 
                session['func'] = str(f[0])
                return redirect('telausuario')
        else:
            return redirect('/cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login.html")




#PAGINAS DE USUARIO/TÉCNICO/ADIMINISTRADOR------------------------------------PAGINAS DE USUARIO/TÉCNICO/ADIMINISTRADOR-----------------------------------------------------------
@app.route('/telaadm')
@check_id_adm
def telaadm():
    cur = mysql.connection.cursor()
    cur.execute("select * FROM usuarios;")
    usuarios = cur.fetchall()

    cur.execute("select * FROM solicitacao ORDER BY data_abertura DESC;") #pegar todas infos dos chamados 
    Details = cur.fetchall()
    
    cur.execute(historico, [cod])
    lista = cur.fetchall()

    cur.execute("select _status FROM solicitacao ORDER BY data_abertura DESC;")
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


@app.route('/telatecnico')
@check_id_tec
def telatecnico():
    cur = mysql.connection.cursor()
    cur.execute("select codigo_usuario FROM usuarios where codigo_usuario=%s;", [cod])
    x = int(str(cur.fetchall()).strip('(,)'))
    
    cur.execute("select * FROM solicitacao where codigo_usuario=%s ORDER BY data_abertura DESC;",[x])
    Details = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("select * FROM usuarios;")
    usuarios = cur.fetchall()

    return render_template("telatecnico.html", Details=Details, usuarios=usuarios)

@app.route('/telausuario')
@check_id_user
def hist():
    cur = mysql.connection.cursor()  
    users = cur.execute(historico, [cod])
    lista = cur.fetchall()
    return render_template("telausuario.html", lista=lista)



#FUNÇÕES DE CHAMADO------------------------------------------------------------FUNÇÕES DE CHAMADO-----------------------------------
@app.route('/solicitacao', methods= ['POST']) 
def solicitacao():
    #isso possibilita o usuario fazer a solicitacao
    cur = mysql.connection.cursor()  
    a = cur.execute(quantia_tec)
    qta_tec = int(str(cur.fetchall()).strip('(,)'))
  
    cur.execute(quantia_chamado)
    qta_cha = int(str(cur.fetchall()).strip('(,)')) +1

    if qta_tec == 0:
        qta_tec = 1
    else:
        qta_tec = qta_tec
    cont = qta_cha % qta_tec

    print (cont)

    cur.execute("SELECT codigo_usuario FROM usuarios WHERE contador_solicitacao=%s;", [cont])
    tecnico = cur.fetchall()
    tecnico = int(str(tecnico).strip('(,)'))

    solicitacao = request.form['solicitacao']
    problema = request.form['tipo']
    aberto = 'Aberto'
    cur = con.cursor()
    cur.execute(add_solicitacao, [solicitacao,cod,tecnico,aberto,problema])
    feedback = cur.fetchall
    con.commit()

    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [cod])
    funcao = cur.fetchall()

    for f in funcao: 
        if f[0] == 3:
            return redirect ('/telaadm')
        else:
            return redirect ('/telausuario')


@app.route('/resposta/<id>', methods= ['POST']) 
def resposta(id):
    #isso possibilita o técnico ou o adm responder a solicitacao
    resposta = request.form['resposta']
    status = request.form['status']

    cur = mysql.connection.cursor()
    cur.execute(verifica_funcao, [cod])
    funcao = cur.fetchall()

    if resposta == '':
        for f in funcao: 
            if f[0] == 3:
                return redirect ('/telaadm#ab')
            else:
                return redirect ('/telatecnico#ab')

    cur = con.cursor()
    cur.execute(add_resposta, [resposta,status,id])
    feedback = cur.fetchall
    con.commit()

    for f in funcao: 
        if f[0] == 3:
            return redirect ('/telaadm#ab')
        else:
            return redirect ('/telatecnico#ab')



#FUNÇÕES DE ADM PROMOVER/REBAIXAR----------------------------------------------FUNÇÕES DE ADM PROMOVER/REBAIXAR-------------------------------------------------
@app.route('/tornarexe/<id>', methods= ['POST']) 
def usuarios(id):
    #isso possibilita o adm tornar um usuario em tecnico
    cur = con.cursor()
    cur.execute(tornar_tec, [2,id])
    feedback = cur.fetchall
    con.commit()

    cur = mysql.connection.cursor()  
    a = cur.execute(quantia_tec)
    qta_tec = int(str(cur.fetchall()).strip('(,)')) -1
    
    cur = con.cursor()
    cur.execute(tec_cont, [qta_tec,id])
    feedback = cur.fetchall
    con.commit()
    return redirect ("/telaadm#usuarios")


@app.route('/tornaruser/<id>', methods= ['POST']) 
def tecnico(id):
    # -------------------------------

    cur = mysql.connection.cursor()  
    a = cur.execute(quantia_tec)
    max_cont = int(str(cur.fetchall()).strip('(,)'))

    print (max_cont)

    cur = mysql.connection.cursor()
    cur.execute('SELECT codigo_usuario, contador_solicitacao FROM usuarios WHERE funcao=%s', [2])
    tec_cont_soli = cur.fetchall()

    print (tec_cont_soli)

    # ------------------------------
    cur = con.cursor()
    cur.execute('SELECT codigo_solicitacao FROM solicitacao WHERE codigo_usuario=%s', [id])
    soli_tec = cur.fetchall()
    solicitacoes = []
    for n in soli_tec:
        n = int(str(n).strip('(,)'))
        solicitacoes.append(n)
    

    cur.execute('UPDATE usuarios SET funcao=%s, contador_solicitacao=%s WHERE codigo_usuario = %s', [1,None,id])
    feedback = cur.fetchall
    con.commit()

    cur.execute('SELECT codigo_usuario FROM usuarios WHERE funcao=%s', [2])
    tecni = cur.fetchall()
    tecnicos = []
    for n in tecni:
        n = int(str(n).strip('(,)'))
        tecnicos.append(n)

    current_tec = 0
    for s in solicitacoes:
        if current_tec == len(tecnicos):
            current_tec = 0

        cur.execute('UPDATE solicitacao SET codigo_usuario=%s WHERE codigo_solicitacao=%s', [tecnicos[current_tec], s])
        current_tec += 1

    con.commit()
    # ------------------------------

    cur = mysql.connection.cursor()
    cur.execute('SELECT contador_solicitacao FROM usuarios WHERE codigo_usuario=%s', [id])
    cod_cont = int(str(cur.fetchall()).strip('(,)'))

    print (cod_cont)

    if max_cont != cod_cont-1:
        
        for contador_tecs in range(max_cont):
            print (contador_tecs)
            if cod_cont < contador_tecs:
                
                x = contador_tecs-1

                cur = con.cursor()
                cur.execute('UPDATE usuarios SET contador_solicitacao=%s WHERE contador_solicitacao=%s', [x,contador_tecs])
        con.commit()


    # ------------------------------

    return redirect ("/telaadm#usuarios")
