-- DataDialogue AI - Script de creación de base de datos bancaria
-- Ejecutar en Supabase SQL Editor

CREATE TABLE IF NOT EXISTS ciudad (
    id_ciudad SERIAL PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    id_ciudad INTEGER REFERENCES ciudad(id_ciudad),
    telefono VARCHAR(20),
    correo VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS cuentas (
    id_cuenta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    tipo_cuenta VARCHAR(20) CHECK (tipo_cuenta IN ('Ahorros', 'Corriente')) NOT NULL,
    saldo NUMERIC(15, 2) DEFAULT 0,
    fecha_apertura DATE NOT NULL,
    estado VARCHAR(10) CHECK (estado IN ('Activa', 'Inactiva')) DEFAULT 'Activa'
);

CREATE TABLE IF NOT EXISTS movimientos (
    id_movimiento SERIAL PRIMARY KEY,
    id_cuenta INTEGER REFERENCES cuentas(id_cuenta),
    fecha_movimiento TIMESTAMP NOT NULL DEFAULT NOW(),
    tipo_movimiento VARCHAR(20) CHECK (tipo_movimiento IN ('Depósito', 'Retiro', 'Transferencia')) NOT NULL,
    valor NUMERIC(15, 2) NOT NULL,
    descripcion TEXT
);

-- Datos de ciudades
INSERT INTO ciudad (nombre_ciudad, departamento) VALUES
    ('Bogotá', 'Cundinamarca'),
    ('Medellín', 'Antioquia'),
    ('Cali', 'Valle del Cauca'),
    ('Manizales', 'Caldas'),
    ('Barranquilla', 'Atlántico'),
    ('Bucaramanga', 'Santander');

-- Datos de clientes
INSERT INTO clientes (nombre, apellido, documento, fecha_nacimiento, id_ciudad, telefono, correo) VALUES
    ('Carlos', 'Ramírez', '1020304050', '1990-03-15', 1, '3001234567', 'carlos.ramirez@email.com'),
    ('Laura', 'Gómez', '1030405060', '1985-07-22', 2, '3109876543', 'laura.gomez@email.com'),
    ('Andrés', 'Martínez', '1040506070', '1992-11-08', 3, '3205551234', 'andres.martinez@email.com'),
    ('Valentina', 'Torres', '1050607080', '1988-01-30', 4, '3157894561', 'valentina.torres@email.com'),
    ('Sebastián', 'Herrera', '1060708090', '1995-09-17', 5, '3004567890', 'sebastian.herrera@email.com'),
    ('María', 'López', '1070809100', '1993-05-25', 6, '3213456789', 'maria.lopez@email.com');

-- Datos de cuentas
INSERT INTO cuentas (id_cliente, tipo_cuenta, saldo, fecha_apertura, estado) VALUES
    (1, 'Ahorros',   1500000.00, '2020-01-15', 'Activa'),
    (1, 'Corriente',  800000.00, '2021-06-01', 'Activa'),
    (2, 'Ahorros',   3200000.00, '2019-03-10', 'Activa'),
    (3, 'Corriente', 5000000.00, '2018-08-22', 'Activa'),
    (4, 'Ahorros',    450000.00, '2022-02-14', 'Activa'),
    (5, 'Ahorros',   2750000.00, '2020-11-30', 'Inactiva'),
    (6, 'Corriente', 1200000.00, '2023-01-05', 'Activa');

-- Datos de movimientos
INSERT INTO movimientos (id_cuenta, fecha_movimiento, tipo_movimiento, valor, descripcion) VALUES
    (1, '2024-01-10 09:00:00', 'Depósito',      500000.00, 'Consignación nómina enero'),
    (1, '2024-01-15 14:30:00', 'Retiro',         200000.00, 'Retiro cajero automático'),
    (2, '2024-01-20 11:00:00', 'Transferencia',  300000.00, 'Pago arriendo'),
    (3, '2024-02-05 10:15:00', 'Depósito',      1000000.00, 'Ahorro mensual'),
    (3, '2024-02-12 16:00:00', 'Retiro',          150000.00, 'Compra supermercado'),
    (4, '2024-02-18 08:30:00', 'Depósito',      2000000.00, 'Consignación empresa'),
    (5, '2024-03-01 13:45:00', 'Retiro',          100000.00, 'Servicio público'),
    (6, '2024-03-10 09:00:00', 'Depósito',       750000.00, 'Pago freelance'),
    (7, '2024-03-15 11:30:00', 'Transferencia',   400000.00, 'Pago factura'),
    (1, '2024-03-20 15:00:00', 'Depósito',        600000.00, 'Bono extra');
