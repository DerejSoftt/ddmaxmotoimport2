![Logotipo de la aplicación](../facturacion/static/image/logo.png)

# Documentacion Técnica del Sistema de Facturación y Gestión

## 1. Introducción

El proyecto **sytem_phone** es una plataforma integral para la operación diaria de una casa comercial de motocicletas y dispositivos móviles. La aplicación centraliza la gestión de inventario, ciclo de ventas, control de caja, créditos, cobranzas, devoluciones y generación de comprobantes. Está construida sobre **Django 5.2** con un backend basado en **MySQL** y una única app denominada `facturacion`, que concentra modelos, vistas, plantillas y recursos estáticos propios del negocio.

## 2. Tecnologías y dependencias clave

- **Django 5.2** para el framework web y ORM.
- **MySQL** como motor relacional principal (configurado mediante variables de entorno en `sytem_phone/settings.py`).
- **ReportLab** para la emisión de comprobantes PDF y otros reportes impresos.
- **Pandas** y funciones personalizadas para cálculos agregados del dashboard.
- **WhiteNoise** para servir archivos estáticos en despliegues productivos.
- **python-dotenv** (`load_dotenv`) para inyectar secretos y credenciales sin exponerlos en el repositorio.

## 3. Arquitectura general

- **App única (`facturacion`)**: concentra los modelos de dominio, vistas basadas en funciones y rutas declaradas en `facturacion/urls.py`.
- **Plantillas HTML** bajo `facturacion/templates/facturacion/`, organizadas por vistas (ventas, dashboard, entradas, cuentas por cobrar, etc.).
- **Recursos estáticos** ubicados en `facturacion/static/` y recolectados en `staticfiles/` para despliegue.
- **Configuración central** en `sytem_phone/settings.py`, donde se habilitan middlewares, almacenamiento de estáticos y parámetros regionales (`LANGUAGE_CODE='es-do'`, `TIME_ZONE='America/Santo_Domingo'`).
- **Seguridad**: autenticación estándar de Django, decoradores `login_required` y un decorador custom `superuser_required` para operaciones sensibles (por ejemplo edición o eliminación de inventario).

## 4. Modelo de datos principal

Los modelos residen en [facturacion/models.py](facturacion/models.py) y cubren todo el ciclo operativo.

| Modelo                | Rol principal                                                                                                                                           | Relacionamientos destacados                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `Proveedor`           | Catálogo de suplidores con datos de contacto, país y términos de pago.                                                                                  | Consumido por `EntradaProducto`.                                                      |
| `EntradaProducto`     | Inventario granular (IMEI, marca, color, estado, costos, margen). Calcula ITBIS y margen automáticamente y registra movimientos de stock.               | FK a `Proveedor`; enlazado con `DetalleVenta`, `MovimientoStock` y `Devolucion`.      |
| `Cliente`             | Registro de clientes con límite de crédito y datos de contacto.                                                                                         | Asociado a `Venta`, `CuentaPorCobrar` y `ComprobantePago`.                            |
| `Venta`               | Encapsula cada transacción de venta, soportando contado, crédito y financiamiento (tasa, plazo, cuota, total con intereses).                            | Relación 1:N con `DetalleVenta`; 1:1 con `CuentaPorCobrar` en créditos.               |
| `DetalleVenta`        | Desglose de productos vendidos, cantidades y precios unitarios.                                                                                         | FK a `Venta` y `EntradaProducto`.                                                     |
| `CuentaPorCobrar`     | Control de créditos, con estados (`pendiente`, `parcial`, `pagada`, `vencida`, `anulada`) y cálculo de saldo. Incluye soporte de rebajas y soft delete. | 1:1 con `Venta`, N:1 con `Cliente`; asociado a `PagoCuentaPorCobrar` y `RebajaDeuda`. |
| `PagoCuentaPorCobrar` | Registro de abonos (efectivo, tarjeta, transferencia) y observaciones.                                                                                  | FK a `CuentaPorCobrar` y `ComprobantePago`.                                           |
| `RebajaDeuda`         | Bitácora de ajustes manuales al saldo de una cuenta.                                                                                                    | FK a `CuentaPorCobrar` y `User`.                                                      |
| `Caja` y `CierreCaja` | Control de apertura/cierre de caja, con montos iniciales y discrepancias.                                                                               | Vinculados a usuarios.                                                                |
| `MovimientoStock`     | Auditoría de entradas, salidas, devoluciones y ajustes.                                                                                                 | FK a `EntradaProducto` y `User`.                                                      |
| `Devolucion`          | Registra devoluciones vinculadas a una `Venta` y reinstala stock si aplica.                                                                             | FK a `EntradaProducto`.                                                               |
| `ComprobantePago`     | Emite comprobantes numerados (`CP-AAAA-######`) para pagos o descuentos.                                                                                | 1:1 con `PagoCuentaPorCobrar`.                                                        |

## 5. Módulos funcionales

### 5.1 Autenticación y roles

- Vista `index` maneja login utilizando `django.contrib.auth`. Redirige a `iniciocaja` tras autenticarse.
- Decoradores `login_required` protegen todas las vistas operativas. `superuser_required` restringe endpoints críticos (por ejemplo `inventario_editar` y `inventario_eliminar`).
- Vista `roles` y plantillas asociadas permiten administrar permisos básicos (frente a `User`, `Group`, `Permission`).

### 5.2 Dashboard y analítica

- `dashboard` y `dashboard_data` calculan métricas diarias/mensuales con ORM y consultas SQL directas para eficiencia.
- Indicadores: ventas contado, créditos (monto inicial + pagos), acumulados mensuales, evolución semanal, inventario disponible, productos con stock bajo, cuentas vencidas, top productos (últimos 30 días) y últimas ventas.
- `dashboard_data_tradicional` actúa como plan de contingencia en caso de error con pandas o consultas avanzadas.

### 5.3 Gestión de inventario

- Vista `inventario` (y `inventario_datos`) expone un catálogo editable vía AJAX con edición y eliminación protegida para superusuarios.
- `EntradaProducto.save()` genera códigos únicos (`PROD-XXXXXX`), calcula ITBIS, costo total y margen. Cada variación de cantidad dispara `MovimientoStock` para trazabilidad.
- Endpoints adicionales (`reavastecer`, `actualizar_stock`, `entrada`, `agregar_nuevo_producto`) soportan altas manuales y carga de plantillas.

### 5.4 Proveedores

- Formularios en `gestiondesuplidores` y `registrosuplidores`, respaldados por endpoints `agregar_proveedor`, `editar_proveedor`, `eliminar_proveedor` y `get_proveedor_data` para CRUD completo.

### 5.5 Clientes

- `listadecliente` y `registrodecliente` gestionan el ciclo de vida de clientes y validan límites de crédito.
- Endpoints REST (`guardar_cliente`, `obtener_clientes`, `editar_cliente`, `eliminar_cliente`) permiten integraciones front-end.

### 5.6 Ventas y caja

- `iniciocaja` abre sesiones de caja (`Caja`) para cada usuario, garantizando una sola caja abierta por operador.
- `ventas` carga formulario con clientes activos e inventario disponible.
- `procesar_venta` valida totales con funciones auxiliares (`safe_decimal`, `safe_int`), controla descuentos, soporta ventas financiadas (tasa mensual, cuota, total con interés) y crea `CuentaPorCobrar` automáticamente cuando aplica.
- Cada `DetalleVenta` descuenta stock y registra movimientos. El view final retorna respuesta JSON con desglose de totales para usar en el frontend.
- `cuadre`, `cierredecaja` y `procesar_cierre_caja` consolidan los datos para arqueos diarios.

### 5.7 Cuentas por cobrar y pagos

- `cuentaporcobrar` muestra cartera con filtros por estado, vencimiento y cliente.
- `detalle_cuenta` expone la ficha completa con historial de pagos.
- `registrar_pago` crea `PagoCuentaPorCobrar` y genera `ComprobantePago` numerado, con opción de anulación (`anular_comprobante_action`).
- `anular_cuenta`, `eliminar_cuenta_pagada` y `rebajar_deuda` gestionan casos especiales (anulaciones, descuentos, ajustes.
- `cuentasAtrasada` y `generar_pdf_deudas` ofrecen reportes puntuales de morosidad.

### 5.8 Devoluciones, anulaciones y comprobantes

- `devoluciones`, `buscar_factura_devolucion` y `procesar_devolucion` controlan devoluciones, reponiendo stock y marcando razones.
- `anular`, `buscar_factura`, `anular_factura` y `anular_factura_action` permiten revertir ventas, preservando bitácora (`motivo_anulacion`, `fecha_anulacion`, `usuario_anulacion`).
- `lista_comprobantes`, `generar_comprobante_pdf`, `buscar_comprobante`, `ultimo_comprobante` y `reimprimirfactura` cubren el ciclo de emisión y respaldo documental.

### 5.9 Reporting y utilitarios

- Reportes PDF: comprobantes, listados de cuentas vencidas y facturas reimpresas (basado en ReportLab).
- Exportaciones CSV desde funciones auxiliares en `views.py`.
- Consultas especiales (`buscar_productos`, `buscar_productos_similares`, `obtener_productos_disponibles`) facilitan experiencias tipo POS.

## 6. Flujo operativo end-to-end

1. **Ingreso de mercancía**: usuarios registran proveedores y entradas de productos, generando códigos únicos y movimientos de stock.
2. **Habilitación de caja**: cada vendedor abre su `Caja` con monto inicial.
3. **Venta**:
   - Selección de cliente (existente o nuevo).
   - Construcción de carrito con validación de stock en tiempo real.
   - Configuración de pago: contado, crédito simple o financiamiento con intereses.
   - Confirmación: se crea `Venta`, `DetalleVenta`, se descuenta stock y se actualiza el dashboard.
4. **Créditos**: si la venta es a crédito, se crea `CuentaPorCobrar` con saldo inicial y vencimiento; pagos iniciales se registran como `monto_pagado`.
5. **Cobranza**: abonos posteriores actualizan el saldo, emiten comprobantes y pueden descargarse como PDF.
6. **Devoluciones / anulaciones**: flujos dedicados revierten ventas o productos, restaurando inventario y dejando trazabilidad.
7. **Cierre**: al final del día el cajero registra montos reales, compara contra lo esperado y documenta diferencias en `CierreCaja`.

## 7. Integraciones internas y archivos relevantes

- **Rutas**: cubren todo el dominio y se centralizan en [facturacion/urls.py](facturacion/urls.py).
- **Plantillas**: cada feature tiene su HTML (por ejemplo `facturacion/templates/facturacion/ventas.html`, `dashboard.html`, `cuentaporcobrar.html`).
- **Assets**: imágenes y scripts en `facturacion/static/`; archivos compilados en `staticfiles/` listos para WhiteNoise.

## 8. Seguridad y cumplimiento

- Credenciales de base de datos y llaves se cargan desde `.env` (no versionado).
- CSRF está habilitado globalmente; endpoints AJAX críticos usan `@csrf_exempt` solo cuando es imprescindible y se compensan con `superuser_required`.
- Validaciones server-side para montos, descuento, stock y límites de crédito evitan inconsistencias contables.
- Soft delete en `CuentaPorCobrar` preserva histórico sin exponer datos sensibles en documentos.

## 9. Despliegue y configuración

1. Crear archivo `.env` con `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` y `DEBUG`.
2. Instalar dependencias (`pip install -r requirements.txt`).
3. Ejecutar migraciones (`python manage.py migrate`).
4. Crear superusuario (`python manage.py createsuperuser`).
5. Colectar estáticos (`python manage.py collectstatic`).
6. Configurar servicio WSGI (Gunicorn/uwsgi) apuntando a `sytem_phone.wsgi` y habilitar WhiteNoise para estáticos.

## 10. Métricas y mejoras futuras sugeridas

- **KPI adicionales**: rotación de inventario, margen por marca, aging de cuentas.<br>
- **Alertas proactivas**: notificaciones por correo o WhatsApp para cuentas vencidas o stock crítico.
- **API pública**: encapsular endpoints clave en una API REST (Django REST Framework) para integraciones externas.
- **Pruebas automatizadas**: ampliar `facturacion/tests.py` con casos de venta, rebaja de deuda y devoluciones.

Esta documentación resume la estructura actual del proyecto y sirve como base para incorporación de nuevos desarrolladores, auditorías internas y planificación de roadmap.
