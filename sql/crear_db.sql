DROP DATABASE IF EXISTS aerolinea;
CREATE DATABASE aerolinea CHARACTER SET utf8mb4;

USE aerolinea;

CREATE TABLE rutas (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_vuelo CHAR(6) UNIQUE NOT NULL,
    origen CHAR(3) NOT NULL,
    destino CHAR(3) NOT NULL,
    distancia_km INT UNSIGNED NOT NULL,
    duracion_min SMALLINT UNSIGNED NOT NULL
);

CREATE TABLE pasajeros (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono INT NOT NULL,
    esta_en_lista_negra BOOLEAN NOT NULL,
    es_vip BOOLEAN NOT NULL
);

CREATE TABLE estados_ventas (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE estados_vuelos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE estados_aviones (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cargos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	descripcion VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE estados_staff (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE estados_tarjetas_embarque (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE tipos_documento (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE roles (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE documentos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_documento VARCHAR(20) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    pais_emision CHAR(3) NOT NULL,
    id_pasajero INT UNSIGNED NOT NULL,
    id_tipo_documento INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_pasajero) REFERENCES pasajeros(id),
    FOREIGN KEY (id_tipo_documento) REFERENCES tipos_documento(id),
    UNIQUE (id_tipo_documento, num_documento, pais_emision)
);

CREATE TABLE aviones (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(10) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    capacidad SMALLINT UNSIGNED NOT NULL,
    autonomia_km SMALLINT UNSIGNED NOT NULL,
    costo_hora_vuelo DECIMAL(10,2) NOT NULL,
    id_estado_actual INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_estado_actual) REFERENCES estados_aviones(id)
);

CREATE TABLE vuelos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_partida_programada DATETIME NOT NULL,
    fecha_arribo_programada DATETIME NOT NULL,
    fecha_partida_real DATETIME,
    fecha_arribo_real DATETIME,
    costo_operativo_usd DECIMAL(10,2) NOT NULL,
    precio_venta_usd DECIMAL(10,2) NOT NULL,
    id_ruta INT UNSIGNED NOT NULL,
    id_avion INT UNSIGNED,
    id_estado_actual INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_ruta) REFERENCES rutas(id),
    FOREIGN KEY (id_avion) REFERENCES aviones(id),
    FOREIGN KEY (id_estado_actual) REFERENCES estados_vuelos(id)
);

CREATE TABLE staff (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    id_cargo_actual INT UNSIGNED NOT NULL,
    id_estado_actual INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_cargo_actual) REFERENCES cargos(id),
    FOREIGN KEY (id_estado_actual) REFERENCES estados_staff(id)
);

CREATE TABLE asignaciones_vuelos (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_rol INT UNSIGNED NOT NULL,
    id_vuelo INT UNSIGNED NOT NULL,
    id_staff INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id),
    FOREIGN KEY (id_vuelo) REFERENCES vuelos(id),
    FOREIGN KEY (id_staff) REFERENCES staff(id),
    UNIQUE (id_rol, id_vuelo, id_staff)
);

CREATE TABLE ventas (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    num_reserva CHAR(6) NOT NULL,
    fecha_venta DATETIME NOT NULL DEFAULT NOW(),
    precio_pagado_usd DECIMAL(10,2) NOT NULL,
    id_vuelo INT UNSIGNED NOT NULL,
    id_estado_actual INT UNSIGNED NOT NULL,
    id_pasajero INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_vuelo) REFERENCES vuelos(id),
    FOREIGN KEY (id_estado_actual) REFERENCES estados_ventas(id),
    FOREIGN KEY (id_pasajero) REFERENCES pasajeros(id)
);

CREATE TABLE tarjetas_embarque (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_emision DATETIME NOT NULL,
    fecha_embarque DATETIME,
    id_estado_actual INT UNSIGNED NOT NULL,
    id_venta INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_estado_actual) REFERENCES estados_tarjetas_embarque(id),
	FOREIGN KEY (id_venta) REFERENCES ventas(id)
);

CREATE TABLE certificaciones_staff (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_staff INT UNSIGNED NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    licencia_hasta DATETIME,
    FOREIGN KEY (id_staff) REFERENCES staff(id)
);

CREATE TABLE historial_cambios (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tabla VARCHAR(100) NOT NULL,
    operacion VARCHAR(100) NOT NULL,
    id_modificado VARCHAR(100) NOT NULL,
    campo VARCHAR(100),
    valor_anterior VARCHAR(100),
    valor_nuevo VARCHAR(100),
    fecha_cambio DATETIME NOT NULL,
    id_staff INT UNSIGNED
);