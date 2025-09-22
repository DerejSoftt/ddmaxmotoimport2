-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-09-2025 a las 20:46:26
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
-- Base de datos: `ddmaxmotoimport`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(17, 'Can add Venta', 5, 'add_venta'),
(18, 'Can change Venta', 5, 'change_venta'),
(19, 'Can delete Venta', 5, 'delete_venta'),
(20, 'Can view Venta', 5, 'view_venta'),
(21, 'Can add Detalle de Venta', 6, 'add_detalleventa'),
(22, 'Can change Detalle de Venta', 6, 'change_detalleventa'),
(23, 'Can delete Detalle de Venta', 6, 'delete_detalleventa'),
(24, 'Can view Detalle de Venta', 6, 'view_detalleventa'),
(25, 'Can add movimiento stock', 7, 'add_movimientostock'),
(26, 'Can change movimiento stock', 7, 'change_movimientostock'),
(27, 'Can delete movimiento stock', 7, 'delete_movimientostock'),
(28, 'Can view movimiento stock', 7, 'view_movimientostock'),
(29, 'Can add Cuenta por Cobrar', 8, 'add_cuentaporcobrar'),
(30, 'Can change Cuenta por Cobrar', 8, 'change_cuentaporcobrar'),
(31, 'Can delete Cuenta por Cobrar', 8, 'delete_cuentaporcobrar'),
(32, 'Can view Cuenta por Cobrar', 8, 'view_cuentaporcobrar'),
(33, 'Can add Pago de Cuenta por Cobrar', 9, 'add_pagocuentaporcobrar'),
(34, 'Can change Pago de Cuenta por Cobrar', 9, 'change_pagocuentaporcobrar'),
(35, 'Can delete Pago de Cuenta por Cobrar', 9, 'delete_pagocuentaporcobrar'),
(36, 'Can view Pago de Cuenta por Cobrar', 9, 'view_pagocuentaporcobrar'),
(37, 'Can add Cierre de Caja', 10, 'add_cierrecaja'),
(38, 'Can change Cierre de Caja', 10, 'change_cierrecaja'),
(39, 'Can delete Cierre de Caja', 10, 'delete_cierrecaja'),
(40, 'Can view Cierre de Caja', 10, 'view_cierrecaja'),
(41, 'Can add devolucion', 11, 'add_devolucion'),
(42, 'Can change devolucion', 11, 'change_devolucion'),
(43, 'Can delete devolucion', 11, 'delete_devolucion'),
(44, 'Can view devolucion', 11, 'view_devolucion'),
(45, 'Can add Comprobante de Pago', 12, 'add_comprobantepago'),
(46, 'Can change Comprobante de Pago', 12, 'change_comprobantepago'),
(47, 'Can delete Comprobante de Pago', 12, 'delete_comprobantepago'),
(48, 'Can view Comprobante de Pago', 12, 'view_comprobantepago'),
(49, 'Can add log entry', 13, 'add_logentry'),
(50, 'Can change log entry', 13, 'change_logentry'),
(51, 'Can delete log entry', 13, 'delete_logentry'),
(52, 'Can view log entry', 13, 'view_logentry'),
(53, 'Can add permission', 14, 'add_permission'),
(54, 'Can change permission', 14, 'change_permission'),
(55, 'Can delete permission', 14, 'delete_permission'),
(56, 'Can view permission', 14, 'view_permission'),
(57, 'Can add group', 15, 'add_group'),
(58, 'Can change group', 15, 'change_group'),
(59, 'Can delete group', 15, 'delete_group'),
(60, 'Can view group', 15, 'view_group'),
(61, 'Can add user', 16, 'add_user'),
(62, 'Can change user', 16, 'change_user'),
(63, 'Can delete user', 16, 'delete_user'),
(64, 'Can view user', 16, 'view_user'),
(65, 'Can add content type', 17, 'add_contenttype'),
(66, 'Can change content type', 17, 'change_contenttype'),
(67, 'Can delete content type', 17, 'delete_contenttype'),
(68, 'Can view content type', 17, 'view_contenttype'),
(69, 'Can add session', 18, 'add_session'),
(70, 'Can change session', 18, 'change_session'),
(71, 'Can delete session', 18, 'delete_session'),
(72, 'Can view session', 18, 'view_session');

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
(1, 'pbkdf2_sha256$600000$1MDwLmoMhKdJA8yYbmSwM2$IIGHftg+lRJqHHGaLG23FYxc4nwD7lpqxygsgoiq3C8=', '2025-09-20 18:50:46.655782', 1, 'LAMAQUINA', '', '', '', 1, 1, '2025-09-20 00:54:38.853879');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, '2025-09-20 01:06:45.213561', NULL, 0.00, NULL, 'abierta', NULL, 1);

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
(1, 'YONEYRI PEREZ ROMAN', '101-0010551-8', '(829) 601-5331', '(809) 396-1864', 'LOMA DE CASTANUELA POR LA CALLE DE RAMONA BAR ', '', 200000.00, 1, '2025-09-20 01:06:36.717864'),
(2, 'jose miguel', '998-3993898-3', '(323) 232-3232', '(433) 343-3343', 'loma', '', 700000.00, 1, '2025-09-20 19:37:51.817574'),
(3, 'JOSE ARISMENDY VASQUEZ JIMENEZ', '101-0003250-6', '(849) 361-7897', '(849) 353-5343', 'CATAÑUELAS ', '', 100000.00, 1, '2025-09-20 21:25:24.738761'),
(4, 'MERCEDES GARCIA', '117-0002037-0', '(829) 272-3284', '(000) 000-0000', 'LAS MATAS DE SANTAS ', '', 100000.00, 1, '2025-09-20 21:37:09.581815'),
(5, 'RAFAEL FRANCISCO JIMENEZ REYES', '101-0007657-8', '(849) 360-9855', '(000) 000-0000', 'LOMA DE CASTAÑUELAS', '', 100000.00, 1, '2025-09-20 21:43:28.463408'),
(7, 'ISIDRO ALMONTE REYES', '101-0000020-6', '(809) 749-6258', '(000) 000-0000', 'CATAÑUELAS ', '', 1000000.00, 1, '2025-09-20 21:54:05.424619');

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
(1, 62540.00, 45000.00, '2025-10-20', 'pendiente', 'Venta a crédito - Factura: F-2025-000001\nCliente: YONERY PEREZ ROMAN\nProductos:\nTAURO FTZ 150 x1 - RD$98000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$45000.00\n- Tasa de interés: 3% mensual\n- Plazo: 6 meses\n- Monto a Financiar: RD$53000.00\n- Interés Mensual: RD$1590.00\n- Cuota mensual: RD$10423.33\n- Ganancia por Interés: RD$9540.00\n- Total con Interés: RD$62540.00\n- Total a Pagar: RD$107540.00\n', '2025-09-20 01:50:33.532570', '2025-09-20 01:50:33.532589', 1, 1, 'TAURO FTZ 150 x1 - RD$98000.00', 0, NULL, 62540.00),
(2, 62540.00, 45000.00, '2025-10-20', 'anulada', 'Venta a crédito - Factura: F-2025-000002\nCliente: jose miguel\nProductos:\nTAURO FTZ 150 x1 - RD$98000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$45000.00\n- Tasa de interés: 3% mensual\n- Plazo: 6 meses\n- Monto a Financiar: RD$53000.00\n- Interés Mensual: RD$1590.00\n- Cuota mensual: RD$10423.33\n- Ganancia por Interés: RD$9540.00\n- Total con Interés: RD$62540.00\n- Total a Pagar: RD$107540.00\n', '2025-09-20 19:39:05.506412', '2025-09-20 20:12:57.482976', 2, 2, 'TAURO FTZ 150 x1 - RD$98000.00', 1, '2025-09-20 20:12:57.481643', 62540.00),
(3, 54400.00, 10000.00, '2025-10-20', 'anulada', 'Venta a crédito - Factura: F-2025-000003\nCliente: jose miguel\nProductos:\nTAURO FTZ 150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-20 19:56:01.847753', '2025-09-20 20:12:44.037777', 2, 3, 'TAURO FTZ 150 x1 - RD$50000.00', 1, '2025-09-20 20:12:44.036619', 54400.00),
(4, 54400.00, 10000.00, '2025-10-20', 'pendiente', 'Venta a crédito - Factura: F-2025-000004\nCliente: jose miguel\nProductos:\nTAURO FTZ 150 x1 - RD$50000.00\n\nFINANCIAMIENTO:\n- Monto Inicial: RD$10000.00\n- Tasa de interés: 3% mensual\n- Plazo: 12 meses\n- Monto a Financiar: RD$40000.00\n- Interés Mensual: RD$1200.00\n- Cuota mensual: RD$4533.33\n- Ganancia por Interés: RD$14400.00\n- Total con Interés: RD$54400.00\n- Total a Pagar: RD$64400.00\n', '2025-09-20 20:13:52.480148', '2025-09-20 20:13:52.480170', 2, 4, 'TAURO FTZ 150 x1 - RD$50000.00', 0, NULL, 54400.00);

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
(1, 1, 98000.00, 98000.00, 1, 1),
(2, 1, 98000.00, 98000.00, 1, 2),
(3, 1, 50000.00, 50000.00, 1, 3),
(4, 1, 50000.00, 50000.00, 1, 4);

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
(13, 'admin', 'logentry'),
(15, 'auth', 'group'),
(14, 'auth', 'permission'),
(16, 'auth', 'user'),
(17, 'contenttypes', 'contenttype'),
(4, 'facturacion', 'caja'),
(10, 'facturacion', 'cierrecaja'),
(1, 'facturacion', 'cliente'),
(12, 'facturacion', 'comprobantepago'),
(8, 'facturacion', 'cuentaporcobrar'),
(6, 'facturacion', 'detalleventa'),
(11, 'facturacion', 'devolucion'),
(3, 'facturacion', 'entradaproducto'),
(7, 'facturacion', 'movimientostock'),
(9, 'facturacion', 'pagocuentaporcobrar'),
(2, 'facturacion', 'proveedor'),
(5, 'facturacion', 'venta'),
(18, 'sessions', 'session');

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
(1, 'contenttypes', '0001_initial', '2025-09-20 00:49:40.952920'),
(2, 'auth', '0001_initial', '2025-09-20 00:49:41.551667'),
(3, 'admin', '0001_initial', '2025-09-20 00:49:41.659796'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-09-20 00:49:41.666488'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-20 00:49:41.674299'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-09-20 00:49:41.739847'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-09-20 00:49:41.803058'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-09-20 00:49:41.814778'),
(9, 'auth', '0004_alter_user_username_opts', '2025-09-20 00:49:41.823820'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-09-20 00:49:41.868136'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-09-20 00:49:41.870321'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-09-20 00:49:41.877520'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-09-20 00:49:41.889941'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-09-20 00:49:41.900966'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-09-20 00:49:41.929037'),
(16, 'auth', '0011_update_proxy_permissions', '2025-09-20 00:49:41.938434'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-09-20 00:49:41.952788'),
(18, 'facturacion', '0001_initial', '2025-09-20 00:49:42.138944'),
(19, 'facturacion', '0002_venta_detalleventa', '2025-09-20 00:49:42.469175'),
(20, 'facturacion', '0003_movimientostock', '2025-09-20 00:49:42.599553'),
(21, 'facturacion', '0004_entradaproducto_es_producto_base', '2025-09-20 00:49:42.615978'),
(22, 'facturacion', '0005_cuentaporcobrar_pagocuentaporcobrar', '2025-09-20 00:49:42.853946'),
(23, 'facturacion', '0006_cuentaporcobrar_productos', '2025-09-20 00:49:42.870547'),
(24, 'facturacion', '0007_cierrecaja', '2025-09-20 00:49:42.946455'),
(25, 'facturacion', '0008_venta_cuota_mensual_venta_es_financiada_and_more', '2025-09-20 00:49:43.073194'),
(26, 'facturacion', '0009_venta_montoinicial', '2025-09-20 00:49:43.093528'),
(27, 'facturacion', '0010_venta_fecha_anulacion_venta_motivo_anulacion_and_more', '2025-09-20 00:49:43.197711'),
(28, 'facturacion', '0011_devolucion', '2025-09-20 00:49:43.345389'),
(29, 'facturacion', '0012_venta_total_a_pagar', '2025-09-20 00:49:43.365339'),
(30, 'facturacion', '0013_cuentaporcobrar_anulada_and_more', '2025-09-20 00:49:43.429498'),
(31, 'facturacion', '0014_alter_cuentaporcobrar_monto_total_con_interes', '2025-09-20 00:49:43.473447'),
(32, 'facturacion', '0015_comprobantepago', '2025-09-20 00:49:43.736039'),
(33, 'sessions', '0001_initial', '2025-09-20 00:49:43.776846');

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
('h8oopt6dhlr16tf2ozn8nacwwumlntap', '.eJxVjDsOwyAQBe9CHSHA5pcyvc-All0ITiKQjF1FuXuE5CJp38y8Nwtw7CUcPW1hJXZlkl1-twj4THUAekC9N46t7tsa-VD4STtfGqXX7XT_Dgr0MmqJagJEnyMSYXRIGoU0aMFlpYV0BHaaUiayRs_WaaNBeMwIYvbKs88XHvI4wg:1v02fW:TMCMe0I25EpRk5ZLSUVAaGnr7Dh0v9HF5QSCOKRhOQQ', '2025-10-04 18:50:46.659196');

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
(1, 'PROD-294342', '004886', '2025-09-20', '000000000', 'TAURO FTZ 150', 'tauro', 'FTZ150', '10', 'TARVJKKA8SM004306', 'nuevo', 'azul', 0, 2, 86000.00, 18.00, 15480.00, 101480.00, 98000.00, -3.43, 1, 'COMPRADO EN MOTO NEGOCIADO MICHAEL S.R.L', '2025-09-20 01:40:29.392301', '2025-09-20 21:59:58.522646', 1, 0);

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
(1, 'MOTO NEGOCIANDO MICHAEL S.R.L', '130-41628-1', 'MICHAEL', 'MICHEL@GMAIL.COM', '(809) 585-1442', '(809) 258-3440', 'DO', 'NAVARRETE SANTIAGO', 'smartphones', 'AV.DUAETE PROXIMO A LA BOMBA SHELL  NAVARRETE SANTIAGO', 'contado', 6000000.00, 'MI AMIGO', 1, '2025-09-20 01:12:43.485435', '2025-09-20 01:12:43.485467');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `li`
--

CREATE TABLE `li` (
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, '2025-09-20 01:50:33.528416', 'ajuste', 1, 1, 0, 'Ajuste manual de stock', NULL, 1, NULL),
(2, '2025-09-20 19:35:41.988412', 'ajuste', 1, 0, 1, 'Ajuste manual de stock', NULL, 1, NULL),
(3, '2025-09-20 19:35:41.993806', 'ajuste', 1, 0, 1, 'Ajuste manual desde sistema de reabastecimiento', NULL, 1, 1),
(4, '2025-09-20 19:39:05.498305', 'ajuste', 1, 1, 0, 'Ajuste manual de stock', NULL, 1, NULL),
(5, '2025-09-20 19:54:23.070347', 'ajuste', 1, 0, 1, 'Ajuste manual de stock', NULL, 1, NULL),
(6, '2025-09-20 19:54:23.077470', 'ajuste', 1, 0, 1, 'Ajuste manual desde sistema de reabastecimiento', NULL, 1, 1),
(7, '2025-09-20 19:54:24.710870', 'ajuste', 1, 1, 2, 'Ajuste manual de stock', NULL, 1, NULL),
(8, '2025-09-20 19:54:24.717346', 'ajuste', 1, 1, 2, 'Ajuste manual desde sistema de reabastecimiento', NULL, 1, 1),
(9, '2025-09-20 19:56:01.844818', 'ajuste', 1, 2, 1, 'Ajuste manual de stock', NULL, 1, NULL),
(10, '2025-09-20 20:13:52.476616', 'ajuste', 1, 1, 0, 'Ajuste manual de stock', NULL, 1, NULL);

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
(1, 'F-2025-000001', '2025-09-20 01:50:33.514433', 'YONERY PEREZ ROMAN', '101-0010551-8', 'credito', 'efectivo', 98000.00, 0.00, 0.00, 62540.00, 0.00, 0.00, 1, 0, '2025-09-20 01:50:33.519407', '2025-09-20 01:50:33.519417', 1, 1, 10423.33, 1, 9540.00, 53000.00, 6, 3.00, 62540.00, 45000.00, NULL, NULL, NULL, 107540.00),
(2, 'F-2025-000002', '2025-09-20 19:39:05.479414', 'jose miguel', '998-3993898-3', 'credito', 'efectivo', 98000.00, 0.00, 0.00, 62540.00, 0.00, 0.00, 1, 0, '2025-09-20 19:39:05.484717', '2025-09-20 19:39:05.484782', 2, 1, 10423.33, 1, 9540.00, 53000.00, 6, 3.00, 62540.00, 45000.00, NULL, NULL, NULL, 107540.00),
(3, 'F-2025-000003', '2025-09-20 19:56:01.827433', 'jose miguel', '998-3993898-3', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-20 19:56:01.830591', '2025-09-20 19:56:01.830623', 2, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00),
(4, 'F-2025-000004', '2025-09-20 20:13:52.468046', 'jose miguel', '998-3993898-3', 'credito', 'efectivo', 50000.00, 0.00, 0.00, 54400.00, 0.00, 0.00, 1, 0, '2025-09-20 20:13:52.469650', '2025-09-20 20:13:52.469662', 2, 1, 4533.33, 1, 14400.00, 40000.00, 12, 3.00, 54400.00, 10000.00, NULL, NULL, NULL, 64400.00);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `caja`
--
ALTER TABLE `caja`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cierre_caja`
--
ALTER TABLE `cierre_caja`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `comprobantes_pago`
--
ALTER TABLE `comprobantes_pago`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cuentas_por_cobrar`
--
ALTER TABLE `cuentas_por_cobrar`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `facturacion_proveedor`
--
ALTER TABLE `facturacion_proveedor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `movimientos_stock`
--
ALTER TABLE `movimientos_stock`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `pagos_cuentas_por_cobrar`
--
ALTER TABLE `pagos_cuentas_por_cobrar`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
