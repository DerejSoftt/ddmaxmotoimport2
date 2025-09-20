-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-09-2025 a las 05:53:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `phonedb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(1, 'usuario1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add Cliente', 1, 'add_cliente'),
(2, 'Can change Cliente', 1, 'change_cliente'),
(3, 'Can delete Cliente', 1, 'delete_cliente'),
(4, 'Can view Cliente', 1, 'view_cliente'),
(5, 'Can add Proveedor', 2, 'add_proveedor'),
(6, 'Can change Proveedor', 2, 'change_proveedor'),
(7, 'Can delete Proveedor', 2, 'delete_proveedor'),
(8, 'Can view Proveedor', 2, 'view_proveedor'),
(9, 'Can add Entrada de Producto', 3, 'add_entradaproducto'),
(10, 'Can change Entrada de Producto', 3, 'change_entradaproducto'),
(11, 'Can delete Entrada de Producto', 3, 'delete_entradaproducto'),
(12, 'Can view Entrada de Producto', 3, 'view_entradaproducto'),
(13, 'Can add Caja', 4, 'add_caja'),
(14, 'Can change Caja', 4, 'change_caja'),
(15, 'Can delete Caja', 4, 'delete_caja'),
(16, 'Can view Caja', 4, 'view_caja'),
(17, 'Can add log entry', 5, 'add_logentry'),
(18, 'Can change log entry', 5, 'change_logentry'),
(19, 'Can delete log entry', 5, 'delete_logentry'),
(20, 'Can view log entry', 5, 'view_logentry'),
(21, 'Can add permission', 6, 'add_permission'),
(22, 'Can change permission', 6, 'change_permission'),
(23, 'Can delete permission', 6, 'delete_permission'),
(24, 'Can view permission', 6, 'view_permission'),
(25, 'Can add group', 7, 'add_group'),
(26, 'Can change group', 7, 'change_group'),
(27, 'Can delete group', 7, 'delete_group'),
(28, 'Can view group', 7, 'view_group'),
(29, 'Can add user', 8, 'add_user'),
(30, 'Can change user', 8, 'change_user'),
(31, 'Can delete user', 8, 'delete_user'),
(32, 'Can view user', 8, 'view_user'),
(33, 'Can add content type', 9, 'add_contenttype'),
(34, 'Can change content type', 9, 'change_contenttype'),
(35, 'Can delete content type', 9, 'delete_contenttype'),
(36, 'Can view content type', 9, 'view_contenttype'),
(37, 'Can add session', 10, 'add_session'),
(38, 'Can change session', 10, 'change_session'),
(39, 'Can delete session', 10, 'delete_session'),
(40, 'Can view session', 10, 'view_session'),
(41, 'Can add Venta', 11, 'add_venta'),
(42, 'Can change Venta', 11, 'change_venta'),
(43, 'Can delete Venta', 11, 'delete_venta'),
(44, 'Can view Venta', 11, 'view_venta'),
(45, 'Can add Detalle de Venta', 12, 'add_detalleventa'),
(46, 'Can change Detalle de Venta', 12, 'change_detalleventa'),
(47, 'Can delete Detalle de Venta', 12, 'delete_detalleventa'),
(48, 'Can view Detalle de Venta', 12, 'view_detalleventa'),
(49, 'Can add movimiento stock', 13, 'add_movimientostock'),
(50, 'Can change movimiento stock', 13, 'change_movimientostock'),
(51, 'Can delete movimiento stock', 13, 'delete_movimientostock'),
(52, 'Can view movimiento stock', 13, 'view_movimientostock'),
(53, 'Can add Cuenta por Cobrar', 14, 'add_cuentaporcobrar'),
(54, 'Can change Cuenta por Cobrar', 14, 'change_cuentaporcobrar'),
(55, 'Can delete Cuenta por Cobrar', 14, 'delete_cuentaporcobrar'),
(56, 'Can view Cuenta por Cobrar', 14, 'view_cuentaporcobrar'),
(57, 'Can add Pago de Cuenta por Cobrar', 15, 'add_pagocuentaporcobrar'),
(58, 'Can change Pago de Cuenta por Cobrar', 15, 'change_pagocuentaporcobrar'),
(59, 'Can delete Pago de Cuenta por Cobrar', 15, 'delete_pagocuentaporcobrar'),
(60, 'Can view Pago de Cuenta por Cobrar', 15, 'view_pagocuentaporcobrar'),
(61, 'Can add Cierre de Caja', 16, 'add_cierrecaja'),
(62, 'Can change Cierre de Caja', 16, 'change_cierrecaja'),
(63, 'Can delete Cierre de Caja', 16, 'delete_cierrecaja'),
(64, 'Can view Cierre de Caja', 16, 'view_cierrecaja'),
(65, 'Can add devolucion', 17, 'add_devolucion'),
(66, 'Can change devolucion', 17, 'change_devolucion'),
(67, 'Can delete devolucion', 17, 'delete_devolucion'),
(68, 'Can view devolucion', 17, 'view_devolucion'),
(69, 'Can add Comprobante de Pago', 18, 'add_comprobantepago'),
(70, 'Can change Comprobante de Pago', 18, 'change_comprobantepago'),
(71, 'Can delete Comprobante de Pago', 18, 'delete_comprobantepago'),
(72, 'Can view Comprobante de Pago', 18, 'view_comprobantepago');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$lGRqNegNfNDKmxbjfscvxR$Q/exGasZZkoL9klTkjTK1WXvje3tBh6mzbWY9JC/oRo=', '2025-09-19 15:07:04.728785', 1, 'jose', '', '', '', 1, 1, '2025-08-30 00:14:16.493405'),
(2, 'pbkdf2_sha256$600000$pHnbzanZ62Mb8j7QngpegO$NiM24p251NofJ1cYIHehBkWKmJS6aFskZv5pi423EjI=', '2025-09-01 14:36:30.832738', 1, 'joel', '', '', '', 1, 1, '2025-09-01 14:36:10.863442'),
(3, 'pbkdf2_sha256$600000$t6ReAspHtINwkEURQ9Pv5T$eemV35vMZSmba7iBeejl6ZwMCBXGhsLNGxHmX6+zuo0=', '2025-09-19 06:50:35.741735', 0, 'alez', 'alex', 'Rafael', 'amig@gmail.com', 0, 1, '2025-09-18 23:34:12.181049');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caja`
--

CREATE TABLE `caja` (
  `id` bigint(20) NOT NULL,
  `fecha_apertura` datetime(6) NOT NULL,
  `fecha_cierre` datetime(6) DEFAULT NULL,
  `monto_inicial` decimal(10,2) NOT NULL,
  `monto_final` decimal(10,2) DEFAULT NULL,
  `estado` varchar(10) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `caja`
--

INSERT INTO `caja` (`id`, `fecha_apertura`, `fecha_cierre`, `monto_inicial`, `monto_final`, `estado`, `observaciones`, `usuario_id`) VALUES
(2, '2025-09-01 14:36:58.718330', '2025-09-04 04:35:03.040117', 5000.00, 128900.00, 'cerrada', '', 2),
(3, '2025-09-04 04:36:25.937931', '2025-09-04 04:37:52.375058', 7000.00, 32000.00, 'cerrada', '', 2),
(4, '2025-09-05 15:22:37.765852', '2025-09-06 12:13:25.360816', 100.00, 10000.00, 'cerrada', '', 2),
(5, '2025-09-06 12:22:25.967937', '2025-09-06 12:24:41.746907', 6000.00, 6000.00, 'cerrada', '', 2),
(6, '2025-09-06 15:28:12.491963', '2025-09-06 15:37:22.606222', 100.00, 58500.00, 'cerrada', '', 2),
(7, '2025-09-06 15:42:22.171542', '2025-09-06 15:46:13.953864', 500.00, 31500.00, 'cerrada', '', 2),
(8, '2025-09-06 15:48:48.675205', '2025-09-06 15:51:00.465729', 100.00, 35000.00, 'cerrada', '', 2),
(9, '2025-09-09 02:24:49.293224', '2025-09-09 02:31:27.510513', 500.00, 29400.00, 'cerrada', '', 2),
(10, '2025-09-09 03:24:16.823134', '2025-09-09 03:25:38.255311', 700.00, 30000.00, 'cerrada', '', 2),
(11, '2025-09-11 22:32:50.043578', '2025-09-11 22:42:49.248862', 100.00, 63000.00, 'cerrada', '', 1),
(12, '2025-09-11 22:58:26.849337', '2025-09-17 02:17:24.570530', 100.00, 0.00, 'cerrada', '', 1),
(13, '2025-09-17 02:20:56.314463', '2025-09-17 02:23:10.152840', 2000.00, 30000.00, 'cerrada', '', 1),
(14, '2025-09-17 02:28:00.838256', '2025-09-17 02:29:25.742178', 500.00, 30000.00, 'cerrada', '', 1),
(15, '2025-09-17 02:30:55.755970', '2025-09-17 02:32:08.472592', 1000.00, 30500.00, 'cerrada', '', 1),
(16, '2025-09-17 02:37:46.510517', '2025-09-17 02:41:05.734707', 1000.00, 66000.00, 'cerrada', '', 1),
(17, '2025-09-17 03:23:14.524101', '2025-09-17 05:00:55.187799', 1000.00, 31000.00, 'cerrada', '', 1),
(18, '2025-09-17 05:04:19.951386', '2025-09-17 05:05:22.119844', 2000.00, 32000.00, 'cerrada', '', 1),
(19, '2025-09-17 13:31:03.529939', '2025-09-17 13:48:28.495586', 1000.00, 59800.00, 'cerrada', '', 1),
(20, '2025-09-17 15:36:36.842753', NULL, 0.00, NULL, 'abierta', NULL, 1),
(21, '2025-09-19 03:12:02.601669', '2025-09-19 03:25:31.425852', 1000.00, 51680.00, 'cerrada', '', 3),
(22, '2025-09-19 03:52:06.682075', '2025-09-19 04:04:26.959462', 1000.00, 51680.00, 'cerrada', '', 3),
(23, '2025-09-19 04:07:00.235137', '2025-09-19 04:55:42.628843', 1000.00, 90000.00, 'cerrada', '', 3),
(24, '2025-09-19 04:56:44.838398', '2025-09-19 05:01:46.247688', 1000.00, 104000.00, 'cerrada', '', 3),
(25, '2025-09-19 05:09:26.435560', '2025-09-19 05:50:49.757307', 0.00, 70000.00, 'cerrada', '', 3),
(26, '2025-09-19 05:51:10.836528', '2025-09-19 05:53:34.449487', 1000.00, 60000.00, 'cerrada', '', 3),
(27, '2025-09-19 06:50:49.244853', '2025-09-19 06:52:51.573948', 1000.00, 70000.00, 'cerrada', '', 3),
(28, '2025-09-19 07:02:00.952284', '2025-09-19 07:04:05.451199', 0.00, 60000.00, 'cerrada', '', 3),
(29, '2025-09-19 07:10:58.349744', '2025-09-19 07:14:23.559830', 100.00, 61000.00, 'cerrada', '', 3),
(30, '2025-09-19 13:06:05.239357', NULL, 0.00, NULL, 'abierta', NULL, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cierre_caja`
--

CREATE TABLE `cierre_caja` (
  `id` bigint(20) NOT NULL,
  `monto_efectivo_real` decimal(10,2) NOT NULL,
  `monto_tarjeta_real` decimal(10,2) NOT NULL,
  `total_esperado` decimal(10,2) NOT NULL,
  `diferencia` decimal(10,2) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `fecha_cierre` datetime(6) NOT NULL,
  `caja_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cierre_caja`
--

INSERT INTO `cierre_caja` (`id`, `monto_efectivo_real`, `monto_tarjeta_real`, `total_esperado`, `diferencia`, `observaciones`, `fecha_cierre`, `caja_id`) VALUES
(1, 128900.00, 0.00, 128700.00, 200.00, '', '2025-09-04 04:35:03.043844', 2),
(2, 32000.00, 0.00, 30000.00, 2000.00, '', '2025-09-04 04:37:52.375058', 3),
(3, 5000.00, 5000.00, 5000.00, 5000.00, '', '2025-09-06 12:13:25.360816', 4),
(4, 6000.00, 0.00, 5000.00, 1000.00, '', '2025-09-06 12:24:41.757329', 5),
(5, 58500.00, 0.00, 58500.00, 0.00, '', '2025-09-06 15:37:22.612887', 6),
(6, 31500.00, 0.00, 31500.00, 0.00, '', '2025-09-06 15:46:13.953864', 7),
(7, 35000.00, 0.00, 35000.00, 0.00, '', '2025-09-06 15:51:00.469685', 8),
(8, 29400.00, 0.00, 29400.00, 0.00, '', '2025-09-09 02:31:27.515510', 9),
(9, 30000.00, 0.00, 30000.00, 0.00, '', '2025-09-09 03:25:38.264682', 10),
(10, 58500.00, 4500.00, 63000.00, 0.00, '', '2025-09-11 22:42:49.252862', 11),
(11, 0.00, 0.00, 0.00, 0.00, '', '2025-09-17 02:17:24.584810', 12),
(12, 30000.00, 0.00, 30000.00, 0.00, '', '2025-09-17 02:23:10.161306', 13),
(13, 30000.00, 0.00, 30000.00, 0.00, '', '2025-09-17 02:29:25.799055', 14),
(14, 30500.00, 0.00, 30000.00, 500.00, '', '2025-09-17 02:32:08.479955', 15),
(15, 6000.00, 60000.00, 65000.00, 1000.00, '', '2025-09-17 02:41:05.742543', 16),
(16, 31000.00, 0.00, 30000.00, 1000.00, '', '2025-09-17 05:00:55.204334', 17),
(17, 32000.00, 0.00, 32000.00, 0.00, '', '2025-09-17 05:05:22.131258', 18),
(18, 59800.00, 0.00, 59800.00, 0.00, '', '2025-09-17 13:48:28.507555', 19),
(19, 51680.00, 0.00, 52680.00, -1000.00, '', '2025-09-19 03:25:31.448849', 21),
(20, 51680.00, 0.00, 51680.00, 0.00, '', '2025-09-19 04:04:26.964464', 22),
(21, 90000.00, 0.00, 89440.00, 560.00, '', '2025-09-19 04:55:42.640808', 23),
(22, 104000.00, 0.00, 104400.00, -400.00, '', '2025-09-19 05:01:46.294686', 24),
(23, 70000.00, 0.00, 70000.00, 0.00, '', '2025-09-19 05:50:49.783304', 25),
(24, 60000.00, 0.00, 60000.00, 0.00, '', '2025-09-19 05:53:34.455502', 26),
(25, 70000.00, 0.00, 70000.00, 0.00, '', '2025-09-19 06:52:51.578943', 27),
(26, 60000.00, 0.00, 60000.00, 0.00, '', '2025-09-19 07:04:05.455200', 28),
(27, 61000.00, 0.00, 60000.00, 1000.00, '', '2025-09-19 07:14:23.579891', 29);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `identification_number` varchar(20) NOT NULL,
  `primary_phone` varchar(15) NOT NULL,
  `secondary_phone` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `email` varchar(254) NOT NULL,
  `credit_limit` decimal(10,2) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `full_name`, `identification_number`, `primary_phone`, `secondary_phone`, `address`, `email`, `credit_limit`, `status`, `fecha_registro`) VALUES
(1, 'jose Miguel b. Acosta', '402-2834666-6', '(829) 451-0168', '(829) 451-0169', 'motecristi', '', 9000.00, 1, '2025-08-30 13:01:42.940939'),
(2, 'Rafael Acosta', '402-2834666-8', '(829) 451-0162', '(829) 451-0168', 'motecristi', '', 60000.00, 1, '2025-08-31 04:22:51.606021'),
(3, 'Joel Piña', '445-4544446-4', '(455) 545-5455', '(767) 676-7676', 'loma', '', 5000.00, 1, '2025-09-01 14:57:41.794318'),
(4, 'Maria Moncion', '665-6556656-5', '(829) 451-0167', '(565) 656-6565', 'loma', '', 8000.00, 1, '2025-09-01 15:34:46.893557'),
(5, 'Darimal', '009-3938373-6', '(366) 536-3776', '(377) 373-7838', 'castañuela', '', 20000.00, 1, '2025-09-17 13:28:34.495473'),
(6, 'alex acosta', '788-7428743-2', '(932) 982-9842', '(298) 329-8983', 'motecristi', '', 600000.00, 1, '2025-09-18 15:46:04.530057'),
(7, 'arturo bello', '909-0004384-2', '(987) 427-8487', '(329) 209-2983', 'loma', '', 400000.00, 1, '2025-09-19 19:37:40.511996'),
(8, 'joel', '787-7776767-4', '(829) 451-0168', '(383) 883-8388', 'loma', '', 3000000.00, 1, '2025-09-19 19:54:16.590377'),
(9, 'jay', '484-8747749-7', '(329) 898-3298', '(329) 329-8329', '487474', '', 500000.00, 1, '2025-09-19 20:22:26.465391');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprobantes_pago`
--

CREATE TABLE `comprobantes_pago` (
  `id` bigint(20) NOT NULL,
  `numero_comprobante` varchar(20) NOT NULL,
  `tipo_comprobante` varchar(15) NOT NULL,
  `fecha_emision` datetime(6) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `cuenta_id` bigint(20) NOT NULL,
  `pago_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comprobantes_pago`
--

INSERT INTO `comprobantes_pago` (`id`, `numero_comprobante`, `tipo_comprobante`, `fecha_emision`, `cliente_id`, `cuenta_id`, `pago_id`) VALUES
(1, 'CP-2025-000001', 'recibo', '2025-09-19 22:10:54.552745', 7, 38, 11),
(2, 'CP-2025-000002', 'recibo', '2025-09-19 22:29:52.155771', 7, 38, 12),
(3, 'CP-2025-000003', 'recibo', '2025-09-19 22:37:26.186026', 7, 38, 13),
(4, 'CP-2025-000004', 'recibo', '2025-09-19 23:03:13.790032', 9, 39, 14),
(5, 'CP-2025-000005', 'recibo', '2025-09-19 23:04:11.495116', 9, 39, 15),
(6, 'CP-2025-000006', 'recibo', '2025-09-19 23:08:00.927362', 9, 39, 16),
(7, 'CP-2025-000007', 'recibo', '2025-09-19 23:14:20.804267', 9, 39, 17),
(8, 'CP-2025-000008', 'recibo', '2025-09-19 23:15:13.672152', 9, 37, 18),
(9, 'CP-2025-000009', 'recibo', '2025-09-19 23:17:52.904033', 7, 40, 19),
(10, 'CP-2025-000010', 'recibo', '2025-09-19 23:24:21.114317', 6, 36, 20);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas_por_cobrar`
--

CREATE TABLE `cuentas_por_cobrar` (
  `id` bigint(20) NOT NULL,
  `monto_total` decimal(12,2) NOT NULL,
  `monto_pagado` decimal(12,2) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `estado` varchar(10) NOT NULL,
  `observaciones` longtext NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `venta_id` bigint(20) NOT NULL,
  `productos` longtext NOT NULL,
  `anulada` tinyint(1) NOT NULL,
  `fecha_anulacion` datetime(6) DEFAULT NULL,
  `monto_total_con_interes` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cuentas_por_cobrar`
--

INSERT INTO `cuentas_por_cobrar` (`id`, `monto_total`, `monto_pagado`, `fecha_vencimiento`, `estado`, `observaciones`, `fecha_creacion`, `fecha_actualizacion`, `cliente_id`, `venta_id`, `productos`, `anulada`, `fecha_anulacion`, `monto_total_con_interes`) VALUES
(36, 54400.00, 54400.00, '2025-10-19', 'pagada', 'Venta a crédito - Factura: F-2025-000079\nCliente: alex acosta\nProductos:\nCG150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-19 20:55:07.769635', '2025-09-19 23:24:21.123284', 6, 81, 'CG150 x1 - RD$50000.00', 0, NULL, 54400.00),
(37, 54400.00, 54400.00, '2025-10-19', 'pagada', 'Venta a crédito - Factura: F-2025-000080\nCliente: jay\nProductos:\nCG150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-19 21:07:03.486224', '2025-09-19 23:15:13.697152', 9, 82, 'CG150 x1 - RD$50000.00', 0, NULL, 54400.00),
(38, 54400.00, 54400.00, '2025-10-19', 'pagada', 'Venta a crédito - Factura: F-2025-000081\nCliente: arturo bello\nProductos:\nCG150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-19 21:22:36.361760', '2025-09-19 22:37:26.195026', 7, 83, 'CG150 x1 - RD$50000.00', 0, NULL, 54400.00),
(39, 54400.00, 54400.00, '2025-10-19', 'pagada', 'Venta a crédito - Factura: F-2025-000082\nCliente: jay\nProductos:\nCG150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-19 23:02:08.655855', '2025-09-19 23:14:20.812265', 9, 84, 'CG150 x1 - RD$50000.00', 0, NULL, 54400.00),
(40, 54400.00, 15000.00, '2025-10-19', 'parcial', 'Venta a crédito - Factura: F-2025-000083\nCliente: arturo bello\nProductos:\nCG150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-19 23:16:01.818648', '2025-09-19 23:17:52.917032', 7, 85, 'CG150 x1 - RD$50000.00', 0, NULL, 54400.00),
(41, 54400.00, 10000.00, '2025-10-20', 'anulada', 'Venta a crédito - Factura: F-2025-000084\nCliente: joel\nProductos:\nCG150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-20 00:10:46.140594', '2025-09-20 00:20:03.712119', 8, 86, 'CG150 x1 - RD$50000.00', 1, '2025-09-20 00:20:03.708130', 54400.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_venta`
--

CREATE TABLE `detalles_venta` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL CHECK (`cantidad` >= 0),
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  `venta_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_venta`
--

INSERT INTO `detalles_venta` (`id`, `cantidad`, `precio_unitario`, `subtotal`, `producto_id`, `venta_id`) VALUES
(8, 1, 30000.00, 30000.00, 31, 9),
(9, 1, 30000.00, 30000.00, 31, 10),
(10, 1, 30000.00, 30000.00, 31, 11),
(11, 1, 5000.00, 5000.00, 32, 12),
(12, 1, 5000.00, 5000.00, 32, 13),
(13, 1, 30000.00, 30000.00, 31, 14),
(14, 1, 30000.00, 30000.00, 31, 15),
(15, 1, 30000.00, 30000.00, 31, 16),
(16, 1, 30000.00, 30000.00, 31, 17),
(17, 1, 30000.00, 30000.00, 31, 18),
(18, 1, 5000.00, 5000.00, 32, 19),
(19, 1, 30000.00, 30000.00, 31, 20),
(20, 1, 30000.00, 30000.00, 31, 21),
(21, 1, 5000.00, 5000.00, 32, 22),
(22, 1, 5000.00, 5000.00, 32, 23),
(23, 2, 30000.00, 60000.00, 31, 24),
(24, 1, 5000.00, 5000.00, 32, 25),
(25, 1, 30000.00, 30000.00, 31, 26),
(26, 1, 5000.00, 5000.00, 32, 27),
(27, 1, 30000.00, 30000.00, 31, 28),
(28, 1, 5000.00, 5000.00, 32, 29),
(29, 1, 30000.00, 30000.00, 31, 30),
(30, 1, 30000.00, 30000.00, 31, 31),
(31, 1, 30000.00, 30000.00, 31, 32),
(32, 1, 5000.00, 5000.00, 32, 32),
(33, 1, 30000.00, 30000.00, 31, 33),
(34, 1, 5000.00, 5000.00, 32, 34),
(35, 1, 30000.00, 30000.00, 31, 35),
(36, 1, 30000.00, 30000.00, 31, 36),
(37, 1, 30000.00, 30000.00, 31, 37),
(38, 1, 5000.00, 5000.00, 32, 38),
(39, 1, 30000.00, 30000.00, 31, 39),
(40, 1, 30000.00, 30000.00, 31, 40),
(41, 1, 30000.00, 30000.00, 31, 41),
(42, 1, 30000.00, 30000.00, 31, 42),
(43, 1, 60000.00, 60000.00, 34, 43),
(44, 1, 5000.00, 5000.00, 32, 44),
(45, 1, 50000.00, 50000.00, 34, 45),
(47, 1, 50000.00, 50000.00, 34, 47),
(49, 1, 50000.00, 50000.00, 34, 49),
(50, 1, 50000.00, 50000.00, 34, 50),
(51, 1, 50000.00, 50000.00, 34, 51),
(52, 1, 50000.00, 50000.00, 34, 52),
(53, 1, 50000.00, 50000.00, 34, 53),
(54, 1, 50000.00, 50000.00, 34, 54),
(55, 1, 50000.00, 50000.00, 34, 55),
(56, 1, 50000.00, 50000.00, 34, 56),
(57, 1, 50000.00, 50000.00, 34, 57),
(58, 1, 50000.00, 50000.00, 34, 58),
(59, 1, 50000.00, 50000.00, 34, 59),
(60, 1, 50000.00, 50000.00, 34, 60),
(61, 1, 50000.00, 50000.00, 34, 61),
(62, 1, 50000.00, 50000.00, 34, 62),
(63, 1, 50000.00, 50000.00, 34, 63),
(64, 1, 50000.00, 50000.00, 34, 64),
(65, 1, 50000.00, 50000.00, 34, 65),
(66, 1, 50000.00, 50000.00, 34, 66),
(68, 1, 50000.00, 50000.00, 34, 68),
(69, 1, 50000.00, 50000.00, 34, 69),
(70, 1, 50000.00, 50000.00, 34, 70),
(71, 1, 50000.00, 50000.00, 34, 71),
(72, 1, 50000.00, 50000.00, 34, 72),
(73, 1, 50000.00, 50000.00, 34, 73),
(74, 1, 50000.00, 50000.00, 34, 74),
(75, 1, 50000.00, 50000.00, 34, 75),
(76, 1, 50000.00, 50000.00, 34, 76),
(77, 1, 50000.00, 50000.00, 34, 77),
(78, 1, 50000.00, 50000.00, 34, 78),
(79, 1, 50000.00, 50000.00, 34, 79),
(80, 1, 50000.00, 50000.00, 34, 80),
(81, 1, 50000.00, 50000.00, 34, 81),
(82, 1, 50000.00, 50000.00, 34, 82),
(83, 1, 50000.00, 50000.00, 34, 83),
(84, 1, 50000.00, 50000.00, 34, 84),
(85, 1, 50000.00, 50000.00, 34, 85),
(86, 1, 50000.00, 50000.00, 34, 86);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(5, 'admin', 'logentry'),
(7, 'auth', 'group'),
(6, 'auth', 'permission'),
(8, 'auth', 'user'),
(9, 'contenttypes', 'contenttype'),
(4, 'facturacion', 'caja'),
(16, 'facturacion', 'cierrecaja'),
(1, 'facturacion', 'cliente'),
(18, 'facturacion', 'comprobantepago'),
(14, 'facturacion', 'cuentaporcobrar'),
(12, 'facturacion', 'detalleventa'),
(17, 'facturacion', 'devolucion'),
(3, 'facturacion', 'entradaproducto'),
(13, 'facturacion', 'movimientostock'),
(15, 'facturacion', 'pagocuentaporcobrar'),
(2, 'facturacion', 'proveedor'),
(11, 'facturacion', 'venta'),
(10, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-08-29 23:15:05.342118'),
(2, 'auth', '0001_initial', '2025-08-29 23:15:05.925902'),
(3, 'admin', '0001_initial', '2025-08-29 23:15:06.089026'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-08-29 23:15:06.100810'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-08-29 23:15:06.123549'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-08-29 23:15:06.273007'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-08-29 23:15:06.406115'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-08-29 23:15:06.454979'),
(9, 'auth', '0004_alter_user_username_opts', '2025-08-29 23:15:06.467313'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-08-29 23:15:06.533210'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-08-29 23:15:06.538503'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-08-29 23:15:06.551739'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-08-29 23:15:06.578826'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-08-29 23:15:06.602394'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-08-29 23:15:06.627130'),
(16, 'auth', '0011_update_proxy_permissions', '2025-08-29 23:15:06.830034'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-08-29 23:15:06.906936'),
(18, 'facturacion', '0001_initial', '2025-08-29 23:15:07.371740'),
(19, 'sessions', '0001_initial', '2025-08-29 23:15:07.520986'),
(20, 'facturacion', '0002_venta_detalleventa', '2025-08-30 12:20:20.332124'),
(21, 'facturacion', '0003_movimientostock', '2025-08-30 12:39:08.405823'),
(22, 'facturacion', '0004_entradaproducto_es_producto_base', '2025-08-30 16:54:36.205280'),
(23, 'facturacion', '0005_cuentaporcobrar_pagocuentaporcobrar', '2025-09-01 20:20:47.759149'),
(24, 'facturacion', '0006_cuentaporcobrar_productos', '2025-09-02 13:28:12.180774'),
(25, 'facturacion', '0007_cierrecaja', '2025-09-03 23:30:57.666624'),
(26, 'facturacion', '0008_venta_cuota_mensual_venta_es_financiada_and_more', '2025-09-18 13:46:35.275141'),
(27, 'facturacion', '0009_venta_montoinicial', '2025-09-18 15:38:44.529348'),
(28, 'facturacion', '0010_venta_fecha_anulacion_venta_motivo_anulacion_and_more', '2025-09-19 00:21:24.088227'),
(29, 'facturacion', '0011_devolucion', '2025-09-19 03:08:41.914331'),
(30, 'facturacion', '0012_venta_total_a_pagar', '2025-09-19 14:11:01.569708'),
(31, 'facturacion', '0013_cuentaporcobrar_anulada_and_more', '2025-09-19 19:24:18.392952'),
(32, 'facturacion', '0014_alter_cuentaporcobrar_monto_total_con_interes', '2025-09-19 19:36:17.929260'),
(33, 'facturacion', '0015_comprobantepago', '2025-09-19 22:06:59.196184');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('4ne9lpbfxl43lp8z2ft5loq0sw19zsbf', '.eJxVj01ShDAQhe-StYUJEQgsZ-8ZUp1ORzJiYoXAZmrubqNojV29et97_XMTFrY6222lYqMXk2jF06PmAN8pHcBfIb3lBnOqJbrmsDQnXZvX7Gm5nN5_A2ZYZ04b5VCb3jtpCBGDAxgMqn4YjQ8vWmkHoVedkQp0NwSUrSJtRnRooDX9cRVGKoVsTCGL6SYC4Qw8WY7P3K1sO_bMuYD9MR5IT203acPgg8_OljhU455tIVjEpCVXI39phXKlCif8BjVXWCytn1TA54eEj4EKJYxwOrPjb3fAmBOtvJt37pQqrBbzlqqYFH-wRJboT5L3-xflknzU:1uvozC:FCQUHlEOOOF-BsXWFBkBgDecQoyV4ytPmJ_dJycTY-U', '2025-09-23 03:25:38.346172'),
('ba72xb4ldiyuomm84js429m3l4jvs2bh', '.eJxVj8FuwyAQRP-Fc-VgY0zwMfd-A1pgqUldqAD7EuXfu2ncqpU4oHmzO7M3ZmBri9kqFhM9m1nPXv5qFtw7pgfwV0hvuXM5tRJt97B0B63da_a4Xg7vvwUL1IWmrbf9qHUIfUAhR-kU0DdMwk5nra2dFE5KjXJw3CvUXgjhHBc4oJVK2ZGWuoiloIkpZDbfWEC3wKNwf-L6NPBBkmfJBczTSGgY5pGeJvBBtbNBGmpxz6YgrGyWZ8l5x39og3LFBgccD9Zyg9Vg_cQCnpInwZ_Ax4AFk4vU4lvIlg7ewcWcsFI8xe6YGlTj8pYamwUdsUaS8Ffq7_cvULl9nQ:1uxA9S:-ZlHhMZ7mzVuSl8QnUFlcAIMv_y-kRTc6z2YzJukoBc', '2025-09-26 20:13:46.059142'),
('c88p9mgxd6y2zrj9ie6ae8qu01n0noxy', '.eJxVjM0OwiAQhN-FsyGl_Kx49O4zEHZZpGogKe3J-O62SQ96m8z3zbxFiOtSwtp5DlMSF6HE6bfDSE-uO0iPWO9NUqvLPKHcFXnQLm8t8et6uH8HJfayrTGhMt7nrDJrayxB3GJ2Gt3Ze0QH7ACMHWlIwD5prYkGzSOjBUAjPl_8rzhM:1uwqMY:N09f96iiOrnbsOLTv2q7M6TUdEY0z5FXDGDsdJZtO4w', '2025-09-25 23:05:58.835729'),
('eab8b36lyt52s5y59wt4vibyarkek8x0', '.eJxVjM0OwiAQhN-FsyGl_Kx49O4zEHZZpGogKe3J-O62SQ96m8z3zbxFiOtSwtp5DlMSF6HE6bfDSE-uO0iPWO9NUqvLPKHcFXnQLm8t8et6uH8HJfayrTGhMt7nrDJrayxB3GJ2Gt3Ze0QH7ACMHWlIwD5prYkGzSOjBUAjPl_8rzhM:1uzchU:LaGTmD9677LLNQFlmVa50stwigWBq9ljnlYV4cRk1QM', '2025-10-03 15:07:04.748283');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturacion_devolucion`
--

CREATE TABLE `facturacion_devolucion` (
  `id` bigint(20) NOT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL CHECK (`cantidad` >= 0),
  `motivo` varchar(100) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `fecha_devolucion` datetime(6) NOT NULL,
  `producto_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `venta_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturacion_entradaproducto`
--

CREATE TABLE `facturacion_entradaproducto` (
  `id` bigint(20) NOT NULL,
  `codigo_producto` varchar(20) NOT NULL,
  `numero_factura` varchar(50) NOT NULL,
  `fecha_entrada` date NOT NULL,
  `ncf` varchar(20) DEFAULT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `marca` varchar(20) NOT NULL,
  `modelo` varchar(100) NOT NULL,
  `capacidad` varchar(10) DEFAULT NULL,
  `imei_serial` varchar(50) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `color` varchar(20) DEFAULT NULL,
  `cantidad` int(10) UNSIGNED NOT NULL CHECK (`cantidad` >= 0),
  `cantidad_minima` int(10) UNSIGNED NOT NULL CHECK (`cantidad_minima` >= 0),
  `costo_compra` decimal(10,2) NOT NULL,
  `porcentaje_itbis` decimal(5,2) NOT NULL,
  `monto_itbis` decimal(10,2) NOT NULL,
  `costo_total` decimal(10,2) NOT NULL,
  `costo_venta` decimal(10,2) NOT NULL,
  `margen_ganancia` decimal(10,2) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `observaciones` longtext DEFAULT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `proveedor_id` bigint(20) NOT NULL,
  `es_producto_base` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `facturacion_entradaproducto`
--

INSERT INTO `facturacion_entradaproducto` (`id`, `codigo_producto`, `numero_factura`, `fecha_entrada`, `ncf`, `nombre_producto`, `marca`, `modelo`, `capacidad`, `imei_serial`, `estado`, `color`, `cantidad`, `cantidad_minima`, `costo_compra`, `porcentaje_itbis`, `monto_itbis`, `costo_total`, `costo_venta`, `margen_ganancia`, `activo`, `observaciones`, `fecha_registro`, `fecha_actualizacion`, `proveedor_id`, `es_producto_base`) VALUES
(31, 'PROD-280490', '3344444', '2025-08-30', '4424244242', 'Samsung Galaxi S20', 'samsung', 'S20', '128GB', '444343434343434', 'nuevo', 'azul', 985, 2, 20000.00, 18.00, 3600.00, 23600.00, 30000.00, 27.12, 1, '', '2025-08-30 21:00:35.927799', '2025-08-30 21:00:35.927799', 1, 0),
(32, 'PROD-613040', 'PRO-123-204', '2025-09-01', '46546545446', 'TECHO', 'samsung', 'smrrte9', '64GB', '6565665656664', 'nuevo', 'negro', 996, 2, 4000.00, 18.00, 720.00, 4720.00, 5000.00, 5.93, 1, 'este telefono ya tiene dueño', '2025-09-01 14:48:29.122159', '2025-09-09 04:25:02.885967', 2, 0),
(33, 'PROD-742452', '8998898', '2025-09-17', '93209323K3K', 'zusuki', 'motorola', 'uiiuuuu98', '12', '87877878776', 'nuevo', 'dorado', 500, 2, 80000.00, 18.00, 14400.00, 94400.00, 90000.00, -4.66, 1, '', '2025-09-17 05:16:58.663126', '2025-09-19 15:15:30.301862', 1, 0),
(34, 'PROD-661581', '6366633', '2025-09-17', '3Y7373783', 'CG150', 'otros', 'CG200', '', '3553663790', 'nuevo', 'negro', 9987, 2, 40000.00, 18.00, 7200.00, 47200.00, 50000.00, 5.93, 1, '', '2025-09-17 13:24:23.199279', '2025-09-20 00:19:15.827987', 3, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturacion_proveedor`
--

CREATE TABLE `facturacion_proveedor` (
  `id` bigint(20) NOT NULL,
  `nombre_empresa` varchar(100) NOT NULL,
  `rnc` varchar(13) NOT NULL,
  `nombre_contacto` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `whatsapp` varchar(20) DEFAULT NULL,
  `pais` varchar(2) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `direccion` longtext DEFAULT NULL,
  `terminos_pago` varchar(20) DEFAULT NULL,
  `limite_credito` decimal(12,2) NOT NULL,
  `notas` longtext DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `ultima_actualizacion` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `facturacion_proveedor`
--

INSERT INTO `facturacion_proveedor` (`id`, `nombre_empresa`, `rnc`, `nombre_contacto`, `email`, `telefono`, `whatsapp`, `pais`, `ciudad`, `categoria`, `direccion`, `terminos_pago`, `limite_credito`, `notas`, `activo`, `fecha_registro`, `ultima_actualizacion`) VALUES
(1, 'samsumg', '676-76667-6', 'Wilkin', 'amig@gmail.com', '(829) 451-0168', '', 'DO', 'castañulas', 'smartphones', 'loma', 'contado', 1000.00, '', 1, '2025-08-30 00:42:37.255731', '2025-08-30 00:42:37.255731'),
(2, 'niño comunicacion', '887-88777-8', 'niño', 'nino@gmail.com', '(829) 451-0168', '(737) 637-6376', 'DO', 'castañulas', 'smartphones', 'loma', 'contado', 50000.00, 'ESTE SUPLIDOR ME FIA 50000 SIN ITBIS', 1, '2025-09-01 14:42:28.363835', '2025-09-01 14:42:28.363835'),
(3, 'tauro', '444-45454-5', 'jose ', 'amig@gmail.com', '(829) 451-0169', '(123) 098-7654', 'DO', 'castañulas', 'accesorios', 'loma', 'contado', 0.00, '', 1, '2025-09-17 13:18:58.987673', '2025-09-17 13:18:58.987673');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_stock`
--

CREATE TABLE `movimientos_stock` (
  `id` bigint(20) NOT NULL,
  `fecha_movimiento` datetime(6) NOT NULL,
  `tipo_movimiento` varchar(20) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `cantidad_anterior` int(11) NOT NULL,
  `cantidad_nueva` int(11) NOT NULL,
  `motivo` varchar(200) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `producto_id` bigint(20) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `movimientos_stock`
--

INSERT INTO `movimientos_stock` (`id`, `fecha_movimiento`, `tipo_movimiento`, `cantidad`, `cantidad_anterior`, `cantidad_nueva`, `motivo`, `referencia`, `producto_id`, `usuario_id`) VALUES
(15, '2025-08-30 21:01:46.043518', 'ajuste', 1, 10, 9, 'Ajuste manual de stock', NULL, 31, NULL),
(16, '2025-08-30 21:01:46.043518', 'venta', 1, 10, 9, 'Venta', 'F-2025-000008', 31, 1),
(17, '2025-09-01 12:05:04.405166', 'ajuste', 1, 9, 8, 'Ajuste manual de stock', NULL, 31, NULL),
(18, '2025-09-01 12:05:04.409193', 'venta', 1, 9, 8, 'Venta', 'F-2025-000009', 31, 1),
(19, '2025-09-01 12:53:24.392941', 'ajuste', 1, 8, 7, 'Ajuste manual de stock', NULL, 31, NULL),
(20, '2025-09-01 12:53:24.394659', 'venta', 1, 8, 7, 'Venta', 'F-2025-000010', 31, 1),
(21, '2025-09-01 14:53:03.687642', 'ajuste', 1, 5, 4, 'Ajuste manual de stock', NULL, 32, NULL),
(22, '2025-09-01 14:53:03.701579', 'venta', 1, 5, 4, 'Venta', 'F-2025-000011', 32, 2),
(23, '2025-09-01 15:00:13.915133', 'ajuste', 1, 4, 3, 'Ajuste manual de stock', NULL, 32, NULL),
(24, '2025-09-01 15:00:13.915133', 'venta', 1, 4, 3, 'Venta', 'F-2025-000012', 32, 2),
(25, '2025-09-01 15:32:53.775829', 'ajuste', 1, 7, 6, 'Ajuste manual de stock', NULL, 31, NULL),
(26, '2025-09-01 15:32:53.779160', 'venta', 1, 7, 6, 'Venta', 'F-2025-000013', 31, 2),
(27, '2025-09-01 15:37:34.234498', 'ajuste', 1, 6, 5, 'Ajuste manual de stock', NULL, 31, NULL),
(28, '2025-09-01 15:37:34.236177', 'venta', 1, 6, 5, 'Venta', 'F-2025-000014', 31, 2),
(29, '2025-09-01 21:14:44.797502', 'ajuste', 1, 5, 4, 'Ajuste manual de stock', NULL, 31, NULL),
(30, '2025-09-01 21:14:44.800017', 'venta', 1, 5, 4, 'Venta', 'F-2025-000015', 31, 2),
(31, '2025-09-02 01:37:13.524190', 'ajuste', 1, 4, 3, 'Ajuste manual de stock', NULL, 31, NULL),
(32, '2025-09-02 01:37:13.530283', 'venta', 1, 4, 3, 'Venta', 'F-2025-000016', 31, 2),
(33, '2025-09-02 13:29:39.923032', 'ajuste', 1, 3, 2, 'Ajuste manual de stock', NULL, 31, NULL),
(34, '2025-09-02 13:29:39.925564', 'venta', 1, 3, 2, 'Venta', 'F-2025-000017', 31, 2),
(35, '2025-09-02 15:34:21.967249', 'ajuste', 1, 3, 2, 'Ajuste manual de stock', NULL, 32, NULL),
(36, '2025-09-02 15:34:21.971367', 'venta', 1, 3, 2, 'Venta', 'F-2025-000018', 32, 2),
(37, '2025-09-03 23:54:18.760676', 'ajuste', 1, 2, 1, 'Ajuste manual de stock', NULL, 31, NULL),
(38, '2025-09-03 23:54:18.793974', 'venta', 1, 2, 1, 'Venta', 'F-2025-000019', 31, 2),
(39, '2025-09-04 04:36:55.137873', 'ajuste', 1, 1, 0, 'Ajuste manual de stock', NULL, 31, NULL),
(40, '2025-09-04 04:36:55.151729', 'venta', 1, 1, 0, 'Venta', 'F-2025-000020', 31, 2),
(41, '2025-09-06 12:06:08.770947', 'ajuste', 1, 2, 1, 'Ajuste manual de stock', NULL, 32, NULL),
(42, '2025-09-06 12:06:08.770947', 'venta', 1, 2, 1, 'Venta', 'F-2025-000021', 32, 2),
(43, '2025-09-06 12:23:30.454337', 'ajuste', 1, 1, 0, 'Ajuste manual de stock', NULL, 32, NULL),
(44, '2025-09-06 12:23:30.454337', 'venta', 1, 1, 0, 'Venta', 'F-2025-000022', 32, 2),
(45, '2025-09-06 15:29:01.127869', 'ajuste', 2, 1000, 998, 'Ajuste manual de stock', NULL, 31, NULL),
(46, '2025-09-06 15:29:01.135875', 'venta', 2, 1000, 998, 'Venta', 'F-2025-000023', 31, 2),
(47, '2025-09-06 15:31:29.418884', 'ajuste', 1, 1000, 999, 'Ajuste manual de stock', NULL, 32, NULL),
(48, '2025-09-06 15:31:29.419881', 'venta', 1, 1000, 999, 'Venta', 'F-2025-000024', 32, 2),
(49, '2025-09-06 15:43:37.547454', 'ajuste', 1, 998, 997, 'Ajuste manual de stock', NULL, 31, NULL),
(50, '2025-09-06 15:43:37.547454', 'venta', 1, 998, 997, 'Venta', 'F-2025-000025', 31, 2),
(51, '2025-09-06 15:44:16.634424', 'ajuste', 1, 999, 998, 'Ajuste manual de stock', NULL, 32, NULL),
(52, '2025-09-06 15:44:16.634424', 'venta', 1, 999, 998, 'Venta', 'F-2025-000026', 32, 2),
(53, '2025-09-06 15:50:02.883860', 'ajuste', 1, 997, 996, 'Ajuste manual de stock', NULL, 31, NULL),
(54, '2025-09-06 15:50:02.883860', 'venta', 1, 997, 996, 'Venta', 'F-2025-000027', 31, 2),
(55, '2025-09-06 15:50:34.300050', 'ajuste', 1, 998, 997, 'Ajuste manual de stock', NULL, 32, NULL),
(56, '2025-09-06 15:50:34.300050', 'venta', 1, 998, 997, 'Venta', 'F-2025-000028', 32, 2),
(57, '2025-09-09 02:26:12.209847', 'ajuste', 1, 996, 995, 'Ajuste manual de stock', NULL, 31, NULL),
(58, '2025-09-09 02:26:12.212378', 'venta', 1, 996, 995, 'Venta', 'F-2025-000029', 31, 2),
(59, '2025-09-09 03:25:05.429412', 'ajuste', 1, 995, 994, 'Ajuste manual de stock', NULL, 31, NULL),
(60, '2025-09-09 03:25:05.433675', 'venta', 1, 995, 994, 'Venta', 'F-2025-000030', 31, 2),
(61, '2025-09-09 04:24:26.748722', 'ajuste', 1, 997, 996, 'Ajuste manual de stock', NULL, 32, NULL),
(62, '2025-09-09 04:24:26.796912', 'ajuste', 1, 997, 996, 'Ajuste manual desde sistema de reabastecimiento', NULL, 32, 2),
(63, '2025-09-09 04:25:01.958557', 'ajuste', 1, 996, 997, 'Ajuste manual de stock', NULL, 32, NULL),
(64, '2025-09-09 04:25:01.969064', 'ajuste', 1, 996, 997, 'Ajuste manual desde sistema de reabastecimiento', NULL, 32, 2),
(65, '2025-09-09 04:25:02.177874', 'ajuste', 1, 997, 998, 'Ajuste manual de stock', NULL, 32, NULL),
(66, '2025-09-09 04:25:02.203826', 'ajuste', 1, 997, 998, 'Ajuste manual desde sistema de reabastecimiento', NULL, 32, 2),
(67, '2025-09-09 04:25:02.410404', 'ajuste', 1, 998, 999, 'Ajuste manual de stock', NULL, 32, NULL),
(68, '2025-09-09 04:25:02.422186', 'ajuste', 1, 998, 999, 'Ajuste manual desde sistema de reabastecimiento', NULL, 32, 2),
(69, '2025-09-09 04:25:02.909036', 'ajuste', 1, 999, 1000, 'Ajuste manual de stock', NULL, 32, NULL),
(70, '2025-09-09 04:25:02.923130', 'ajuste', 1, 999, 1000, 'Ajuste manual desde sistema de reabastecimiento', NULL, 32, 2),
(71, '2025-09-11 22:34:52.259487', 'ajuste', 1, 994, 993, 'Ajuste manual de stock', NULL, 31, NULL),
(72, '2025-09-11 22:34:52.426496', 'venta', 1, 994, 993, 'Venta', 'F-2025-000031', 31, 1),
(73, '2025-09-11 22:34:52.519485', 'ajuste', 1, 1000, 999, 'Ajuste manual de stock', NULL, 32, NULL),
(74, '2025-09-11 22:34:52.521492', 'venta', 1, 1000, 999, 'Venta', 'F-2025-000031', 32, 1),
(75, '2025-09-11 22:36:15.593639', 'ajuste', 1, 993, 992, 'Ajuste manual de stock', NULL, 31, NULL),
(76, '2025-09-11 22:36:15.597655', 'venta', 1, 993, 992, 'Venta', 'F-2025-000032', 31, 1),
(77, '2025-09-11 22:37:08.798562', 'ajuste', 1, 999, 998, 'Ajuste manual de stock', NULL, 32, NULL),
(78, '2025-09-11 22:37:08.802553', 'venta', 1, 999, 998, 'Venta', 'F-2025-000033', 32, 1),
(79, '2025-09-17 02:22:07.865589', 'ajuste', 1, 992, 991, 'Ajuste manual de stock', NULL, 31, NULL),
(80, '2025-09-17 02:22:07.871842', 'venta', 1, 992, 991, 'Venta', 'F-2025-000034', 31, 1),
(81, '2025-09-17 02:28:38.669315', 'ajuste', 1, 991, 990, 'Ajuste manual de stock', NULL, 31, NULL),
(82, '2025-09-17 02:28:38.669315', 'venta', 1, 991, 990, 'Venta', 'F-2025-000035', 31, 1),
(83, '2025-09-17 02:31:32.968886', 'ajuste', 1, 990, 989, 'Ajuste manual de stock', NULL, 31, NULL),
(84, '2025-09-17 02:31:32.969942', 'venta', 1, 990, 989, 'Venta', 'F-2025-000036', 31, 1),
(85, '2025-09-17 02:38:22.870394', 'ajuste', 1, 998, 997, 'Ajuste manual de stock', NULL, 32, NULL),
(86, '2025-09-17 02:38:22.882935', 'venta', 1, 998, 997, 'Venta', 'F-2025-000037', 32, 1),
(87, '2025-09-17 02:38:56.062341', 'ajuste', 1, 989, 988, 'Ajuste manual de stock', NULL, 31, NULL),
(88, '2025-09-17 02:38:56.064336', 'venta', 1, 989, 988, 'Venta', 'F-2025-000038', 31, 1),
(89, '2025-09-17 02:39:38.297461', 'ajuste', 1, 988, 987, 'Ajuste manual de stock', NULL, 31, NULL),
(90, '2025-09-17 02:39:38.300865', 'venta', 1, 988, 987, 'Venta', 'F-2025-000039', 31, 1),
(91, '2025-09-17 03:23:42.628377', 'ajuste', 1, 987, 986, 'Ajuste manual de stock', NULL, 31, NULL),
(92, '2025-09-17 03:23:42.630590', 'venta', 1, 987, 986, 'Venta', 'F-2025-000040', 31, 1),
(93, '2025-09-17 05:04:54.775316', 'ajuste', 1, 986, 985, 'Ajuste manual de stock', NULL, 31, NULL),
(94, '2025-09-17 05:04:54.790580', 'venta', 1, 986, 985, 'Venta', 'F-2025-000041', 31, 1),
(95, '2025-09-17 13:45:26.061454', 'ajuste', 1, 20, 19, 'Ajuste manual de stock', NULL, 34, NULL),
(96, '2025-09-17 13:45:26.297804', 'venta', 1, 20, 19, 'Venta', 'F-2025-000042', 34, 1),
(97, '2025-09-18 15:38:56.623328', 'ajuste', 1, 997, 996, 'Ajuste manual de stock', NULL, 32, NULL),
(98, '2025-09-18 15:46:42.824509', 'ajuste', 1, 19, 18, 'Ajuste manual de stock', NULL, 34, NULL),
(99, '2025-09-18 15:48:28.308041', 'ajuste', 1, 18, 17, 'Ajuste manual de stock', NULL, 34, NULL),
(100, '2025-09-18 16:03:21.128540', 'ajuste', 1, 17, 16, 'Ajuste manual de stock', NULL, 34, NULL),
(101, '2025-09-18 18:59:01.383751', 'ajuste', 1, 16, 15, 'Ajuste manual de stock', NULL, 34, NULL),
(102, '2025-09-18 21:50:47.394407', 'ajuste', 1, 15, 14, 'Ajuste manual de stock', NULL, 34, NULL),
(103, '2025-09-18 23:28:31.934287', 'ajuste', 1, 14, 13, 'Ajuste manual de stock', NULL, 34, NULL),
(104, '2025-09-19 00:26:54.897444', 'ajuste', 1, 13, 14, 'Ajuste manual de stock', NULL, 34, NULL),
(105, '2025-09-19 00:27:44.394703', 'ajuste', 1, 14, 15, 'Ajuste manual de stock', NULL, 34, NULL),
(106, '2025-09-19 03:09:56.874082', 'ajuste', 1, 15, 16, 'Ajuste manual de stock', NULL, 34, NULL),
(107, '2025-09-19 03:09:56.886082', 'devolucion', 1, 15, 16, 'Devolución - defectuoso', 'Factura: F-2025-000046', 34, 3),
(108, '2025-09-19 03:13:34.063147', 'ajuste', 1, 16, 15, 'Ajuste manual de stock', NULL, 34, NULL),
(109, '2025-09-19 03:53:05.304342', 'ajuste', 1, 15, 14, 'Ajuste manual de stock', NULL, 34, NULL),
(110, '2025-09-19 04:52:34.433889', 'ajuste', 1, 14, 13, 'Ajuste manual de stock', NULL, 34, NULL),
(111, '2025-09-19 04:54:31.534895', 'ajuste', 1, 13, 12, 'Ajuste manual de stock', NULL, 34, NULL),
(112, '2025-09-19 04:57:46.616340', 'ajuste', 1, 12, 11, 'Ajuste manual de stock', NULL, 34, NULL),
(113, '2025-09-19 04:59:49.949196', 'ajuste', 1, 11, 10, 'Ajuste manual de stock', NULL, 34, NULL),
(114, '2025-09-19 05:38:01.699459', 'ajuste', 1, 10, 9, 'Ajuste manual de stock', NULL, 34, NULL),
(115, '2025-09-19 05:38:51.869017', 'ajuste', 1, 9, 8, 'Ajuste manual de stock', NULL, 34, NULL),
(116, '2025-09-19 05:39:56.571423', 'ajuste', 1, 8, 7, 'Ajuste manual de stock', NULL, 34, NULL),
(117, '2025-09-19 05:52:07.312422', 'ajuste', 1, 7, 6, 'Ajuste manual de stock', NULL, 34, NULL),
(118, '2025-09-19 05:52:58.230666', 'ajuste', 1, 6, 5, 'Ajuste manual de stock', NULL, 34, NULL),
(119, '2025-09-19 06:51:21.443110', 'ajuste', 1, 5, 4, 'Ajuste manual de stock', NULL, 34, NULL),
(120, '2025-09-19 06:52:26.719315', 'ajuste', 1, 4, 3, 'Ajuste manual de stock', NULL, 34, NULL),
(121, '2025-09-19 07:02:36.611374', 'ajuste', 1, 3, 2, 'Ajuste manual de stock', NULL, 34, NULL),
(122, '2025-09-19 07:03:20.934392', 'ajuste', 1, 2, 1, 'Ajuste manual de stock', NULL, 34, NULL),
(123, '2025-09-19 07:12:55.322676', 'ajuste', 1, 10000, 9999, 'Ajuste manual de stock', NULL, 34, NULL),
(124, '2025-09-19 07:13:49.647592', 'ajuste', 1, 9999, 9998, 'Ajuste manual de stock', NULL, 34, NULL),
(125, '2025-09-19 07:17:22.539977', 'ajuste', 1, 9998, 9999, 'Ajuste manual de stock', NULL, 34, NULL),
(126, '2025-09-19 07:17:22.546994', 'devolucion', 1, 9998, 9999, 'Devolución - defectuoso', 'Factura: F-2025-000065', 34, 3),
(127, '2025-09-19 13:06:42.761272', 'ajuste', 1, 9999, 9998, 'Ajuste manual de stock', NULL, 34, NULL),
(128, '2025-09-19 13:09:40.434941', 'ajuste', 1, 9998, 9997, 'Ajuste manual de stock', NULL, 34, NULL),
(129, '2025-09-19 13:37:19.681120', 'ajuste', 1, 9997, 9996, 'Ajuste manual de stock', NULL, 34, NULL),
(130, '2025-09-19 13:48:41.754632', 'ajuste', 1, 9996, 9995, 'Ajuste manual de stock', NULL, 34, NULL),
(131, '2025-09-19 14:12:05.997838', 'ajuste', 1, 9995, 9994, 'Ajuste manual de stock', NULL, 34, NULL),
(132, '2025-09-19 15:15:15.027081', 'ajuste', 1, 9994, 9995, 'Ajuste manual de stock', NULL, 34, NULL),
(133, '2025-09-19 15:15:15.040085', 'ajuste', 1, 9994, 9995, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(134, '2025-09-19 15:15:15.250085', 'ajuste', 1, 9995, 9996, 'Ajuste manual de stock', NULL, 34, NULL),
(135, '2025-09-19 15:15:15.256090', 'ajuste', 1, 9995, 9996, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(136, '2025-09-19 15:15:15.487082', 'ajuste', 1, 9996, 9997, 'Ajuste manual de stock', NULL, 34, NULL),
(137, '2025-09-19 15:15:15.493082', 'ajuste', 1, 9996, 9997, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(138, '2025-09-19 15:15:15.613081', 'ajuste', 1, 9997, 9998, 'Ajuste manual de stock', NULL, 34, NULL),
(139, '2025-09-19 15:15:15.619083', 'ajuste', 1, 9997, 9998, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(140, '2025-09-19 15:15:15.809078', 'ajuste', 1, 9998, 9999, 'Ajuste manual de stock', NULL, 34, NULL),
(141, '2025-09-19 15:15:15.813080', 'ajuste', 1, 9998, 9999, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(142, '2025-09-19 15:15:16.031078', 'ajuste', 1, 9999, 10000, 'Ajuste manual de stock', NULL, 34, NULL),
(143, '2025-09-19 15:15:16.037081', 'ajuste', 1, 9999, 10000, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(144, '2025-09-19 15:15:16.870081', 'ajuste', 1, 10000, 10001, 'Ajuste manual de stock', NULL, 34, NULL),
(145, '2025-09-19 15:15:16.876078', 'ajuste', 1, 10000, 10001, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(146, '2025-09-19 15:15:18.747076', 'ajuste', 1, 10001, 10000, 'Ajuste manual de stock', NULL, 34, NULL),
(147, '2025-09-19 15:15:18.753081', 'ajuste', 1, 10001, 10000, 'Ajuste manual desde sistema de reabastecimiento', NULL, 34, 1),
(148, '2025-09-19 15:15:30.310869', 'ajuste', 496, 4, 500, 'Ajuste manual de stock', NULL, 33, NULL),
(149, '2025-09-19 15:15:30.328875', 'ajuste', 496, 4, 500, 'Ajuste manual desde sistema de reabastecimiento', NULL, 33, 1),
(150, '2025-09-19 19:04:59.313090', 'ajuste', 1, 10000, 9999, 'Ajuste manual de stock', NULL, 34, NULL),
(151, '2025-09-19 19:38:10.524234', 'ajuste', 1, 9999, 9998, 'Ajuste manual de stock', NULL, 34, NULL),
(152, '2025-09-19 19:40:31.716333', 'ajuste', 1, 9998, 9997, 'Ajuste manual de stock', NULL, 34, NULL),
(153, '2025-09-19 19:54:41.027579', 'ajuste', 1, 9997, 9996, 'Ajuste manual de stock', NULL, 34, NULL),
(154, '2025-09-19 19:56:34.661019', 'ajuste', 1, 9996, 9995, 'Ajuste manual de stock', NULL, 34, NULL),
(155, '2025-09-19 20:22:49.879083', 'ajuste', 1, 9995, 9994, 'Ajuste manual de stock', NULL, 34, NULL),
(156, '2025-09-19 20:44:12.896108', 'ajuste', 1, 9994, 9993, 'Ajuste manual de stock', NULL, 34, NULL),
(157, '2025-09-19 20:52:39.392505', 'ajuste', 1, 9993, 9992, 'Ajuste manual de stock', NULL, 34, NULL),
(158, '2025-09-19 20:55:07.759636', 'ajuste', 1, 9992, 9991, 'Ajuste manual de stock', NULL, 34, NULL),
(159, '2025-09-19 21:07:03.483224', 'ajuste', 1, 9991, 9990, 'Ajuste manual de stock', NULL, 34, NULL),
(160, '2025-09-19 21:22:36.357758', 'ajuste', 1, 9990, 9989, 'Ajuste manual de stock', NULL, 34, NULL),
(161, '2025-09-19 23:02:08.647842', 'ajuste', 1, 9989, 9988, 'Ajuste manual de stock', NULL, 34, NULL),
(162, '2025-09-19 23:16:01.815649', 'ajuste', 1, 9988, 9987, 'Ajuste manual de stock', NULL, 34, NULL),
(163, '2025-09-20 00:10:46.131591', 'ajuste', 1, 9987, 9986, 'Ajuste manual de stock', NULL, 34, NULL),
(164, '2025-09-20 00:19:15.836656', 'ajuste', 1, 9986, 9987, 'Ajuste manual de stock', NULL, 34, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos_cuentas_por_cobrar`
--

CREATE TABLE `pagos_cuentas_por_cobrar` (
  `id` bigint(20) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(15) NOT NULL,
  `referencia` varchar(50) NOT NULL,
  `fecha_pago` datetime(6) NOT NULL,
  `observaciones` longtext NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `cuenta_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos_cuentas_por_cobrar`
--

INSERT INTO `pagos_cuentas_por_cobrar` (`id`, `monto`, `metodo_pago`, `referencia`, `fecha_pago`, `observaciones`, `fecha_registro`, `cuenta_id`) VALUES
(8, 4500.00, 'efectivo', '', '2025-09-19 21:38:44.271152', '', '2025-09-19 21:38:44.273150', 37),
(9, 1000.00, 'efectivo', '765', '2025-09-19 22:07:42.287726', 'jk', '2025-09-19 22:07:42.287726', 38),
(10, 1000.00, 'efectivo', '89', '2025-09-19 22:09:41.528916', 'wu', '2025-09-19 22:09:41.529921', 38),
(11, 1000.00, 'efectivo', '8989', '2025-09-19 22:10:54.515742', '9909', '2025-09-19 22:10:54.515742', 38),
(12, 1000.00, 'efectivo', '98', '2025-09-19 22:29:52.148776', 'q8', '2025-09-19 22:29:52.149772', 38),
(13, 42400.00, 'efectivo', '54', '2025-09-19 22:37:26.177027', '34', '2025-09-19 22:37:26.177027', 38),
(14, 5000.00, 'efectivo', '562', '2025-09-19 23:03:13.774011', 'veo', '2025-09-19 23:03:13.775024', 39),
(15, 9000.00, 'efectivo', '162', '2025-09-19 23:04:11.484117', '', '2025-09-19 23:04:11.484117', 39),
(16, 400.00, 'efectivo', '123', '2025-09-19 23:08:00.921367', '', '2025-09-19 23:08:00.921367', 39),
(17, 30000.00, 'efectivo', '001', '2025-09-19 23:14:20.798269', 'pago  completo', '2025-09-19 23:14:20.798269', 39),
(18, 39900.00, 'efectivo', '002', '2025-09-19 23:15:13.552179', 'otro', '2025-09-19 23:15:13.553175', 37),
(19, 5000.00, 'efectivo', '003', '2025-09-19 23:17:52.894036', '', '2025-09-19 23:17:52.896057', 40),
(20, 44400.00, 'efectivo', '005', '2025-09-19 23:24:21.104287', '', '2025-09-19 23:24:21.105284', 36);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `phon`
--

CREATE TABLE `phon` (
  `id` int(11) NOT NULL,
  `nombre` varchar(678) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id` bigint(20) NOT NULL,
  `numero_factura` varchar(20) NOT NULL,
  `fecha_venta` datetime(6) NOT NULL,
  `cliente_nombre` varchar(100) NOT NULL,
  `cliente_documento` varchar(20) NOT NULL,
  `tipo_venta` varchar(10) NOT NULL,
  `metodo_pago` varchar(15) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `descuento_porcentaje` decimal(5,2) NOT NULL,
  `descuento_monto` decimal(10,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `efectivo_recibido` decimal(12,2) NOT NULL,
  `cambio` decimal(12,2) NOT NULL,
  `completada` tinyint(1) NOT NULL,
  `anulada` tinyint(1) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `cliente_id` bigint(20) DEFAULT NULL,
  `vendedor_id` int(11) NOT NULL,
  `cuota_mensual` decimal(12,2) NOT NULL,
  `es_financiada` tinyint(1) NOT NULL,
  `interes_total` decimal(12,2) NOT NULL,
  `monto_financiado` decimal(12,2) NOT NULL,
  `plazo_meses` int(10) UNSIGNED NOT NULL CHECK (`plazo_meses` >= 0),
  `tasa_interes` decimal(5,2) NOT NULL,
  `total_con_interes` decimal(12,2) NOT NULL,
  `montoinicial` decimal(12,2) NOT NULL,
  `fecha_anulacion` datetime(6) DEFAULT NULL,
  `motivo_anulacion` longtext DEFAULT NULL,
  `usuario_anulacion_id` int(11) DEFAULT NULL,
  `total_a_pagar` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id`, `numero_factura`, `fecha_venta`, `cliente_nombre`, `cliente_documento`, `tipo_venta`, `metodo_pago`, `subtotal`, `descuento_porcentaje`, `descuento_monto`, `total`, `efectivo_recibido`, `cambio`, `completada`, `anulada`, `fecha_registro`, `fecha_actualizacion`, `cliente_id`, `vendedor_id`, `cuota_mensual`, `es_financiada`, `interes_total`, `monto_financiado`, `plazo_meses`, `tasa_interes`, `total_con_interes`, `montoinicial`, `fecha_anulacion`, `motivo_anulacion`, `usuario_anulacion_id`, `total_a_pagar`) VALUES
(9, 'F-2025-000008', '2025-08-30 21:01:45.978705', 'rafel', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 31000.00, 1000.00, 1, 0, '2025-08-30 21:01:46.026826', '2025-08-30 21:01:46.026826', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(10, 'F-2025-000009', '2025-09-01 12:05:04.214061', 'jose Miguel b. Acosta', '402-2834666-6', 'credito', 'efectivo', 30000.00, 80.00, 24000.00, 6000.00, 0.00, 0.00, 1, 0, '2025-09-01 12:05:04.372542', '2025-09-01 12:05:04.372542', 1, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(11, 'F-2025-000010', '2025-09-01 12:53:24.371650', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 0.00, 0.00, 1, 0, '2025-09-01 12:53:24.379668', '2025-09-01 12:53:24.379668', 2, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(12, 'F-2025-000011', '2025-09-01 14:53:03.603711', 'joel', '00000000001', 'contado', 'efectivo', 5000.00, 0.00, 0.00, 5000.00, 6000.00, 1000.00, 1, 0, '2025-09-01 14:53:03.674870', '2025-09-01 14:53:03.674870', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(13, 'F-2025-000012', '2025-09-01 15:00:13.903393', 'Joel Piña', '445-4544446-4', 'credito', 'efectivo', 5000.00, 0.00, 0.00, 5000.00, 0.00, 0.00, 1, 0, '2025-09-01 15:00:13.915133', '2025-09-01 15:00:13.915133', 3, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(14, 'F-2025-000013', '2025-09-01 15:32:53.737805', 'jose miguel', '00000000001', 'contado', 'efectivo', 30000.00, 5.00, 1500.00, 28500.00, 30000.00, 1500.00, 1, 0, '2025-09-01 15:32:53.754749', '2025-09-01 15:32:53.754749', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(15, 'F-2025-000014', '2025-09-01 15:37:34.188925', 'Maria Moncion', '665-6556656-5', 'credito', 'efectivo', 30000.00, 76.00, 22800.00, 7200.00, 0.00, 0.00, 1, 0, '2025-09-01 15:37:34.204374', '2025-09-01 15:37:34.204374', 4, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(16, 'F-2025-000015', '2025-09-01 21:14:44.664373', 'jose Miguel b. Acosta', '402-2834666-6', 'credito', 'efectivo', 30000.00, 70.00, 21000.00, 9000.00, 0.00, 0.00, 1, 0, '2025-09-01 21:14:44.770347', '2025-09-01 21:14:44.770347', 1, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(17, 'F-2025-000016', '2025-09-02 01:37:13.350015', 'jose Miguel b. Acosta', '402-2834666-6', 'credito', 'efectivo', 30000.00, 70.00, 21000.00, 9000.00, 0.00, 0.00, 1, 0, '2025-09-02 01:37:13.480672', '2025-09-02 01:37:13.481655', 1, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(18, 'F-2025-000017', '2025-09-02 13:29:39.787029', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 0.00, 0.00, 1, 0, '2025-09-02 13:29:39.897556', '2025-09-02 13:29:39.897556', 2, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(19, 'F-2025-000018', '2025-09-02 15:34:21.920871', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 5000.00, 0.00, 0.00, 5000.00, 0.00, 0.00, 1, 0, '2025-09-02 15:34:21.938827', '2025-09-02 15:34:21.938827', 2, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(20, 'F-2025-000019', '2025-09-03 23:54:18.640274', 'jose', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-03 23:54:18.664543', '2025-09-03 23:54:18.664543', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(21, 'F-2025-000020', '2025-09-04 04:36:55.134689', 'rafel', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-04 04:36:55.137873', '2025-09-04 04:36:55.137873', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(22, 'F-2025-000021', '2025-09-06 12:06:08.641251', 'rafel', '00000000001', 'contado', 'tarjeta', 5000.00, 0.00, 0.00, 5000.00, 0.00, 0.00, 1, 0, '2025-09-06 12:06:08.721867', '2025-09-06 12:06:08.721867', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(23, 'F-2025-000022', '2025-09-06 12:23:30.405591', 'rafel', '00000000001', 'contado', 'transferencia', 5000.00, 0.00, 0.00, 5000.00, 0.00, 0.00, 1, 0, '2025-09-06 12:23:30.437625', '2025-09-06 12:23:30.437625', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(24, 'F-2025-000023', '2025-09-06 15:29:00.964203', 'rafael', '', 'contado', 'efectivo', 60000.00, 10.00, 6000.00, 54000.00, 55000.00, 1000.00, 1, 0, '2025-09-06 15:29:01.017344', '2025-09-06 15:29:01.017344', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(25, 'F-2025-000024', '2025-09-06 15:31:29.292470', 'andres', '', 'contado', 'efectivo', 5000.00, 10.00, 500.00, 4500.00, 5000.00, 500.00, 1, 0, '2025-09-06 15:31:29.353701', '2025-09-06 15:31:29.353701', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(26, 'F-2025-000025', '2025-09-06 15:43:37.496242', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 30000.00, 10.00, 3000.00, 27000.00, 0.00, 0.00, 1, 0, '2025-09-06 15:43:37.510570', '2025-09-06 15:43:37.510570', 2, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(27, 'F-2025-000026', '2025-09-06 15:44:16.611765', 'andres', '', 'contado', 'efectivo', 5000.00, 10.00, 500.00, 4500.00, 5000.00, 500.00, 1, 0, '2025-09-06 15:44:16.625911', '2025-09-06 15:44:16.625911', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(28, 'F-2025-000027', '2025-09-06 15:50:02.868179', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 0.00, 0.00, 1, 0, '2025-09-06 15:50:02.870314', '2025-09-06 15:50:02.870314', 2, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(29, 'F-2025-000028', '2025-09-06 15:50:34.266052', 'andres arias', '', 'contado', 'efectivo', 5000.00, 0.00, 0.00, 5000.00, 5000.00, 0.00, 1, 0, '2025-09-06 15:50:34.286052', '2025-09-06 15:50:34.286052', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(30, 'F-2025-000029', '2025-09-09 02:26:12.160297', 'jose', '00000000001', 'contado', 'efectivo', 30000.00, 2.00, 600.00, 29400.00, 30000.00, 600.00, 1, 0, '2025-09-09 02:26:12.184960', '2025-09-09 02:26:12.184960', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(31, 'F-2025-000030', '2025-09-09 03:25:05.386738', 'rafel', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-09 03:25:05.407859', '2025-09-09 03:25:05.407859', NULL, 2, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(32, 'F-2025-000031', '2025-09-11 22:34:51.984952', 'rafael', '', 'contado', 'efectivo', 35000.00, 10.00, 3500.00, 31500.00, 32000.00, 500.00, 1, 0, '2025-09-11 22:34:52.232494', '2025-09-11 22:34:52.232494', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(33, 'F-2025-000032', '2025-09-11 22:36:15.423685', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 30000.00, 10.00, 3000.00, 27000.00, 0.00, 0.00, 1, 0, '2025-09-11 22:36:15.513638', '2025-09-11 22:36:15.513638', 2, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(34, 'F-2025-000033', '2025-09-11 22:37:08.773559', 'Rafael Acosta', '402-2834666-8', 'credito', 'tarjeta', 5000.00, 10.00, 500.00, 4500.00, 0.00, 0.00, 1, 0, '2025-09-11 22:37:08.786597', '2025-09-11 22:37:08.787605', 2, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(35, 'F-2025-000034', '2025-09-17 02:22:07.838383', 'jose', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-17 02:22:07.854257', '2025-09-17 02:22:07.854257', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(36, 'F-2025-000035', '2025-09-17 02:28:38.619972', 'rafel', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-17 02:28:38.658749', '2025-09-17 02:28:38.658749', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(37, 'F-2025-000036', '2025-09-17 02:31:32.944325', 'alex', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-17 02:31:32.956391', '2025-09-17 02:31:32.956391', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(38, 'F-2025-000037', '2025-09-17 02:38:22.784475', 'hvfhv', '', 'contado', 'efectivo', 5000.00, 0.00, 0.00, 5000.00, 5000.00, 0.00, 1, 0, '2025-09-17 02:38:22.838557', '2025-09-17 02:38:22.838557', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(39, 'F-2025-000038', '2025-09-17 02:38:56.018780', 'rafel', '', 'contado', 'tarjeta', 30000.00, 0.00, 0.00, 30000.00, 0.00, 0.00, 1, 0, '2025-09-17 02:38:56.037280', '2025-09-17 02:38:56.037280', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(40, 'F-2025-000039', '2025-09-17 02:39:38.250226', 'Rafael Acosta', '402-2834666-8', 'credito', 'tarjeta', 30000.00, 0.00, 0.00, 30000.00, 0.00, 0.00, 1, 0, '2025-09-17 02:39:38.274739', '2025-09-17 02:39:38.274739', 2, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(41, 'F-2025-000040', '2025-09-17 03:23:42.585057', 'rafel', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-17 03:23:42.613610', '2025-09-17 03:23:42.613610', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(42, 'F-2025-000041', '2025-09-17 05:04:54.763226', 'rafel', '00000000001', 'contado', 'efectivo', 30000.00, 0.00, 0.00, 30000.00, 30000.00, 0.00, 1, 0, '2025-09-17 05:04:54.773160', '2025-09-17 05:04:54.773160', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(43, 'F-2025-000042', '2025-09-17 13:45:25.941893', 'jose', '00000000001', 'contado', 'efectivo', 60000.00, 2.00, 1200.00, 58800.00, 60000.00, 1200.00, 1, 0, '2025-09-17 13:45:26.034115', '2025-09-17 13:45:26.034115', NULL, 1, 0.00, 0, 0.00, 0.00, 1, 0.00, 0.00, 1.00, NULL, NULL, NULL, 0.00),
(44, 'F-2025-000043', '2025-09-18 15:38:56.574596', 'Rafael Acosta', '402-2834666-8', 'credito', 'efectivo', 5000.00, 0.00, 0.00, 4080.00, 0.00, 0.00, 1, 0, '2025-09-18 15:38:56.607666', '2025-09-18 15:38:56.607666', 2, 1, 340.00, 1, 1080.00, 3000.00, 12, 3.00, 4080.00, 2000.00, NULL, NULL, NULL, 0.00),
(45, 'F-2025-000044', '2025-09-18 15:46:42.803545', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-18 15:46:42.805543', '2025-09-18 15:46:42.805543', 6, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(47, 'F-2025-000045', '2025-09-18 16:03:21.103102', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 1, '2025-09-18 16:03:21.106222', '2025-09-19 00:27:44.382830', 6, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, '2025-09-19 00:27:44.378777', 'nol', 3, 0.00),
(48, 'F-2025-000046', '2025-09-18 18:59:01.226569', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 0.00, 0.00, 1000.00, -1000.00, 0.00, 0.00, 1, 0, '2025-09-18 18:59:01.355545', '2025-09-19 03:09:56.894087', 6, 1, 4420.00, 1, 14040.00, 39000.00, 12, 3.00, 63040.00, 10000.00, NULL, NULL, NULL, 0.00),
(49, 'F-2025-000047', '2025-09-18 21:50:47.275388', 'rafel', '00000000001', 'contado', 'efectivo', 50000.00, 0.00, 5.00, 49995.00, 50000.00, 5.00, 1, 0, '2025-09-18 21:50:47.343382', '2025-09-18 21:50:47.343382', NULL, 1, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(50, 'F-2025-000048', '2025-09-18 23:28:31.894289', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 1.00, 0.00, 53720.00, 0.00, 0.00, 1, 1, '2025-09-18 23:28:31.913288', '2025-09-19 00:26:54.735447', 6, 1, 4476.67, 1, 14220.00, 39500.00, 12, 3.00, 53720.00, 10000.00, '2025-09-19 00:26:54.495180', 'no le gusto', 3, 0.00),
(51, 'F-2025-000049', '2025-09-19 03:13:34.011149', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 4.00, 0.00, 51680.00, 0.00, 0.00, 1, 0, '2025-09-19 03:13:34.054148', '2025-09-19 03:13:34.054148', 6, 3, 4306.67, 1, 13680.00, 38000.00, 12, 3.00, 51680.00, 10000.00, NULL, NULL, NULL, 0.00),
(52, 'F-2025-000050', '2025-09-19 03:53:05.254455', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 4.00, 0.00, 51680.00, 0.00, 0.00, 1, 0, '2025-09-19 03:53:05.271357', '2025-09-19 03:53:05.271357', 6, 3, 4306.67, 1, 13680.00, 38000.00, 12, 3.00, 51680.00, 10000.00, NULL, NULL, NULL, 0.00),
(53, 'F-2025-000051', '2025-09-19 04:52:34.378904', 'rafel', '00000000001', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 04:52:34.418892', '2025-09-19 04:52:34.418892', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(54, 'F-2025-000052', '2025-09-19 04:54:31.399896', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 2.00, 0.00, 39440.00, 0.00, 0.00, 1, 0, '2025-09-19 04:54:31.407895', '2025-09-19 04:54:31.407895', 6, 3, 3286.67, 1, 10440.00, 29000.00, 12, 3.00, 39440.00, 20000.00, NULL, NULL, NULL, 0.00),
(55, 'F-2025-000053', '2025-09-19 04:57:46.595339', 'hjh', '', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 04:57:46.600340', '2025-09-19 04:57:46.600340', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(56, 'F-2025-000054', '2025-09-19 04:59:49.910197', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 50000.00, 0.00, 1, 0, '2025-09-19 04:59:49.914196', '2025-09-19 04:59:49.914196', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(57, 'F-2025-000055', '2025-09-19 05:38:01.651497', 'lk', '', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 05:38:01.681460', '2025-09-19 05:38:01.681460', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(58, 'F-2025-000056', '2025-09-19 05:38:51.855019', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 50000.00, 0.00, 1, 0, '2025-09-19 05:38:51.859014', '2025-09-19 05:38:51.859014', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(59, 'F-2025-000057', '2025-09-19 05:39:56.498425', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 10.00, 0.00, 47600.00, 50000.00, 0.00, 1, 0, '2025-09-19 05:39:56.506424', '2025-09-19 05:39:56.506424', 6, 3, 3966.67, 1, 12600.00, 35000.00, 12, 3.00, 47600.00, 10000.00, NULL, NULL, NULL, 0.00),
(60, 'F-2025-000058', '2025-09-19 05:52:07.294395', 'rafel', '00000000001', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 05:52:07.302406', '2025-09-19 05:52:07.302406', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(61, 'F-2025-000059', '2025-09-19 05:52:58.114669', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 05:52:58.182682', '2025-09-19 05:52:58.182682', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(62, 'F-2025-000060', '2025-09-19 06:51:21.397111', 'ldk', '', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 06:51:21.416109', '2025-09-19 06:51:21.416109', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(63, 'F-2025-000061', '2025-09-19 06:52:26.629337', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 40800.00, 50000.00, 0.00, 1, 0, '2025-09-19 06:52:26.635333', '2025-09-19 06:52:26.636331', 6, 3, 3400.00, 1, 10800.00, 30000.00, 12, 3.00, 40800.00, 20000.00, NULL, NULL, NULL, 0.00),
(64, 'F-2025-000062', '2025-09-19 07:02:36.484372', 'rafel', '00000000001', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 07:02:36.488374', '2025-09-19 07:02:36.488374', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(65, 'F-2025-000063', '2025-09-19 07:03:20.846398', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 07:03:20.850393', '2025-09-19 07:03:20.850393', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(66, 'F-2025-000064', '2025-09-19 07:12:55.198677', 'gh', '', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 07:12:55.251635', '2025-09-19 07:12:55.251635', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(67, 'F-2025-000065', '2025-09-19 07:13:49.259059', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 0.00, 0.00, 0.00, 0.00, 50000.00, 0.00, 1, 0, '2025-09-19 07:13:49.268068', '2025-09-19 07:17:22.553978', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(68, 'F-2025-000066', '2025-09-19 13:06:42.625119', 'rafel', '00000000001', 'contado', 'efectivo', 50000.00, 2.00, 0.00, 50000.00, 50000.00, 1000.00, 1, 0, '2025-09-19 13:06:42.723940', '2025-09-19 13:06:42.723940', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(69, 'F-2025-000067', '2025-09-19 13:09:40.408987', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 13:09:40.409987', '2025-09-19 13:09:40.409987', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(70, 'F-2025-000068', '2025-09-19 13:37:19.523937', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 13:37:19.540941', '2025-09-19 13:37:19.540941', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 0.00),
(71, 'F-2025-000069', '2025-09-19 13:48:41.730239', 'rafel', '00000000001', 'contado', 'efectivo', 50000.00, 0.00, 0.00, 50000.00, 50000.00, 0.00, 1, 0, '2025-09-19 13:48:41.740257', '2025-09-19 13:48:41.740257', NULL, 3, 0.00, 0, 0.00, 0.00, 0, 0.00, 0.00, 0.00, NULL, NULL, NULL, 0.00),
(72, 'F-2025-000070', '2025-09-19 14:12:05.892143', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 14:12:05.974871', '2025-09-19 14:12:05.974871', 6, 3, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(73, 'F-2025-000071', '2025-09-19 19:04:59.224056', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 19:04:59.256650', '2025-09-19 19:04:59.256650', 6, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(74, 'F-2025-000072', '2025-09-19 19:38:10.447795', 'arturo bello', '909-0004384-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 19:38:10.452976', '2025-09-19 19:38:10.452976', 7, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(75, 'F-2025-000073', '2025-09-19 19:40:31.700372', 'arturo bello', '909-0004384-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 40800.00, 0.00, 0.00, 1, 0, '2025-09-19 19:40:31.704742', '2025-09-19 19:40:31.705364', 7, 1, 3400.00, 1, 10800.00, 30000.00, 12, 3.00, 40800.00, 20000.00, NULL, NULL, NULL, 60800.00),
(76, 'F-2025-000074', '2025-09-19 19:54:40.944767', 'joel', '787-7776767-4', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 19:54:40.950718', '2025-09-19 19:54:40.950718', 8, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(77, 'F-2025-000075', '2025-09-19 19:56:34.402021', 'joel', '787-7776767-4', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 19:56:34.407486', '2025-09-19 19:56:34.407486', 8, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(78, 'F-2025-000076', '2025-09-19 20:22:49.831866', 'jay', '484-8747749-7', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 20:22:49.836759', '2025-09-19 20:22:49.836759', 9, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(79, 'F-2025-000077', '2025-09-19 20:44:12.862097', 'jay', '484-8747749-7', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 40800.00, 0.00, 0.00, 1, 0, '2025-09-19 20:44:12.868097', '2025-09-19 20:44:12.868097', 9, 1, 3400.00, 1, 10800.00, 30000.00, 12, 3.00, 40800.00, 20000.00, NULL, NULL, NULL, 60800.00),
(80, 'F-2025-000078', '2025-09-19 20:52:39.361503', 'jay', '484-8747749-7', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 20:52:39.366504', '2025-09-19 20:52:39.366504', 9, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(81, 'F-2025-000079', '2025-09-19 20:55:07.736636', 'alex acosta', '788-7428743-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 20:55:07.741635', '2025-09-19 20:55:07.741635', 6, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(82, 'F-2025-000080', '2025-09-19 21:07:03.460604', 'jay', '484-8747749-7', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 21:07:03.467606', '2025-09-19 21:07:03.467606', 9, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(83, 'F-2025-000081', '2025-09-19 21:22:36.307762', 'arturo bello', '909-0004384-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 21:22:36.315765', '2025-09-19 21:22:36.315765', 7, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(84, 'F-2025-000082', '2025-09-19 23:02:08.615845', 'jay', '484-8747749-7', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 23:02:08.626899', '2025-09-19 23:02:08.626899', 9, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(85, 'F-2025-000083', '2025-09-19 23:16:01.777647', 'arturo bello', '909-0004384-2', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-19 23:16:01.781649', '2025-09-19 23:16:01.781649', 7, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(86, 'F-2025-000084', '2025-09-20 00:10:46.037039', 'joel', '787-7776767-4', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 1, '2025-09-20 00:10:46.065847', '2025-09-20 00:19:15.805827', 8, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, '2025-09-20 00:19:15.778388', 'jjaja', 1, 64400.00);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `caja`
--
ALTER TABLE `caja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `caja_usuario_id_73ec6cff_fk_auth_user_id` (`usuario_id`);

--
-- Indices de la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cierre_caja_caja_id_bdc4df11_fk_caja_id` (`caja_id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `identification_number` (`identification_number`);

--
-- Indices de la tabla `comprobantes_pago`
--
ALTER TABLE `comprobantes_pago`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_comprobante` (`numero_comprobante`),
  ADD UNIQUE KEY `pago_id` (`pago_id`),
  ADD KEY `comprobantes_pago_cliente_id_1cb91e58_fk_clientes_id` (`cliente_id`),
  ADD KEY `comprobantes_pago_cuenta_id_5730def8_fk_cuentas_por_cobrar_id` (`cuenta_id`);

--
-- Indices de la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `venta_id` (`venta_id`),
  ADD KEY `cuentas_por_cobrar_cliente_id_2f733987_fk_clientes_id` (`cliente_id`);

--
-- Indices de la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `detalles_venta_producto_id_a8d14811_fk_facturaci` (`producto_id`),
  ADD KEY `detalles_venta_venta_id_8487699d_fk_ventas_id` (`venta_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `facturacion_devolucion`
--
ALTER TABLE `facturacion_devolucion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `facturacion_devoluci_producto_id_c8b06715_fk_facturaci` (`producto_id`),
  ADD KEY `facturacion_devolucion_usuario_id_988eb9c0_fk_auth_user_id` (`usuario_id`),
  ADD KEY `facturacion_devolucion_venta_id_2d99fa67_fk_ventas_id` (`venta_id`);

--
-- Indices de la tabla `facturacion_entradaproducto`
--
ALTER TABLE `facturacion_entradaproducto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_producto` (`codigo_producto`),
  ADD UNIQUE KEY `imei_serial` (`imei_serial`),
  ADD KEY `facturacion_entradap_proveedor_id_83cda334_fk_facturaci` (`proveedor_id`);

--
-- Indices de la tabla `facturacion_proveedor`
--
ALTER TABLE `facturacion_proveedor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `movimientos_stock`
--
ALTER TABLE `movimientos_stock`
  ADD PRIMARY KEY (`id`),
  ADD KEY `movimientos_stock_producto_id_1d9c3cd8_fk_facturaci` (`producto_id`),
  ADD KEY `movimientos_stock_usuario_id_1e45edce_fk_auth_user_id` (`usuario_id`);

--
-- Indices de la tabla `pagos_cuentas_por_cobrar`
--
ALTER TABLE `pagos_cuentas_por_cobrar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pagos_cuentas_por_co_cuenta_id_545a6003_fk_cuentas_p` (`cuenta_id`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_factura` (`numero_factura`),
  ADD KEY `ventas_cliente_id_30fc3b9d_fk_clientes_id` (`cliente_id`),
  ADD KEY `ventas_vendedor_id_4047adb4_fk_auth_user_id` (`vendedor_id`),
  ADD KEY `ventas_usuario_anulacion_id_7fdc93f9_fk_auth_user_id` (`usuario_anulacion_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `caja`
--
ALTER TABLE `caja`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `comprobantes_pago`
--
ALTER TABLE `comprobantes_pago`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `facturacion_devolucion`
--
ALTER TABLE `facturacion_devolucion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `facturacion_entradaproducto`
--
ALTER TABLE `facturacion_entradaproducto`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `facturacion_proveedor`
--
ALTER TABLE `facturacion_proveedor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `movimientos_stock`
--
ALTER TABLE `movimientos_stock`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=165;

--
-- AUTO_INCREMENT de la tabla `pagos_cuentas_por_cobrar`
--
ALTER TABLE `pagos_cuentas_por_cobrar`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `caja`
--
ALTER TABLE `caja`
  ADD CONSTRAINT `caja_usuario_id_73ec6cff_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  ADD CONSTRAINT `cierre_caja_caja_id_bdc4df11_fk_caja_id` FOREIGN KEY (`caja_id`) REFERENCES `caja` (`id`);

--
-- Filtros para la tabla `comprobantes_pago`
--
ALTER TABLE `comprobantes_pago`
  ADD CONSTRAINT `comprobantes_pago_cliente_id_1cb91e58_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `comprobantes_pago_cuenta_id_5730def8_fk_cuentas_por_cobrar_id` FOREIGN KEY (`cuenta_id`) REFERENCES `cuentas_por_cobrar` (`id`),
  ADD CONSTRAINT `comprobantes_pago_pago_id_9d3b5395_fk_pagos_cue` FOREIGN KEY (`pago_id`) REFERENCES `pagos_cuentas_por_cobrar` (`id`);

--
-- Filtros para la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  ADD CONSTRAINT `cuentas_por_cobrar_cliente_id_2f733987_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `cuentas_por_cobrar_venta_id_e0896fce_fk_ventas_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`);

--
-- Filtros para la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  ADD CONSTRAINT `detalles_venta_producto_id_a8d14811_fk_facturaci` FOREIGN KEY (`producto_id`) REFERENCES `facturacion_entradaproducto` (`id`),
  ADD CONSTRAINT `detalles_venta_venta_id_8487699d_fk_ventas_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `facturacion_devolucion`
--
ALTER TABLE `facturacion_devolucion`
  ADD CONSTRAINT `facturacion_devoluci_producto_id_c8b06715_fk_facturaci` FOREIGN KEY (`producto_id`) REFERENCES `facturacion_entradaproducto` (`id`),
  ADD CONSTRAINT `facturacion_devolucion_usuario_id_988eb9c0_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `facturacion_devolucion_venta_id_2d99fa67_fk_ventas_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`);

--
-- Filtros para la tabla `facturacion_entradaproducto`
--
ALTER TABLE `facturacion_entradaproducto`
  ADD CONSTRAINT `facturacion_entradap_proveedor_id_83cda334_fk_facturaci` FOREIGN KEY (`proveedor_id`) REFERENCES `facturacion_proveedor` (`id`);

--
-- Filtros para la tabla `movimientos_stock`
--
ALTER TABLE `movimientos_stock`
  ADD CONSTRAINT `movimientos_stock_producto_id_1d9c3cd8_fk_facturaci` FOREIGN KEY (`producto_id`) REFERENCES `facturacion_entradaproducto` (`id`),
  ADD CONSTRAINT `movimientos_stock_usuario_id_1e45edce_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `pagos_cuentas_por_cobrar`
--
ALTER TABLE `pagos_cuentas_por_cobrar`
  ADD CONSTRAINT `pagos_cuentas_por_co_cuenta_id_545a6003_fk_cuentas_p` FOREIGN KEY (`cuenta_id`) REFERENCES `cuentas_por_cobrar` (`id`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_cliente_id_30fc3b9d_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `ventas_usuario_anulacion_id_7fdc93f9_fk_auth_user_id` FOREIGN KEY (`usuario_anulacion_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `ventas_vendedor_id_4047adb4_fk_auth_user_id` FOREIGN KEY (`vendedor_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
