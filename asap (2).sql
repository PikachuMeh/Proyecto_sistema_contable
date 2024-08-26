-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-08-2024 a las 22:19:10
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `asap`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asientos_contables`
--

CREATE TABLE `asientos_contables` (
  `id_asiento_contable` int(11) NOT NULL,
  `id_cuenta_contable` int(11) NOT NULL,
  `id_plan_cuentas` int(11) NOT NULL,
  `num_asiento` int(11) NOT NULL,
  `documento_respaldo` text NOT NULL,
  `fecha` date NOT NULL,
  `id_cuentas_principales` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bitacora`
--

CREATE TABLE `bitacora` (
  `id_bitacora` int(11) NOT NULL,
  `fecha_hora` date NOT NULL,
  `accion_realizada` text NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cierre_contable`
--

CREATE TABLE `cierre_contable` (
  `id_cierre_contable` int(11) NOT NULL,
  `estado` varchar(30) NOT NULL,
  `id_plan_cuentas` int(11) NOT NULL,
  `fecha_contable_apertura` date NOT NULL,
  `fecha_contable_cierre` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_contables`
--

CREATE TABLE `cuentas_contables` (
  `id_cuenta_contable` int(11) NOT NULL,
  `codigo` varchar(200) NOT NULL,
  `nombre_cuenta` text NOT NULL,
  `nivel_cuenta` text NOT NULL,
  `tipo_cuenta` text NOT NULL,
  `saldo_normal` float NOT NULL,
  `estado_cuenta` text NOT NULL,
  `id_plan_cuenta` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `cuentas_contables`
--

INSERT INTO `cuentas_contables` (`id_cuenta_contable`, `codigo`, `nombre_cuenta`, `nivel_cuenta`, `tipo_cuenta`, `saldo_normal`, `estado_cuenta`, `id_plan_cuenta`) VALUES
(1, '1', 'ACTIVO', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(2, '1.1', 'ACTIVO CIRCULANTE', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(3, '1.1.1', 'DISPONIBLE', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(4, '1.1.1.01', 'CAJA', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(5, '1.1.1.01.01', 'Caja chica en moneda nacional', 'Nivel calculado', 'Tipo determinado', 10000, 'Activo', 2),
(6, '1.1.1.01.02', 'Caja chica en moneda extranjera', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(7, '1.1.1.01.03.001', 'Caja chica en dólares', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(8, '1.1.1.01.03.002', 'Caja chica en Euros', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(9, '1.1.1.01.03.005', 'Caja chica en otras monedas', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(10, '1.1.1.01.03', 'Caja en moneda nacional', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(11, '1.1.1.01.04', 'Caja en moneda extranjera', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(12, '1.1.1.01.04.001', 'Caja en dólares', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(13, '1.1.1.01.04.002', 'Caja en Pesos', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(14, '1.1.1.01.04.003', 'Caja en Euros', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(15, '1.1.1.01.04.005', 'Caja en otras monedas', 'Nivel calculado', 'Tipo determinado', 0, 'Activo', 2),
(16, '1', 'ACTIVO', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(17, '1.1', 'ACTIVO CIRCULANTE', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(18, '1.1.1', 'DISPONIBLE', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(19, '1.1.1.01', 'CAJA', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(20, '1.1.1.01.01', 'Caja chica en moneda nacional', 'Nivel calculado', 'Activos', 10000, 'Activo', 6),
(21, '1.1.1.01.02', 'Caja chica en moneda extranjera', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(22, '1.1.1.01.03.001', 'Caja chica en dólares', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(23, '1.1.1.01.03.002', 'Caja chica en Euros', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(24, '1.1.1.01.03.005', 'Caja chica en otras monedas', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(25, '1.1.1.01.03', 'Caja en moneda nacional', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(26, '1.1.1.01.04', 'Caja en moneda extranjera', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(27, '1.1.1.01.04.001', 'Caja en dólares', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(28, '1.1.1.01.04.002', 'Caja en Pesos', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(29, '1.1.1.01.04.003', 'Caja en Euros', 'Nivel calculado', 'Activos', 0, 'Activo', 6),
(30, '1.1.1.01.04.005', 'Caja en otras monedas', 'Nivel calculado', 'Activos', 0, 'Activo', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_principales`
--

CREATE TABLE `cuentas_principales` (
  `id_cuentas_principales` int(11) NOT NULL,
  `codigo` varchar(45) NOT NULL,
  `nombre_cuenta` text NOT NULL,
  `nivel_cuenta` text NOT NULL,
  `tipo_cuenta` text NOT NULL,
  `id_cuenta_contable` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamentos`
--

CREATE TABLE `departamentos` (
  `id_departamento` int(11) NOT NULL,
  `nombre_departamento` text NOT NULL,
  `id_empresa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `departamentos`
--

INSERT INTO `departamentos` (`id_departamento`, `nombre_departamento`, `id_empresa`) VALUES
(1, 'ola', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas`
--

CREATE TABLE `empresas` (
  `id_empresas` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `fecha_constitucion` date NOT NULL,
  `rif` varchar(10) NOT NULL,
  `fecha_ejercicio_economico` date NOT NULL,
  `fecha_contable` date NOT NULL,
  `actividad_economica` text NOT NULL,
  `direccion` text NOT NULL,
  `correo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `empresas`
--

INSERT INTO `empresas` (`id_empresas`, `nombre`, `fecha_constitucion`, `rif`, `fecha_ejercicio_economico`, `fecha_contable`, `actividad_economica`, `direccion`, `correo`) VALUES
(1, 'Adrianazo', '0000-00-00', 'J-28371827', '2022-02-22', '0000-00-00', 'Sector Primario', 'Chacao', 'juanmalave.itjo@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_plan`
--

CREATE TABLE `movimientos_plan` (
  `id_plan_cuentas` int(11) NOT NULL,
  `id_registro` int(11) NOT NULL,
  `id_movimientos_plan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `movimientos_plan`
--

INSERT INTO `movimientos_plan` (`id_plan_cuentas`, `id_registro`, `id_movimientos_plan`) VALUES
(2, 7, 1),
(5, 12, 3),
(6, 13, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_usuarios`
--

CREATE TABLE `movimientos_usuarios` (
  `id_movimientos_usuarios` int(11) NOT NULL,
  `id_usuarios` int(11) NOT NULL,
  `id_movimientos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plan_cuentas`
--

CREATE TABLE `plan_cuentas` (
  `id_plan_cuentas` int(11) NOT NULL,
  `codigo` varchar(200) NOT NULL,
  `descripcion_cuenta` text NOT NULL,
  `id_empresas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `plan_cuentas`
--

INSERT INTO `plan_cuentas` (`id_plan_cuentas`, `codigo`, `descripcion_cuenta`, `id_empresas`) VALUES
(2, '2odwFZX4aK44Ml8bBSzX', 'Plan de cuentas para la empresa 1', 1),
(5, 'C0iR0i5vH1WMB6GQomln', 'Plan de cuentas para la empresa 1', 1),
(6, 'Gm13hTLNq4bPp7HUwePg', 'Plan de cuentas para la empresa 1', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros_movimientos`
--

CREATE TABLE `registros_movimientos` (
  `id_registros_movimientos` int(11) NOT NULL,
  `fecha_movimiento` date NOT NULL,
  `id_empresas` int(11) NOT NULL,
  `nro_control` varchar(200) NOT NULL,
  `nro_documentos` varchar(200) NOT NULL,
  `id_departamentos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `registros_movimientos`
--

INSERT INTO `registros_movimientos` (`id_registros_movimientos`, `fecha_movimiento`, `id_empresas`, `nro_control`, `nro_documentos`, `id_departamentos`) VALUES
(2, '2024-08-25', 1, './uploads/ola.xlsx', '001', 1),
(3, '2024-08-25', 1, '001', '001', 1),
(4, '2024-08-25', 1, '001', '001', 1),
(5, '2024-08-25', 1, '001', '001', 1),
(6, '2024-08-25', 1, '001', 'C:\\Users\\JUANPC~1\\AppData\\Local\\Temp\\tmpja10cpnv.xlsx', 1),
(7, '2024-08-25', 1, '001', 'C:\\Users\\JUANPC~1\\AppData\\Local\\Temp\\tmp6jnwv4p1.xlsx', 1),
(8, '2024-08-25', 1, '9DrI4zW7Sn', 'archivos_excel\\WHM5uylyQlOKHW9yNDdq.xlsx', 1),
(9, '2024-08-25', 1, 'aFp6feG7PM', 'archivos_excel\\iZPLFQMsQ17RQJOmeNbi.xlsx', 1),
(10, '2024-08-26', 1, 'D0KTJkJjZD', 'archivos_excel\\iEVxfHYiOltMsoHbedC6.xlsx', 1),
(11, '2024-08-26', 1, 'JJev1mTFB7SyZLLJwinI', 'ruta/a/tu/directorio\\ola.xlsx', 1),
(12, '2024-08-26', 1, 'Wlef0P36VH7g0zFaMASi', 'ruta/a/tu/directorio\\ola.xlsx', 1),
(13, '2024-08-26', 1, '8MPzUhnr2NI4J5WYb83w', 'ruta/a/tu/directorio\\ola.xlsx', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

CREATE TABLE `reportes` (
  `id_reportes` int(11) NOT NULL,
  `tipo_reporte` text NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `formato` text NOT NULL,
  `archivo` text NOT NULL,
  `id_cierre_contable` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuarios` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `correo` varchar(50) NOT NULL,
  `clave` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  ADD PRIMARY KEY (`id_asiento_contable`),
  ADD KEY `fk_cuentas_contables_asiento` (`id_cuenta_contable`),
  ADD KEY `fk_plan_cuentas_asientos` (`id_plan_cuentas`),
  ADD KEY `fk_cuenta_principal_asiento` (`id_cuentas_principales`);

--
-- Indices de la tabla `bitacora`
--
ALTER TABLE `bitacora`
  ADD PRIMARY KEY (`id_bitacora`),
  ADD KEY `fk_bitacora` (`usuario_id`);

--
-- Indices de la tabla `cierre_contable`
--
ALTER TABLE `cierre_contable`
  ADD PRIMARY KEY (`id_cierre_contable`),
  ADD KEY `fk_cierre_contable_plan` (`id_plan_cuentas`);

--
-- Indices de la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  ADD PRIMARY KEY (`id_cuenta_contable`),
  ADD KEY `fk_id_plan_cuentas` (`id_plan_cuenta`);

--
-- Indices de la tabla `cuentas_principales`
--
ALTER TABLE `cuentas_principales`
  ADD PRIMARY KEY (`id_cuentas_principales`),
  ADD KEY `fk_cuentas_contables_principales` (`id_cuenta_contable`);

--
-- Indices de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id_departamento`),
  ADD KEY `fk_empresas_id` (`id_empresa`);

--
-- Indices de la tabla `empresas`
--
ALTER TABLE `empresas`
  ADD PRIMARY KEY (`id_empresas`);

--
-- Indices de la tabla `movimientos_plan`
--
ALTER TABLE `movimientos_plan`
  ADD PRIMARY KEY (`id_movimientos_plan`),
  ADD KEY `fk_id_plan` (`id_plan_cuentas`),
  ADD KEY `fk_id_registro_plan` (`id_registro`);

--
-- Indices de la tabla `movimientos_usuarios`
--
ALTER TABLE `movimientos_usuarios`
  ADD PRIMARY KEY (`id_movimientos_usuarios`),
  ADD KEY `fk_id_movimiento_usuarios` (`id_usuarios`),
  ADD KEY `fk_id_movimiento_registro` (`id_movimientos`);

--
-- Indices de la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  ADD PRIMARY KEY (`id_plan_cuentas`),
  ADD KEY `fk_empresas_plan_cuenta` (`id_empresas`);

--
-- Indices de la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  ADD PRIMARY KEY (`id_registros_movimientos`),
  ADD KEY `fk_id_departamentos` (`id_departamentos`);

--
-- Indices de la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD PRIMARY KEY (`id_reportes`),
  ADD KEY `fk_reportes_cierre` (`id_cierre_contable`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  MODIFY `id_asiento_contable` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `bitacora`
--
ALTER TABLE `bitacora`
  MODIFY `id_bitacora` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cierre_contable`
--
ALTER TABLE `cierre_contable`
  MODIFY `id_cierre_contable` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  MODIFY `id_cuenta_contable` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `cuentas_principales`
--
ALTER TABLE `cuentas_principales`
  MODIFY `id_cuentas_principales` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id_departamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `empresas`
--
ALTER TABLE `empresas`
  MODIFY `id_empresas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `movimientos_plan`
--
ALTER TABLE `movimientos_plan`
  MODIFY `id_movimientos_plan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `movimientos_usuarios`
--
ALTER TABLE `movimientos_usuarios`
  MODIFY `id_movimientos_usuarios` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  MODIFY `id_plan_cuentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  MODIFY `id_registros_movimientos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id_reportes` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  ADD CONSTRAINT `fk_cuenta_principal_asiento` FOREIGN KEY (`id_cuentas_principales`) REFERENCES `cuentas_principales` (`id_cuentas_principales`),
  ADD CONSTRAINT `fk_cuentas_contables_asiento` FOREIGN KEY (`id_cuenta_contable`) REFERENCES `cuentas_contables` (`id_cuenta_contable`),
  ADD CONSTRAINT `fk_plan_cuentas_asientos` FOREIGN KEY (`id_plan_cuentas`) REFERENCES `plan_cuentas` (`id_plan_cuentas`);

--
-- Filtros para la tabla `bitacora`
--
ALTER TABLE `bitacora`
  ADD CONSTRAINT `fk_bitacora` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id_usuarios`);

--
-- Filtros para la tabla `cierre_contable`
--
ALTER TABLE `cierre_contable`
  ADD CONSTRAINT `fk_cierre_contable_plan` FOREIGN KEY (`id_plan_cuentas`) REFERENCES `plan_cuentas` (`id_plan_cuentas`);

--
-- Filtros para la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  ADD CONSTRAINT `fk_id_plan_cuentas` FOREIGN KEY (`id_plan_cuenta`) REFERENCES `plan_cuentas` (`id_plan_cuentas`);

--
-- Filtros para la tabla `cuentas_principales`
--
ALTER TABLE `cuentas_principales`
  ADD CONSTRAINT `fk_cuentas_contables_principales` FOREIGN KEY (`id_cuenta_contable`) REFERENCES `cuentas_contables` (`id_cuenta_contable`);

--
-- Filtros para la tabla `departamentos`
--
ALTER TABLE `departamentos`
  ADD CONSTRAINT `fk_empresas_id` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id_empresas`);

--
-- Filtros para la tabla `movimientos_plan`
--
ALTER TABLE `movimientos_plan`
  ADD CONSTRAINT `fk_id_plan` FOREIGN KEY (`id_plan_cuentas`) REFERENCES `plan_cuentas` (`id_plan_cuentas`),
  ADD CONSTRAINT `fk_id_registro_plan` FOREIGN KEY (`id_registro`) REFERENCES `registros_movimientos` (`id_registros_movimientos`);

--
-- Filtros para la tabla `movimientos_usuarios`
--
ALTER TABLE `movimientos_usuarios`
  ADD CONSTRAINT `fk_id_movimiento_registro` FOREIGN KEY (`id_movimientos`) REFERENCES `registros_movimientos` (`id_registros_movimientos`),
  ADD CONSTRAINT `fk_id_movimiento_usuarios` FOREIGN KEY (`id_usuarios`) REFERENCES `usuarios` (`id_usuarios`);

--
-- Filtros para la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  ADD CONSTRAINT `fk_empresas_plan_cuenta` FOREIGN KEY (`id_empresas`) REFERENCES `empresas` (`id_empresas`);

--
-- Filtros para la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  ADD CONSTRAINT `fk_id_departamentos` FOREIGN KEY (`id_departamentos`) REFERENCES `departamentos` (`id_departamento`);

--
-- Filtros para la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD CONSTRAINT `fk_reportes_cierre` FOREIGN KEY (`id_cierre_contable`) REFERENCES `cierre_contable` (`id_cierre_contable`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
