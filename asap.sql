-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-08-2024 a las 22:06:25
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
  `nombre_departamento` int(11) NOT NULL,
  `id_empresa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_plan`
--

CREATE TABLE `movimientos_plan` (
  `id_plan_cuentas` int(11) NOT NULL,
  `id_registro` int(11) NOT NULL,
  `id_movimientos_plan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

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
  `saldo` float NOT NULL,
  `id_movimiento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

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
  ADD PRIMARY KEY (`id_plan_cuentas`);

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
  MODIFY `id_cuenta_contable` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_principales`
--
ALTER TABLE `cuentas_principales`
  MODIFY `id_cuentas_principales` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id_departamento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empresas`
--
ALTER TABLE `empresas`
  MODIFY `id_empresas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `movimientos_plan`
--
ALTER TABLE `movimientos_plan`
  MODIFY `id_movimientos_plan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `movimientos_usuarios`
--
ALTER TABLE `movimientos_usuarios`
  MODIFY `id_movimientos_usuarios` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  MODIFY `id_plan_cuentas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  MODIFY `id_registros_movimientos` int(11) NOT NULL AUTO_INCREMENT;

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
