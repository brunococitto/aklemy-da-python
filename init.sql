DROP TABLE IF EXISTS main;
CREATE TABLE main (id serial PRIMARY KEY, fecha_carga date, cod_localidad integer, id_provincia integer, id_departamento integer, categoria varchar, provincia varchar, localidad varchar, nombre varchar, domicilio varchar, codigo_postal varchar, telefono varchar, mail varchar, web varchar);
DROP TABLE IF EXISTS main_info;
CREATE TABLE main_info (id serial PRIMARY KEY, fecha_carga date, provincia varchar, categoria varchar, fuente varchar, cantidad integer);
DROP TABLE IF EXISTS cinemas_info;
CREATE TABLE cinemas_info (id serial PRIMARY KEY, fecha_carga date, provincia varchar, cantidad_pantallas integer, cantidad_butacas integer, cantidad_espacios_incaa integer);