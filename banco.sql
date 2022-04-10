create database usuarios_solicitacoes;

use usuarios_solicitacoes;
create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    senha_usuario varchar(30) NOT NULL);

select * from usuarios;


create table solicitacao
(	solicitacao varchar(300) primary key,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    data_inicio DATE not null );
ALTER TABLE solicitacao ADD CONSTRAINT email_usuario FOREIGN KEY ( email_usuario ) REFERENCES usuarios ( email_usuario ) ;

select * from solicitacao;