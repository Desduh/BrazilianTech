create database usuarios_solicitacoes;

use usuarios_solicitacoes;


create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email varchar(40) NOT NULL UNIQUE KEY,
    senha varchar(30) NOT NULL,
    funcao int,
    contador_solicitacao int unique key);


create table solicitacao
(	codigo_solicitacao int primary key AUTO_INCREMENT,
	descricao varchar(1000),
	codigo_usuario_cli int,
    foreign key(codigo_usuario_cli) REFERENCES usuarios (codigo_usuario),
    data_abertura datetime,
    codigo_usuario int,
    foreign key(codigo_usuario) REFERENCES usuarios (codigo_usuario),
    _status varchar(30),
    constraint ck_status check(_status in('Aceito','Negado','Aberto')),
	resposta varchar(1000),
    data_fechamento datetime,
    tipo_problema varchar(40),
    avaliacao int
    constraint ck_avaliacao check(0 < avaliacao <= 6)); 