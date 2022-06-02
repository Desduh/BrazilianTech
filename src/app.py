from concurrent.futures import Executor
import dataclasses
from flask import Flask, render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb
import functools
from datetime import datetime, date
from dateutil.relativedelta import relativedelta




#CONGFIGURAÇÃO MYSQL/FLASK----------------------------------------------------CONGFIGURAÇÃO MYSQL/FLASK------------------------
app = Flask('__name__') 
app.config['MYSQL_HOST'] = 'localhost' #adicione o hostname
app.config['MYSQL_USER'] = 'root' #adicione o nome do seu usuário do MySQL
app.config['MYSQL_PASSWORD'] = 'franca' #adicione a senha do seu usuário do MySQL
app.config['MYSQL_DB'] = 'usuarios_solicitacoes' 
con = MySQLdb.connect( user="root", password="franca", db="usuarios_solicitacoes")#adicione o nome e a senha do seu usuário do MySQL
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
#AMD----------------------------------------------------------------
@app.route('/telaadm')
@check_id_adm
def telaadm():
    return render_template("adm.html")


@app.route('/nova_soli')
def nova_soli():
    return render_template('adm_nova_soli.html')


@app.route('/historico')
def historio():

    cur = mysql.connection.cursor()
    cur.execute(historico, [cod])
    dados = cur.fetchall()
    
    return render_template('adm_historico.html', dados=dados)


@app.route('/respondidas')
def respondidas():
    return render_template('adm_respondidas.html')


@app.route('/solicitacoes')
def solicitacaos():

    cur = mysql.connection.cursor()
    cur.execute("select * FROM solicitacao ORDER BY data_abertura DESC;") #pegar todas infos dos chamados 
    Details = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("select * FROM usuarios;")
    usuarios = cur.fetchall()

    return render_template('adm_solicitacoes.html', Details=Details, usuarios=usuarios)


@app.route('/usuarioss')
def usuarioss():

    cur = mysql.connection.cursor()
    cur.execute("select * FROM usuarios;")
    usuarios = cur.fetchall()

    return render_template('adm_usuarios.html', usuarios=usuarios)


@app.route('/graficos')
def graficos():

    dia_ref = date.today()
    intervalo = 'Tudo'
    per_cham = get_pie_info(intervalo, dia_ref)
    evo_cham = get_evo_info(intervalo, dia_ref)
    media_geral = get_media_geral()

    return render_template('adm_graficos.html', per_cham=per_cham, evo_cham=evo_cham, intervalo=intervalo, media_geral=media_geral)

@app.route('/intervalo', methods= ['POST'])
def intervalo():
    
    intervalo = request.form['intervalo']
    dia_ref = request.form['dataini']
    if dia_ref == '':
        dia_ref = date.today()
    else:
        dia_ref = datetime.strptime(dia_ref[2:], '%y-%m-%d').date()
    per_cham = get_pie_info(intervalo, dia_ref)
    evo_cham = get_evo_info(intervalo, dia_ref)
    media_geral = get_media_geral()


    return render_template('adm_graficos.html', per_cham=per_cham, evo_cham=evo_cham, intervalo=intervalo, media_geral=media_geral)
#--------------------------------------------------------

def get_media_geral():
    cur = con.cursor()
    cur.execute('SELECT avaliacao FROM solicitacao WHERE avaliacao is not null')
    notas = cur.fetchall()
    total = 0
    for n in notas:
        total = total + n[0]
    media = total/len(notas)
    media = format(media, '.2f')
    return media


def get_evo_info(intervalo, dia_ref):
    now = datetime.now()
    cur = con.cursor()
    if intervalo == 'Hoje':
        inter = dia_ref
        periodo = 1
    elif intervalo == 'Última semana':
        inter = dia_ref - relativedelta(days=7)
        periodo = 8
    elif intervalo == 'Últimos 15 dias':
        inter = dia_ref - relativedelta(days=15)
        periodo = 16
    elif intervalo == 'Último mês':
        inter = dia_ref - relativedelta(months=1)
        periodo = 30
    elif intervalo == 'Tudo':
        cur.execute('SELECT min(data_abertura) AS primeira_solicitacao FROM solicitacao')
        inter = cur.fetchall()
        inter = inter[0][0]
        periodo = (dia_ref - (inter.date())).days
        inter = inter.date()

    cur.execute('SELECT min(data_abertura) AS primeira_solicitacao FROM solicitacao')
    p_soli = cur.fetchall()
    p_soli = p_soli[0][0]
    p_soli = p_soli.date()

    if intervalo != 'Tudo':
        cur.execute('SELECT codigo_solicitacao FROM solicitacao WHERE data_abertura >=%s AND data_abertura <=%s AND data_fechamento IS null', [p_soli, str(inter)+' 23:59:59'])
        cham_abertos_n = len(cur.fetchall())
        cham_fechados_n = 0
    else:
        cham_fechados_n, cham_abertos_n = 0, 0
    evo_cham = []
    for dias in range(periodo):

        cur.execute('SELECT codigo_solicitacao FROM solicitacao WHERE data_abertura >%s AND data_abertura<=%s and (data_fechamento <%s or data_fechamento is null)', [inter, str(inter) + ' 23:59:59', dia_ref])
        cham_abertos = cur.fetchall()
        cur.execute('SELECT codigo_solicitacao FROM solicitacao WHERE data_fechamento >=%s AND data_fechamento<=%s', [inter, str(inter)+' 23:59:59'])
        cham_fechados = cur.fetchall()
        cham_abertos_n = (cham_abertos_n + len(cham_abertos)) - len(cham_fechados)
        cham_fechados_n = cham_fechados_n + len(cham_fechados)
        per_cham = [cham_abertos_n, cham_fechados_n]
        per_cham.append(str(inter).replace('-', '/'))
        evo_cham.append(per_cham)
        inter = inter + relativedelta(days=1)
    return evo_cham



def get_pie_info(intervalo, dia_ref):
    if intervalo == 'Hoje':
        inter = dia_ref
    elif intervalo == 'Última semana':
        inter = dia_ref - relativedelta(days=7)
    elif intervalo == 'Últimos 15 dias':
        inter = dia_ref - relativedelta(days=15)
    elif intervalo == 'Último mês':
        inter = dia_ref - relativedelta(months=1)
    elif intervalo == 'Tudo':
        inter = '0000-00-00'
    

    cur = con.cursor()
    cur.execute('SELECT codigo_solicitacao FROM solicitacao WHERE data_abertura >%s AND data_abertura<=%s and (data_fechamento >%s or data_fechamento is null)', [inter, str(dia_ref) + ' 23:59:59', dia_ref])
    cham_abertos = cur.fetchall()
    cur.execute('select codigo_solicitacao from solicitacao where data_abertura >%s and data_abertura <%s and data_fechamento<%s', [inter, dia_ref, dia_ref])
    cham_fechados = cur.fetchall()
    per_cham = [len(cham_abertos), len(cham_fechados)]
    if per_cham == [0, 0]:
        return 'Não houve soilictações durante esse periodo'
    return per_cham
#----------------------------------------------------


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
    cur.execute(verifica_funcao, [cod])
    funcao = cur.fetchall()

    cur = mysql.connection.cursor()  
    cur.execute('SELECT codigo_usuario FROM usuarios WHERE funcao=%s', [2])
    executores_ativos = cur.fetchall()
    if executores_ativos == ():
        print(executores_ativos)

        aviso = 2

        for f in funcao: 
            if f[0] == 3:
                return render_template('adm_nova_soli.html', aviso=aviso)
            else:
                cur = mysql.connection.cursor()  
                users = cur.execute(historico, [cod])
                lista = cur.fetchall()
                return render_template("telausuario.html", lista=lista, aviso=aviso)
    else:

        cur.execute(quantia_tec)
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
        con.commit()

        aviso = 1

        for f in funcao: 
            if f[0] == 3:
                return render_template('adm_nova_soli.html', aviso=aviso)
            else:
                cur = mysql.connection.cursor()  
                users = cur.execute(historico, [cod])
                lista = cur.fetchall()
                return render_template("telausuario.html", lista=lista, aviso=aviso)


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
            return redirect ('/solicitacoes')
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
    cur.execute('SELECT codigo_usuario FROM usuarios WHERE codigo_usuario!=%s AND funcao=%s', [id, 2])
    executores_ativos = cur.fetchall()
    if executores_ativos == ():
        return redirect("/usuarios_erro")
    else:
        a = cur.execute(quantia_tec)
        max_cont = int(str(cur.fetchall()).strip('(,)'))


        cur = mysql.connection.cursor()
        cur.execute('SELECT codigo_usuario, contador_solicitacao FROM usuarios WHERE funcao=%s', [2])
        tec_cont_soli = cur.fetchall()


        # ------------------------------
        cur = con.cursor()
        cur.execute('SELECT codigo_solicitacao FROM solicitacao WHERE codigo_usuario=%s  AND _status=%s', [id,'Aberto'])
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

        if max_cont != cod_cont-1:
        
            for contador_tecs in range(max_cont):
                #print (contador_tecs)
                if cod_cont < contador_tecs:
                
                    x = contador_tecs-1

                    cur = con.cursor()
                    cur.execute('UPDATE usuarios SET contador_solicitacao=%s WHERE contador_solicitacao=%s', [x,contador_tecs])
            con.commit()


    # ------------------------------

        return redirect("/usuarioss")

@app.route('/usuarios_erro')
def falta_tec():

    cur = mysql.connection.cursor()
    cur.execute("select * FROM usuarios;")
    usuarios = cur.fetchall()

    aviso = "*O sistema precisa ter ao menos um técnico!"

    return render_template('adm_usuarios.html', usuarios=usuarios, aviso=aviso)



#FUNÇÕES DE AVALIAÇÃO----------------------------------------------FUNÇÕES DE AVALIAÇÃO-------------------------------------------------
@app.route('/avaliacao_solicitacao/<cod_soli>', methods= ['POST']) 
def avaliacao_solicitacao(cod_soli):

    nota = request.form['rate']


    cur = con.cursor()
    cur.execute("UPDATE solicitacao SET avaliacao=%s WHERE codigo_solicitacao = %s", [nota,cod_soli])
    feedback = cur.fetchall
    con.commit()

    if check_func('3'):
        return redirect ('/historico')
    else:
        return redirect ('/telausuario')