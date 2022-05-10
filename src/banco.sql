create database usuarios_solicitacoes;

use usuarios_solicitacoes;


create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    senha_usuario varchar(30) NOT NULL,
    funcao int);
    
insert into usuarios(email_usuario,senha_usuario,funcao) values("administrador@adm","fatec",3);


create table distribuicao
(   executor int primary key,
    foreign key(executor) REFERENCES usuarios (codigo_usuario),
    contador int);
    

create table chamado
(	codigo_solicitacao int primary key AUTO_INCREMENT,
	solicitacao varchar(1000),
	email_usuario varchar(40),
    data_inicio datetime,
    executor int,
    foreign key(executor) REFERENCES destribuicao (executor),
    _status varchar(30),
    constraint ck_status check(_status in('Aceito','Negado','Aberto')),
	resposta varchar(1000),
    data_fechamento datetime,
    problema varchar(40));    