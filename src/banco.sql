create database usuarios_solicitacoes;

use usuarios_solicitacoes;

create table funcoes
(	cod_func int primary key,
	descricao varchar(50) NOT NULL);
    
insert into funcoes values(1,"Possibilita fazer chamados");
insert into funcoes values(2,"Possibilita responder chamados");
insert into funcoes values(3,"Ambas atividades anteriores e ver relatórios");


create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    senha_usuario varchar(30) NOT NULL,
    funcao int,
    foreign key(funcao) REFERENCES funcoes (cod_func));
    

create table chamado
(	codigo_solicitacao int primary key AUTO_INCREMENT,
	solicitacao varchar(1000),
	email_usuario varchar(40),
    data_inicio datetime,
    email_executor varchar(40),
    _status varchar(30),
    constraint ck_status check(_status in('Aceito','Negado','Aberto')),
	resposta varchar(1000),
    data_fechamento datetime,
    problema varchar(40));