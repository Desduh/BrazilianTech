create database usuarios_solicitacoes;

use usuarios_solicitacoes;
create table usuarios
(	codigo_usuario int primary key AUTO_INCREMENT,
	email_usuario varchar(40) NOT NULL UNIQUE KEY,
    senha_usuario varchar(30) NOT NULL);

select * from usuarios;

create table chamado
(	codigo_solicitacao int primary key AUTO_INCREMENT,
	solicitacao varchar(1000),
	email_usuario varchar(40),
    data_inicio datetime );

select * from chamado;
select codigo_solicitacao,solicitacao,email_usuario,data_inicio FROM chamado ORDER BY data_inicio DESC;


