create database usuarios_solicitacoes;

use usuarios_solicitacoes;
create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    senha_usuario varchar(30) NOT NULL);

select * from usuarios;



create table chamado
(	codigo_solicitacao int primary key AUTO_INCREMENT,
	solicitacao varchar(300),
	email_usuario varchar(40) NOT NULL,
    data_inicio DATE not null );
ALTER TABLE solicitacao ADD CONSTRAINT email_usuario FOREIGN KEY ( email_usuario ) REFERENCES usuarios ( email_usuario ) ;

select * from chamado;