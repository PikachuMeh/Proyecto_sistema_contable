-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-09-2024 a las 01:08:28
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
  `num_asiento` int(11) NOT NULL,
  `documento_respaldo` text NOT NULL,
  `fecha` date NOT NULL,
  `id_empresas` int(11) NOT NULL,
  `cierre_contable` int(11) NOT NULL,
  `tipo_comprobante` int(11) NOT NULL,
  `id_cuentas_principales` int(11) DEFAULT NULL,
  `periodo_contable_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `asientos_contables`
--

INSERT INTO `asientos_contables` (`id_asiento_contable`, `num_asiento`, `documento_respaldo`, `fecha`, `id_empresas`, `cierre_contable`, `tipo_comprobante`, `id_cuentas_principales`, `periodo_contable_id`) VALUES
(8, 1, '5', '2024-09-01', 3, 1, 1, NULL, NULL),
(9, 2, '6', '2024-09-02', 3, 2, 4, NULL, NULL);

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
  `estado` text NOT NULL,
  `fecha_contable_apertura` date NOT NULL,
  `fecha_contable_cierre` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `cierre_contable`
--

INSERT INTO `cierre_contable` (`id_cierre_contable`, `estado`, `fecha_contable_apertura`, `fecha_contable_cierre`) VALUES
(1, 'Cerrado', '2024-09-01', '2024-09-02'),
(2, 'Abierto', '2024-09-02', '0000-00-00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprobantes`
--

CREATE TABLE `comprobantes` (
  `id_comprobante` int(11) NOT NULL,
  `titulo` text NOT NULL,
  `descripcion` text NOT NULL,
  `fecha` date NOT NULL,
  `archivo` text NOT NULL,
  `tipo_comprobante` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `comprobantes`
--

INSERT INTO `comprobantes` (`id_comprobante`, `titulo`, `descripcion`, `fecha`, `archivo`, `tipo_comprobante`) VALUES
(4, 'Comprobante para el asiento contable 3', 'Descripción del comprobante generado automáticamente.', '2024-09-01', 'uploads/Comprobante_para_asiento_contable_3.xlsx', 2),
(5, 'Comprobante para el asiento contable 1', 'Descripción del comprobante generado automáticamente.', '2024-09-01', 'uploads/Comprobante_para_asiento_contable_1.xlsx', 1),
(6, 'Comprobante para el asiento contable 2', 'Descripción del comprobante generado automáticamente.', '2024-09-02', 'uploads/Comprobante_para_asiento_contable_2.xlsx', 4);

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
(33, '1', 'ACTIVO', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(34, '1.1', 'ACTIVO CIRCULANTE', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(35, '1.1.1', 'DISPONIBLE', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(36, '1.1.1.01', 'CAJA', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(37, '1.1.1.01.01', 'Caja chica en moneda nacional', 'Nivel calculado', 'Activos', 10000, 'Activo', 10),
(38, '1.1.1.01.02', 'Caja chica en moneda extranjera', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(39, '1.1.1.01.03.001', 'Caja chica en dólares', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(40, '1.1.1.01.03.002', 'Caja chica en Euros', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(41, '1.1.1.01.03.005', 'Caja chica en otras monedas', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(42, '1.1.1.01.03', 'Caja en moneda nacional', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(43, '1.1.1.01.04', 'Caja en moneda extranjera', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(44, '1.1.1.01.04.001', 'Caja en dólares', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(45, '1.1.1.01.04.002', 'Caja en Pesos', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(46, '1.1.1.01.04.003', 'Caja en Euros', 'Nivel calculado', 'Activos', 0, 'Activo', 10),
(47, '1.1.1.01.04.005', 'Caja en otras monedas', 'Nivel calculado', 'Activos', 0, 'Activo', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_contables_asientos_contables`
--

CREATE TABLE `cuentas_contables_asientos_contables` (
  `id_asiento_contable` int(11) NOT NULL,
  `id_cuenta_contable` int(11) NOT NULL,
  `saldo` double NOT NULL,
  `tipo_saldo` text NOT NULL,
  `id_cuenta_asiento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `cuentas_contables_asientos_contables`
--

INSERT INTO `cuentas_contables_asientos_contables` (`id_asiento_contable`, `id_cuenta_contable`, `saldo`, `tipo_saldo`, `id_cuenta_asiento`) VALUES
(8, 37, 123, 'debe', 1),
(8, 42, 100, 'haber', 2),
(8, 41, 23, 'haber', 3);

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

--
-- Volcado de datos para la tabla `cuentas_principales`
--

INSERT INTO `cuentas_principales` (`id_cuentas_principales`, `codigo`, `nombre_cuenta`, `nivel_cuenta`, `tipo_cuenta`, `id_cuenta_contable`) VALUES
(21, '1', 'ACTIVO', 'Nivel calculado', 'Activos', 33),
(22, '1.1', 'ACTIVO CIRCULANTE', 'Nivel calculado', 'Activos', 34),
(23, '1.1.1', 'DISPONIBLE', 'Nivel calculado', 'Activos', 35),
(24, '1.1.1.01', 'CAJA', 'Nivel calculado', 'Activos', 36);

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
(2, 'Ventas', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas`
--

CREATE TABLE `empresas` (
  `id_empresas` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `fecha_constitucion` date NOT NULL,
  `rif` varchar(11) NOT NULL,
  `fecha_ejercicio_economico` date NOT NULL,
  `actividad_economica` text NOT NULL,
  `direccion` text NOT NULL,
  `correo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `empresas`
--

INSERT INTO `empresas` (`id_empresas`, `nombre`, `fecha_constitucion`, `rif`, `fecha_ejercicio_economico`, `actividad_economica`, `direccion`, `correo`) VALUES
(1, 'Adrianazo', '0000-00-00', 'J-28371827', '2022-02-22', 'Sector Primario', 'Chacao', 'juanmalave.itjo@gmail.com'),
(2, 'Jade', '2024-07-11', 'J312123131', '2024-07-18', 'coso del coso', 'cdwadcawcd123', 'dacwwcadwcadwdca@gmail.com'),
(3, 'Juan', '2024-07-31', 'J-123131312', '2024-08-09', 'coso del coso', 'dcwawadcdcwawad', 'dacwwcadwcadwdca@gmail.com');

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
(10, 15, 5);

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
-- Estructura de tabla para la tabla `periodos_contables`
--

CREATE TABLE `periodos_contables` (
  `id_periodo_contable` int(11) NOT NULL,
  `id_empresa` int(11) NOT NULL,
  `numero_periodo` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'Abierto'
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
(10, 'tYJuwWlstADd3AHQAlxO', 'Plan de cuentas para la empresa 3', 3);

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
(15, '2024-09-01', 3, '7FCSpCsEEpe706gnI7dF', 'uploads\\ola.xlsx', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

CREATE TABLE `reportes` (
  `id_reportes` int(11) NOT NULL,
  `tipo_reporte` text NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `nivel_detalle` text NOT NULL,
  `formato` text NOT NULL,
  `archivo` text NOT NULL,
  `id_asiento_contable` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_comprobante`
--

CREATE TABLE `tipo_comprobante` (
  `id_tipo_comprobante` int(11) NOT NULL,
  `nombre_comprobante` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `tipo_comprobante`
--

INSERT INTO `tipo_comprobante` (`id_tipo_comprobante`, `nombre_comprobante`) VALUES
(1, 'Asientos Apertura'),
(2, 'Asientos de aporte y proviciones'),
(3, 'Asientos de Ingreso'),
(4, 'Asientos de gastos generales'),
(5, 'Asientos de Gastos Generales'),
(6, 'Asientos de Nomina'),
(7, 'Asientos de Cierre');

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
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `nombre`, `correo`, `clave`) VALUES
(1, 'juan', 'juanes.malave@gmail.com', 'juanes321');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  ADD PRIMARY KEY (`id_asiento_contable`),
  ADD KEY `fk_cuenta_principal_asiento` (`id_cuentas_principales`),
  ADD KEY `fk_asientos_comprobante` (`tipo_comprobante`),
  ADD KEY `fk_cierre_contable_asiento` (`cierre_contable`),
  ADD KEY `fk_asientos_empresas` (`id_empresas`),
  ADD KEY `fk_periodo_contable_asiento` (`periodo_contable_id`);

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
  ADD PRIMARY KEY (`id_cierre_contable`);

--
-- Indices de la tabla `comprobantes`
--
ALTER TABLE `comprobantes`
  ADD PRIMARY KEY (`id_comprobante`);

--
-- Indices de la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  ADD PRIMARY KEY (`id_cuenta_contable`),
  ADD KEY `fk_id_plan_cuentas` (`id_plan_cuenta`);

--
-- Indices de la tabla `cuentas_contables_asientos_contables`
--
ALTER TABLE `cuentas_contables_asientos_contables`
  ADD PRIMARY KEY (`id_cuenta_asiento`),
  ADD KEY `fk_asiento_contable_en_cuenta` (`id_asiento_contable`),
  ADD KEY `fk_cuenta_contable_en_asiento` (`id_cuenta_contable`);

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
-- Indices de la tabla `periodos_contables`
--
ALTER TABLE `periodos_contables`
  ADD PRIMARY KEY (`id_periodo_contable`),
  ADD KEY `id_empresa` (`id_empresa`);

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
  ADD KEY `fk_reportes_id_asiento` (`id_asiento_contable`);

--
-- Indices de la tabla `tipo_comprobante`
--
ALTER TABLE `tipo_comprobante`
  ADD PRIMARY KEY (`id_tipo_comprobante`);

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
  MODIFY `id_asiento_contable` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `bitacora`
--
ALTER TABLE `bitacora`
  MODIFY `id_bitacora` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cierre_contable`
--
ALTER TABLE `cierre_contable`
  MODIFY `id_cierre_contable` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `comprobantes`
--
ALTER TABLE `comprobantes`
  MODIFY `id_comprobante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  MODIFY `id_cuenta_contable` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT de la tabla `cuentas_contables_asientos_contables`
--
ALTER TABLE `cuentas_contables_asientos_contables`
  MODIFY `id_cuenta_asiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `cuentas_principales`
--
ALTER TABLE `cuentas_principales`
  MODIFY `id_cuentas_principales` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id_departamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `empresas`
--
ALTER TABLE `empresas`
  MODIFY `id_empresas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `movimientos_plan`
--
ALTER TABLE `movimientos_plan`
  MODIFY `id_movimientos_plan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `movimientos_usuarios`
--
ALTER TABLE `movimientos_usuarios`
  MODIFY `id_movimientos_usuarios` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `periodos_contables`
--
ALTER TABLE `periodos_contables`
  MODIFY `id_periodo_contable` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  MODIFY `id_plan_cuentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  MODIFY `id_registros_movimientos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id_reportes` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_comprobante`
--
ALTER TABLE `tipo_comprobante`
  MODIFY `id_tipo_comprobante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  ADD CONSTRAINT `fk_asientos_comprobante` FOREIGN KEY (`tipo_comprobante`) REFERENCES `tipo_comprobante` (`id_tipo_comprobante`),
  ADD CONSTRAINT `fk_asientos_empresas` FOREIGN KEY (`id_empresas`) REFERENCES `empresas` (`id_empresas`),
  ADD CONSTRAINT `fk_cierre_contable_asiento` FOREIGN KEY (`cierre_contable`) REFERENCES `cierre_contable` (`id_cierre_contable`),
  ADD CONSTRAINT `fk_cuenta_principal_asiento` FOREIGN KEY (`id_cuentas_principales`) REFERENCES `cuentas_principales` (`id_cuentas_principales`),
  ADD CONSTRAINT `fk_periodo_contable_asiento` FOREIGN KEY (`periodo_contable_id`) REFERENCES `periodos_contables` (`id_periodo_contable`);

--
-- Filtros para la tabla `bitacora`
--
ALTER TABLE `bitacora`
  ADD CONSTRAINT `fk_bitacora` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id_usuarios`);

--
-- Filtros para la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  ADD CONSTRAINT `fk_id_plan_cuentas` FOREIGN KEY (`id_plan_cuenta`) REFERENCES `plan_cuentas` (`id_plan_cuentas`);

--
-- Filtros para la tabla `cuentas_contables_asientos_contables`
--
ALTER TABLE `cuentas_contables_asientos_contables`
  ADD CONSTRAINT `fk_asiento_contable_en_cuenta` FOREIGN KEY (`id_asiento_contable`) REFERENCES `asientos_contables` (`id_asiento_contable`),
  ADD CONSTRAINT `fk_cuenta_contable_en_asiento` FOREIGN KEY (`id_cuenta_contable`) REFERENCES `cuentas_contables` (`id_cuenta_contable`);

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
-- Filtros para la tabla `periodos_contables`
--
ALTER TABLE `periodos_contables`
  ADD CONSTRAINT `periodos_contables_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id_empresas`);

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
  ADD CONSTRAINT `fk_reportes_id_asiento` FOREIGN KEY (`id_asiento_contable`) REFERENCES `asientos_contables` (`id_asiento_contable`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
