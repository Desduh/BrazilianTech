<div align='center'>
<h1> FATEC SJC - Profº Jessen Vidal- 1º DSM</h1>
<img src="src\static\imagens\logo_nome.png" style="zoom:50%;" />
</div>


<h2 align="center"> Grupo 5 - BrazilianTech💻</h2>
<div align='center'> <a href='#Descrição do Projeto'>Descrição do Projeto </a> |  <a href='#Execução'>Execução</a> |<a href='#Requisitos'>Requisitos</a> | <a href='#Backlog'>Backlog</a> | <a href='#Tecnologias'>Tecnologias</a> | <a href='#Equipe'> Equipe </a> | <a href='#Vídeo'>Vídeo</a> | <a href='#Sobre o site'>Sobre o site</a></div>
<h3 align="center"> CENTRAL DE SERVIÇOS </h3>

<br>

<h2> Descrição do Projeto </h2>
<p> Este projeto tem por objetivo desenvolvimento de uma plataforma de central de serviços para que a empresa cliente possa receber, atender e recusar serviços.</p> 
<p>Organização do repositório:</p>  
<p> Pasta Src: contendos a pasta Templates, com páginas do site, a pasta Static, com os arquivos estáticos, o arquivo app.py com os códigos de python, o arquivo banco.sql, com as tabelas do Banco de Dados e o arquivo requirements.txt; </p>
<p>  README.MD: arquivo com o detalhamento do projeto.</p>

<br>

<h2> Execução </h2>

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
	.\venv\scripts\activate
```

```console 
	cd ..
```

```console 
	cd ..
```

```console 
	pip install -r  requirements.txt
```

<br>
-Ir no MySQL Workbench > open script > Banco.sql > executar linhas
<img src="src\static\imagens\print_db.png" />
<br>
-Retornar ao  Visual Code e alterar as informações sobre o banco:
<img src="src\static\imagens\print_html.png" />
<br>
-Retornar ao prompt de comando do terminal e digite:

```console 
	flask run
```
-Abra o link

<br>

<h2> Sobre o site </h2>
Assim que estiver pronto, nossa página irá facilitar os problemas descritos pelos usuários, tendo como objetivo a melhoria da comunicação entre cliente e executor, nossa página conecta as pessoas que necessitam de suporte, seja ele: software ou hardware a um profissional da área de TI, atravez de um chate, onde a mesma pode solicitar um pedido ou ver seus pedidos anteriores, tais pedidos são disponibilizados aos profissionais, que solucionarão o problema.
<br>
<img align='center' src=src\static\imagens\usuario.gif />
<br>
<img align='center' src=src\static\imagens\executor.gif />

<br>

<h2>Requisitos</h2>
<p> - O sistema só deverá ser acessado por pessoas devidamente cadastradas; <br>
    - Apenas o administrador do sistema deve possuir acesso total às funcionalidades do sistema; <br>
   	- Ao ser criada, um chamado deve ser atrelada seu criador e atribuída um executor; <br>
   	- Atribuíção do executor deve seguir um esquema de distribuição cíclica; <br>
   	- O executor deve ser capaz de atender e recusar chamados(caso recuse é necessário que  possa justificar); <br>
   	- Um usuário comum deve ser capaz de abrir uma solicitação, visualizar o estado de todas as suas solicitações, da mais recente à mais antiga e atribuir uma nota (de 0 a 10)  pelo serviço após realizado; <br>
   	- Requisitos da solicitação:<br>
   			- data/hora de criação(obrigatório); <br>
   		- data/hora de fechamento(obrigatório); <br>
   		- tipo de problema ou Esclarecimento/Informação; <br>
   		-  uma descrição de abertura(obrigatório); <br>
   		-  uma imagem/arquivo (opcional);<br>
   		-  uma resposta ou justificativa para o fechamento(obrigatório); <br>
   		-  uma avaliação atribuída pelo usuário que a originou, após o fechamento (opcional); <br>
   	-O sistema deve prover relátorios sobre o percentual de solicitações abertas e fechadas em um intervalo de tempo, a evolução diária da quantidade de solicitações abertas e fechadas em intervalos de tempo especificados, uma média de cada executor e uma média global do sistema<p>

<br>
​    
<h2>📃 Backlog do produto </h2>

| Sprint | Etapas                                                       | Status |
| ------ | ------------------------------------------------------------ | ------ |
| 1      | Wireframe                                                    | ✅      |
| 1      | Templates                                                    | ✅      |
| 1      | Flask                                                        | ✅      |
| 1      | Estilização básica das paginas com CSS                       | ✅      |
| 1      | Criação da tabela de cadastro no MYSQL                       | ✅      |
| 1      | Criação das funções para cadastro com Python                 | ✅      |
| 1      | Criação da tabela de chamados no MYSQL                       | ✅      |
| 1      | Criação das funções de chamados com Python                   | ✅      |
| 1      | Conexão dos dados do banco com o front-end                   | ✅      |
| 1      | Criação do READ.ME - 1ºsprint                                | ✅      |
| 1      | Vídeo - 1º sprint                                            | ✅      |
| 2      | Atender e recusar chamados                                   | ❌      |
| 2      | Página do Administrador                                      | ❌      |
| 2      | Organizar chats do mais novo pro mais antigo                 | ❌      |
| 2      | Usuário ser capaz de visualizar os seus chamados e  o status deles | ❌      |
| 2      | Distribuir os chamados para mais de um executor              | ❌      |
| 2      | Criação do READ.ME - 2ºsprint                                | ❌      |
| 2      | Vídeo - 2º sprint                                            | ❌      |
| 3      | Usuário ser capaz de avaliar o serviço                       | ❌      |
| 3      | Complemento da estilização da página de chamados             | ❌      |
| 3      | Gráfico 1: percentual de solicitações abertas e fechadas em um determinado intervalo de tempo | ❌      |
| 3      | Gráfico 2: evolução diária da quantidade de solicitações abertas e fechadas em intervalos de tempo especificados | ❌      |
| 3      | Avaliação média de cada executor.                            | ❌      |
| 3      | Avaliação média global do sistema.                           | ❌      |
| 3      | Estilização final do projeto                                 | ❌      |
| 3      | Criação do READ.ME - 3ºsprint                                | ❌      |
| 3      | Vídeo - 3º sprint                                            | ❌      |

<br>

<h1> Tecnologias:</h1>
<div align='center'>
	<h3>Linguagem Folha de Estilo:</h3>
	<ol><h4>Css3</h4></ol>
	<img src="src\static\imagens\CSS3.png" alt="CSS3" width="300px" >
</div>
<br>
<div align='center'>
	<h3>Linguagem de Marcação:</h3>
	<ol><h4>Html5</h4></ol>
	<img src="src\static\imagens\HTML5.png" alt="HTML5" width="300px" >
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

<h2> Equipe </h2>

| Cargo            | Membros                        |
| :--------------- | ------------------------------ |
| P.O              | Júlia Sousa Gayotto            |
| Scrum Master     | Carlos Eduardo Falandes        |
| Development Team | Ana Clara Marques Pontes       |
| Development Team | Bruno Henrique Menezes Ramos   |
| Development Team | Ian Ferreira Tupinambá Machado |
| Development Team | Lucas França Registro          |


<br>


<h2> Vídeo </h2>

<p>assista nosso vídeo...</p>