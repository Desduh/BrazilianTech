<div align='center'>
<h1> FATEC SJC - Profº Jessen Vidal- 1º DSM</h1>
<img src="src\static\imagens\logo.png" style="zoom:25%;" />
</div>


<h2 align="center"> Grupo 5 - BrazilianTech💻</h2>
<div align='center'> <a href='#-descrição-do-projeto-'>Descrição do Projeto </a> |  <a href='#-execução-'>Execução</a> | <a href='#-sobre-o-site-'>Sobre o site</a> |<a href='#-requisitos'>Requisitos</a> | <a href='#-backlog-do-produto-'>Backlog</a> | <a href='#-histórias-de-usuários-'>Histórias de Usuários</a> | <a href='#-gráficos-de-burndown'>Gráficos de Burndown</a> | <a href='#-tecnologias'>Tecnologias</a> | <a href='#-equipe-'> Equipe </a> | <a href='#-vídeos-'>Vídeos</a> </div>

<br>

<h2> 📚Descrição do Projeto </h2>
<p> Este projeto tem por objetivo desenvolvimento de uma plataforma de central de serviços para que a empresa cliente possa receber, atender e recusar serviços.</p> 
<p>Organização do repositório:</p>  
<p> Pasta Src: pasta templates contém as páginas do site; pasta static contém as imagens e os arquivos de estilização em css; arquivo app.py com os códigos de python; arquivo banco.sql com o script do banco de dados; e o arquivo requirements.txt; </p>
<p> Pasta doc/BD: contento os modelos do banco de dados(conceitual e lógico)</p>
<p>  README.MD: arquivo com o detalhamento do projeto.</p>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>🖥 Execução </h2>

-Criar uma pasta

-Clonar o git dentro dessa pasta com:

```console 
	git clone https://github.com/Desduh/BrazilianTech.git
```

-Baixar o python, o Visual Code Studio e o MySQL

-Abrir a pasta no Visual code, entrar no prompt de comando pelo terminal e digitar 

```console 
	cd BrazilianTech
```

```console 
	cd src
```

```console 
	python -m venv venv
```

```console 
	venv\scripts\activate
```

```console 
	pip install -r requirements.txt
```

<br>
-Ir no MySQL Workbench > open script > banco.sql > adiconar um  e-mail e uma senha para o  administrador > executar linhas
<img src="src\static\imagens\print_db.png" />
<br>
-Retornar ao  Visual Code e alterar as informações sobre o banco:
<img src="src\static\imagens\print_apppy.png" />
<br>
-Retornar ao prompt de comando do terminal e digite:

```console 
	flask run
```
-Abra o link

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>🔍 Sobre o site </h2>

Nossa site  irá facilitar a comunicação entre os clientes e técnicos, pois conecta as pessoas que necessitam de suporte, seja ele: software ou hardware a um profissional da área de TI, onde os mesmos podem solicitar um pedido ou ver seus pedidos anteriores e tais pedidos são disponibilizados aos profissionais, que solucionarão o problema.

Vale destacar que o administrador deve promover ao menos um usuário para técnico (aba usuários -> promover) antes de uma solicitação ser criada:

Templates clientes:

<img src="src\static\imagens\usuario.gif" />

Templates técnicos:

<img src="src\static\imagens\tecnico.gif" />

Templates administrador:

<img src="src\static\imagens\administrador.gif" />

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>📜 Requisitos</h2>

|                            | REQUISITOS FUNCIONAIS                                        |
| :------------------------- | :----------------------------------------------------------- |
| <strong>RF.1.</strong>     | O sistema só deverá ser acessado por pessoas devidamente cadastradas; |
| <strong>RF.2.</strong>     | Apenas o administrador do sistema deve possuir acesso total às funcionalidades do sistema; |
| <strong>RF.3.</strong>     | O técnico deve ser capaz de atender e recusar chamados(caso recuse é necessário que  possa justificar); |
| <strong>RF.4.</strong>     | Um usuário deve ser capaz de abrir uma solicitação, visualizar o estado, da mais recente à mais antiga e atribuir uma nota pelo serviço; |
| <strong>RF.5 E 7.</strong> | Ao ser criada, um chamado deve ser atrelada seu criador e atribuída um técnico; |
| <strong>RF.6.</strong>     | Atribuíção do técnico deve seguir um esquema de distribuição cíclica; |
| <strong>RF.8.</strong>     | Solicitação: data/hora de criação e fechamento, tipo de problema ou esclarecimento, uma descrição, uma imagem/arquivo (opcional), uma resposta/justificativa para o fechamento e uma avaliação atribuída pelo usuário a originou, após o fechamento (opcional); |
| <strong>RF.9.</strong>     | Relátorios sobre o percentual de solicitações abertas e fechadas em um intervalo de tempo, a evolução diária da quantidade de solicitações abertas e fechadas em intervalos de tempo especificados, uma média de cada técnico e uma média global do sistema. |

<br>

|                          | REQUISITOS NÃO FUNCIONAIS                                    |
| ------------------------ | ------------------------------------------------------------ |
| <strong>RN.P.1.</strong> | Desenvolver o back end com alinguagem Python 3+ e o microframework Flask; |
| <strong>RN.P.2.</strong> | Utilizar o sistema gerenciador de banco de dados MariaDB/MySQL; |
| <strong>RN.P.3.</strong> | Utilizar HTML 5 para arquitetura da informação da aplicação; |
| <strong>RN.P.4.</strong> | Utilizar  CSS  3para  especificação  do  layout  e  demais  características  de  renderização  da interface. |
| <strong>RN.P.5.</strong> | Utilizar o GitHub para controle de versão dos artefatos de projeto. |
| <strong>RN.P.6.</strong> | Interface com navegação intuitiva (e.g. acesso à informação com poucos “cliques”); |
| <strong>RN.P.7.</strong> | Sistema responsivo.                                          |
| <strong>RN.P.8.</strong> | Utilizar JavaScript no front end                             |

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>


<h2>📃 Backlog do produto </h2>

| Sprint |   Requisito   | Etapas                                                       | Status |
| ------ | :-----------: | ------------------------------------------------------------ | ------ |
| 1      |       -       | Wireframe                                                    | ✅      |
| 1      | RN.P.3/RN.P.4 | Templates                                                    | ✅      |
| 1      |    RN.P.1     | Flask                                                        | ✅      |
| 1      |    RN.P.4     | Estilização básica das paginas com CSS                       | ✅      |
| 1      |    RN.P.2     | Criação do modelo conceitual e Lógico                        | ✅      |
| 1      |    RN.P.2     | Criação da tabela de usuários no MYSQL                       | ✅      |
| 1      |    RN.P.1     | Criação das funções para cadastro e login com Python         | ✅      |
| 1      |    RN.P.2     | Criação da tabela de solicitações no MYSQL                   | ✅      |
| 1      |    RN.P.1     | Criação das funções de solicitações com Python               | ✅      |
| 1      |    RN.P.1     | Conexão dos dados do banco com o front-end por meio do Python | ✅      |
| 1      |       -       | Criação do READ.ME - 1ºsprint                                | ✅      |
| 1      |       -       | Vídeo - 1º sprint                                            | ✅      |
| 2      |     RF.3      | Atender e recusar solicitações                               | ✅      |
| 2      |     RF.4      | Usuário ser capaz de visualizar as suas solicitações e  o status delas | ✅      |
| 2      |     RF.2      | Página do Administrador                                      | ✅      |
| 2      |     RF.9      | Gráfico 1: percentual de solicitações abertas e fechadas     | ✅      |
| 2      |     RF.6      | Função cíclica das solicitações                              | ✅      |
| 2      |     RF.4      | Organizar solicitações da mais nova para as mais antigas     | ✅      |
| 2      |    RN.P.4     | Complemento da estilização dos templates                     | ✅      |
| 2      |       -       | Criação do READ.ME - 2ºsprint                                | ✅      |
| 2      |       -       | Vídeo - 2º sprint                                            | ✅      |
| 3      |     RF.4      | Cliente ser capaz de avaliar o serviço                       | ❌      |
| 3      |    RN.P.7     | Responsivo                                                   | ❌      |
| 3      |     RF.9      | Alteração do gráfico do percentual de solicitações abertas e fechadas, considerando agora um determinado intervalo de tempo | ✅      |
| 3      |     RF.9      | Gráfico 2: evolução diária da quantidade de solicitações abertas e fechadas em intervalos de tempo especificados | ❌      |
| 3      |     RF.9      | Avaliação média de cada técnico.                             | ✅      |
| 3      |     RF.9      | Avaliação média global do sistema.                           | ✅      |
| 3      |    RN.P.4     | Estilização final do projeto                                 | ❌      |
| 3      |       -       | Criação do READ.ME - 3ºsprint                                | ❌      |
| 3      |       -       | Vídeo - 3º sprint                                            | ❌      |

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>🙋‍ Histórias de Usuários </h2>

​    <img src="src\static\imagens\users_stories.png" />

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>📉 Gráficos de Burndown</h2>

<img src="src\static\imagens\Burndown1.png">

<br>

<img src="src\static\imagens\Burndown2.png">

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>



<h1>🛠 Tecnologias:</h1>
<div align='center'>
	<h3>Linguagem Folha de Estilo:</h3>
	<ol><h4>Css3</h4></ol>
	<img src="src\static\imagens\CSS3.png" alt="CSS3" width="250px" >
</div>


<br>

<div align='center'>
	<h3>Linguagem de Marcação:</h3>
	<ol><h4>Html5</h4></ol>
	<img src="src\static\imagens\HTML5.png" alt="HTML5" width="250px" >
</div>


<br>

<div align='center'>
	<h3>Linguagem de Banco de Dados:</h3>
	<ol><h4>MySQL</h4></ol>
	<img src="src\static\imagens\MySQL.png" alt="HTML5" width="300px" > 
</div>

<br>

<div align='center'>
    <h3>Linguagens de Programação:</h3>
	<ol><h4>Python JavaScript</h4></ol>
	<img src="src\static\imagens\linguagens.png" alt="Linguagens"> 
</div>
<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>👨‍👨‍👧‍👧 Equipe </h2>

| Cargo            | Membros                      |                          GitHub                           |
| :--------------- | :--------------------------- | :-------------------------------------------------------: |
| P.O              | Júlia Sousa Gayotto          |    <a href='https://github.com/JuliaGayotto'>Link</a>     |
| Scrum Master     | Carlos Eduardo Falandes      |       <a href='https://github.com/Desduh'>Link</a>        |
| Development Team | Ana Clara Marques Portes     |      <a href='https://github.com/AnaMarks'>Link</a>       |
| Development Team | Bruno Henrique Menezes Ramos |   <a href='https://github.com/BrunoHenriique'>Link</a>    |
| Development Team | Lucas França Registro        | <a href='https://github.com/LucasFrancaRegistro'>Link</a> |

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

<br>

<h2>🎬 Vídeos </h2>

<p>Assista nossos vídeos, neles contém explicaçôes mais detalhadas sobre o projeto.</p>

-Sprint 1: clique <a href='https://youtu.be/A1cXFDZgTSA'>aqui</a> 

-Sprint 2: clique <a href='https://youtu.be/YaW2hexfnQ4'>aqui</a>

-Sprint 3: clique aqui

<br>

<a href="#-grupo-5---braziliantech">--> voltar ao menu</a>

