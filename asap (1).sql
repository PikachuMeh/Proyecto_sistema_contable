-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-07-2024 a las 23:29:58
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

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
  `id_asientos` int(11) NOT NULL,
  `cuentas_contables_id` int(11) NOT NULL,
  `cuentas_contables_empresas_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion_asiento` text NOT NULL,
  `tipo_asiento` text NOT NULL,
  `documento_respaldo` text NOT NULL,
  `plan_cuentas_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asientos_contables`
--

INSERT INTO `asientos_contables` (`id_asientos`, `cuentas_contables_id`, `cuentas_contables_empresas_id`, `fecha`, `descripcion_asiento`, `tipo_asiento`, `documento_respaldo`, `plan_cuentas_id`) VALUES
(1, 2, 1, '2024-07-22', '1', '1', '1', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria`
--

CREATE TABLE `auditoria` (
  `id_auditoria` int(11) NOT NULL,
  `fecha_hora` varchar(45) NOT NULL,
  `accion_realizada` varchar(45) NOT NULL,
  `usuarios_idusuarios` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_contables`
--

CREATE TABLE `cuentas_contables` (
  `id_cuenta_contable` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `descripcion_cuenta` text NOT NULL,
  `nombre_cuenta` text NOT NULL,
  `nivel_cuenta` text NOT NULL,
  `tipo_cuenta` text NOT NULL,
  `saldo_normal` float NOT NULL,
  `estado_cuenta` text NOT NULL,
  `empresas_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cuentas_contables`
--

INSERT INTO `cuentas_contables` (`id_cuenta_contable`, `codigo`, `descripcion_cuenta`, `nombre_cuenta`, `nivel_cuenta`, `tipo_cuenta`, `saldo_normal`, `estado_cuenta`, `empresas_id`) VALUES
(1, 1, '1', '1', '1', '1', 1, 'abierto', 1),
(2, 1, '1', '1', '1', '1', 1, 'abierto', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas`
--

CREATE TABLE `empresas` (
  `id_empresas` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `fecha_constitucion` date NOT NULL,
  `rif` varchar(12) NOT NULL,
  `fecha_ejercicio_economico` date NOT NULL,
  `fecha_contable` date NOT NULL,
  `actividad_economica` varchar(200) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `correo` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empresas`
--

INSERT INTO `empresas` (`id_empresas`, `nombre`, `fecha_constitucion`, `rif`, `fecha_ejercicio_economico`, `fecha_contable`, `actividad_economica`, `direccion`, `correo`) VALUES
(1, 'Adrianazo', '0000-00-00', 'J-37827121', '0000-00-00', '0000-00-00', 'Sector Primario', 'Chacao', 'juanes.malave@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entidad`
--

CREATE TABLE `entidad` (
  `idEntidad` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `rif` varchar(15) NOT NULL,
  `direccion` text NOT NULL,
  `correo` varchar(200) NOT NULL,
  `telefono_contacto` int(11) NOT NULL,
  `persona_contacto` varchar(200) NOT NULL,
  `Tipo_contribuyente` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plan_cuentas`
--

CREATE TABLE `plan_cuentas` (
  `id_plan_cuentas` int(11) NOT NULL,
  `codigo` int(11) NOT NULL,
  `descripcion_cuenta` text NOT NULL,
  `registro_empresas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `plan_cuentas`
--

INSERT INTO `plan_cuentas` (`id_plan_cuentas`, `codigo`, `descripcion_cuenta`, `registro_empresas`) VALUES
(1, 0, 'Plan de cuentas para la empresa 1', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros_movimientos`
--

CREATE TABLE `registros_movimientos` (
  `id_Registros_Movimientos` int(11) NOT NULL,
  `Fecha_movimiento` date NOT NULL,
  `monto` float NOT NULL,
  `Nro_control` varchar(200) NOT NULL,
  `Nro_documento` varchar(200) NOT NULL,
  `Empresas_id` int(11) DEFAULT NULL,
  `entidad_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_reportes`
--

CREATE TABLE `registro_reportes` (
  `id_registro_reporte` int(11) NOT NULL,
  `registro_reporte` int(11) DEFAULT NULL,
  `movimientos_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

CREATE TABLE `reportes` (
  `id_reporte` int(11) NOT NULL,
  `tipo_reporte` varchar(200) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `nivel_detalle` text NOT NULL,
  `formato` text NOT NULL,
  `archivo` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `descripcion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `descripcion`) VALUES
(1, 'Administrador'),
(2, 'Visitante'),
(3, 'Visualizacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_cuentas`
--

CREATE TABLE `tipos_cuentas` (
  `id_tipo_cuenta` int(11) NOT NULL,
  `nombre_tipo` text NOT NULL,
  `codigo_tipo` int(11) NOT NULL,
  `cuentas_padre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `token`
--

CREATE TABLE `token` (
  `id_token` int(11) NOT NULL,
  `recuperacion` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idusuarios` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `correo` varchar(45) NOT NULL,
  `clave` varchar(45) NOT NULL,
  `roles_idroles` int(11) DEFAULT NULL,
  `token_idtoken` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idusuarios`, `nombre`, `correo`, `clave`, `roles_idroles`, `token_idtoken`) VALUES
(4, 'Juan', 'juanes.malave@gmail.com', 'juanes321', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_registro_movimiento`
--

CREATE TABLE `usuario_registro_movimiento` (
  `id_registro_movimiento` int(11) NOT NULL,
  `usuarios_idusuarios` int(11) DEFAULT NULL,
  `registro_movimiento` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  ADD PRIMARY KEY (`id_asientos`),
  ADD KEY `cuentas_contables_id2` (`cuentas_contables_id`),
  ADD KEY `empresas_cuentasid2` (`cuentas_contables_empresas_id`),
  ADD KEY `plan_cuentasid2` (`plan_cuentas_id`);

--
-- Indices de la tabla `auditoria`
--
ALTER TABLE `auditoria`
  ADD PRIMARY KEY (`id_auditoria`),
  ADD KEY `id_usuariosfk` (`usuarios_idusuarios`);

--
-- Indices de la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  ADD PRIMARY KEY (`id_cuenta_contable`),
  ADD KEY `cuentas_contables_id1` (`empresas_id`);

--
-- Indices de la tabla `empresas`
--
ALTER TABLE `empresas`
  ADD PRIMARY KEY (`id_empresas`);

--
-- Indices de la tabla `entidad`
--
ALTER TABLE `entidad`
  ADD PRIMARY KEY (`idEntidad`);

--
-- Indices de la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  ADD PRIMARY KEY (`id_plan_cuentas`),
  ADD KEY `registro_empresa1` (`registro_empresas`);

--
-- Indices de la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  ADD PRIMARY KEY (`id_Registros_Movimientos`),
  ADD KEY `Empresas_id1` (`Empresas_id`),
  ADD KEY `entidad_id1` (`entidad_id`);

--
-- Indices de la tabla `registro_reportes`
--
ALTER TABLE `registro_reportes`
  ADD PRIMARY KEY (`id_registro_reporte`),
  ADD KEY `registro_reporte_id1` (`registro_reporte`),
  ADD KEY `movimiento_id1` (`movimientos_id`);

--
-- Indices de la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD PRIMARY KEY (`id_reporte`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `tipos_cuentas`
--
ALTER TABLE `tipos_cuentas`
  ADD PRIMARY KEY (`id_tipo_cuenta`),
  ADD KEY `fk_tipos_cuentas_cuentas_padre_id` (`cuentas_padre_id`);

--
-- Indices de la tabla `token`
--
ALTER TABLE `token`
  ADD PRIMARY KEY (`id_token`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idusuarios`),
  ADD KEY `usuarios_ibfk_1` (`roles_idroles`),
  ADD KEY `usuarios_ibfk_2` (`token_idtoken`);

--
-- Indices de la tabla `usuario_registro_movimiento`
--
ALTER TABLE `usuario_registro_movimiento`
  ADD PRIMARY KEY (`id_registro_movimiento`),
  ADD KEY `usuario_registro_movimiento` (`registro_movimiento`),
  ADD KEY `usuarios_idusuario` (`usuarios_idusuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  MODIFY `id_asientos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auditoria`
--
ALTER TABLE `auditoria`
  MODIFY `id_auditoria` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  MODIFY `id_cuenta_contable` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `empresas`
--
ALTER TABLE `empresas`
  MODIFY `id_empresas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `entidad`
--
ALTER TABLE `entidad`
  MODIFY `idEntidad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  MODIFY `id_plan_cuentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  MODIFY `id_Registros_Movimientos` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `registro_reportes`
--
ALTER TABLE `registro_reportes`
  MODIFY `id_registro_reporte` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id_reporte` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipos_cuentas`
--
ALTER TABLE `tipos_cuentas`
  MODIFY `id_tipo_cuenta` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `token`
--
ALTER TABLE `token`
  MODIFY `id_token` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idusuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario_registro_movimiento`
--
ALTER TABLE `usuario_registro_movimiento`
  MODIFY `id_registro_movimiento` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asientos_contables`
--
ALTER TABLE `asientos_contables`
  ADD CONSTRAINT `cuentas_contables_id2` FOREIGN KEY (`cuentas_contables_id`) REFERENCES `cuentas_contables` (`id_cuenta_contable`),
  ADD CONSTRAINT `empresas_cuentasid2` FOREIGN KEY (`cuentas_contables_empresas_id`) REFERENCES `empresas` (`id_empresas`),
  ADD CONSTRAINT `plan_cuentasid2` FOREIGN KEY (`plan_cuentas_id`) REFERENCES `plan_cuentas` (`id_plan_cuentas`);

--
-- Filtros para la tabla `auditoria`
--
ALTER TABLE `auditoria`
  ADD CONSTRAINT `id_usuariosfk` FOREIGN KEY (`usuarios_idusuarios`) REFERENCES `usuarios` (`idusuarios`);

--
-- Filtros para la tabla `cuentas_contables`
--
ALTER TABLE `cuentas_contables`
  ADD CONSTRAINT `cuentas_contables_id1` FOREIGN KEY (`empresas_id`) REFERENCES `empresas` (`id_empresas`);

--
-- Filtros para la tabla `plan_cuentas`
--
ALTER TABLE `plan_cuentas`
  ADD CONSTRAINT `registro_empresa1` FOREIGN KEY (`registro_empresas`) REFERENCES `empresas` (`id_empresas`);

--
-- Filtros para la tabla `registros_movimientos`
--
ALTER TABLE `registros_movimientos`
  ADD CONSTRAINT `Empresas_id1` FOREIGN KEY (`Empresas_id`) REFERENCES `empresas` (`id_empresas`),
  ADD CONSTRAINT `entidad_id1` FOREIGN KEY (`entidad_id`) REFERENCES `entidad` (`idEntidad`);

--
-- Filtros para la tabla `registro_reportes`
--
ALTER TABLE `registro_reportes`
  ADD CONSTRAINT `movimiento_id1` FOREIGN KEY (`movimientos_id`) REFERENCES `registros_movimientos` (`id_Registros_Movimientos`),
  ADD CONSTRAINT `registro_reporte_id1` FOREIGN KEY (`registro_reporte`) REFERENCES `reportes` (`id_reporte`);

--
-- Filtros para la tabla `tipos_cuentas`
--
ALTER TABLE `tipos_cuentas`
  ADD CONSTRAINT `fk_tipos_cuentas_cuentas_padre_id` FOREIGN KEY (`cuentas_padre_id`) REFERENCES `tipos_cuentas` (`id_tipo_cuenta`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`roles_idroles`) REFERENCES `roles` (`id_rol`),
  ADD CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`token_idtoken`) REFERENCES `token` (`id_token`);

--
-- Filtros para la tabla `usuario_registro_movimiento`
--
ALTER TABLE `usuario_registro_movimiento`
  ADD CONSTRAINT `usuario_registro_movimiento` FOREIGN KEY (`registro_movimiento`) REFERENCES `registros_movimientos` (`id_Registros_Movimientos`),
  ADD CONSTRAINT `usuarios_idusuario` FOREIGN KEY (`usuarios_idusuarios`) REFERENCES `usuarios` (`idusuarios`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
