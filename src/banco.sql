create database usuarios_solicitacoes;

use usuarios_solicitacoes;


create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    senha_usuario varchar(30) NOT NULL,
    funcao int,
    contador_solicitacao int);
    
insert into usuarios(email_usuario,senha_usuario,funcao) values("administrador@adm","fatec",3);
    

create table solicitacao
(	codigo_solicitacao int primary key AUTO_INCREMENT,
	descricao varchar(1000),
	email_usuario varchar(40),
    foreign key(email_usuario) REFERENCES usuarios (email_usuario),
    data_abertura datetime,
    codigo_usuario int,
    foreign key(codigo_usuario) REFERENCES usuarios (codigo_usuario),
    _status varchar(30),
    constraint ck_status check(_status in('Aceito','Negado','Aberto')),
	resposta varchar(1000),
    data_fechamento datetime,
    tipo_problema varchar(40)); 