![Logotipo de la aplicación](img-doc/derejmotium.png)

# Documentación Técnica del Sistema de Facturación y Gestión

---

## 1. Introducción

El proyecto **DerejMotiun** es una plataforma integral para la operación diaria de una casa comercial de motocicletas y dispositivos móviles. Centraliza la gestión de inventario, ciclo de ventas, control de caja, créditos, cobranzas, devoluciones y generación de comprobantes. Está construido sobre **Django 5.2** con un backend basado en **MySQL** y una única app denominada `facturacion`, que concentra modelos, vistas, plantillas y recursos estáticos propios del negocio.

---

## 2. Tecnologías y dependencias clave

- **Django 5.2** para el framework web y ORM.
- **MySQL** como motor relacional principal (configurado mediante variables de entorno en [settings.py](sytem_phone/sytem_phone/settings.py)).
- **ReportLab** para la emisión de comprobantes PDF y otros reportes impresos.
- **Pandas** para cálculos agregados del dashboard.
- **WhiteNoise** para servir archivos estáticos en despliegues productivos.
- **python-dotenv** (`load_dotenv`) para inyectar secretos y credenciales sin exponerlos en el repositorio.

---

## 3. Arquitectura general

- **App única (`facturacion`)**: concentra los modelos de dominio, vistas basadas en funciones y rutas declaradas en [urls.py](sytem_phone/facturacion/urls.py).
- **Plantillas HTML** bajo [`templates/facturacion`](sytem_phone/facturacion/templates/facturacion/), organizadas por vistas (ventas, dashboard, entradas, cuentas por cobrar, etc.).
- **Templatetags personalizados** en [custom_filters.py](sytem_phone/facturacion/templatetags/custom_filters.py) para formatear montos y números con el estilo contable local.
- **Recursos estáticos** ubicados en [static](sytem_phone/facturacion/static/) y recolectados en [staticfiles](sytem_phone/facturacion/staticfiles/) para despliegue.
- **Configuración central** en [settings.py](sytem_phone/sytem_phone/settings.py), donde se habilitan middlewares, almacenamiento de estáticos y parámetros regionales (`LANGUAGE_CODE='es-do'`, `TIME_ZONE='America/Santo_Domingo'`).
- **Seguridad**: autenticación estándar de Django, decoradores `login_required` y un decorador custom `superuser_required` para operaciones sensibles (por ejemplo edición o eliminación de inventario).

## Estructura de Carpetas

```
sytem_phone/
│   manage.py
│   requirements.txt
│
├── facturacion/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── facturacion/
│   │       ├── facturacion.html
│   │       ├── dashboard.html
│   │       ├── entrada.html
│   │       ├── cuentaporcobrar.html
│   │       ├── cuentasAtrasada.html
│   │       ├── cierredecaja.html
│   │       ├── devoluciones.html
│   │       ├── comprobante_venta.html
│   │       ├── cuadre.html
│   │       ├── ventas.html
│   │       ├── listadecliente.html
│   │       ├── registrodecliente.html
│   │       ├── roles.html
│   │       ├── anular.html
│   │       ├── imprimir_termica.html
│   │       ├── ticket_chef.html
│   │       ├── salida.html
│   │       ├── historial_pedidos.html
│   ├── migrations/
│   ├── templatetags/
│   ├── tests.py
│   ├── admin.py
│   ├── apps.py
│
├── sytem_phone/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│
├── staticfiles/
│   └── image/
├── img-doc/
│   └── derejmotium.png
├── null/
│   ├── agregarroles.html
│   ├── agregarsucursales.html
│   ├── facturacion.html
│   ├── gestioncaja.html
│   ├── inicio-caja.html
│   ├── inv.html
│   ├── login-espacio.html
│   ├── login-nieve.html
│   ├── prue.html
│   ├── settings.json
│   ├── sucursales.html
│   ├── usuario.html
│   └── ventas.html
```

---

## 4. Modelo de datos principal

Los modelos residen en [models.py](sytem_phone/facturacion/models.py) y cubren todo el ciclo operativo.

| Modelo                | Rol principal                                                                                                  | Relacionamientos destacados                                                           |
| --------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `Proveedor`           | Catálogo de suplidores con datos de contacto, país y términos de pago.                                         | Consumido por `EntradaProducto`.                                                      |
| `EntradaProducto`     | Inventario granular (IMEI, marca, color, estado, costos, margen). Calcula ITBIS y margen automáticamente.      | FK a `Proveedor`; enlazado con `DetalleVenta`, `MovimientoStock` y `Devolucion`.      |
| `Cliente`             | Registro de clientes con límite de crédito y datos de contacto.                                                | Asociado a `Venta`, `CuentaPorCobrar` y `ComprobantePago`.                            |
| `Venta`               | Encapsula cada transacción de venta, soportando contado, crédito y financiamiento (tasa, plazo, cuota, total). | Relación 1:N con `DetalleVenta`; 1:1 con `CuentaPorCobrar` en créditos.               |
| `DetalleVenta`        | Desglose de productos vendidos, cantidades y precios unitarios.                                                | FK a `Venta` y `EntradaProducto`.                                                     |
| `CuentaPorCobrar`     | Control de créditos, con estados y cálculo de saldo. Incluye soporte de rebajas y soft delete.                 | 1:1 con `Venta`, N:1 con `Cliente`; asociado a `PagoCuentaPorCobrar` y `RebajaDeuda`. |
| `PagoCuentaPorCobrar` | Registro de abonos (efectivo, tarjeta, transferencia) y observaciones.                                         | FK a `CuentaPorCobrar` y `ComprobantePago`.                                           |
| `RebajaDeuda`         | Bitácora de ajustes manuales al saldo de una cuenta.                                                           | FK a `CuentaPorCobrar` y `User`.                                                      |
| `Caja` y `CierreCaja` | Control de apertura/cierre de caja, con montos iniciales y discrepancias.                                      | Vinculados a usuarios.                                                                |
| `MovimientoStock`     | Auditoría de entradas, salidas, devoluciones y ajustes.                                                        | FK a `EntradaProducto` y `User`.                                                      |
| `Devolucion`          | Registra devoluciones vinculadas a una `Venta` y reinstala stock si aplica.                                    | FK a `EntradaProducto`.                                                               |
| `ComprobantePago`     | Emite comprobantes numerados para pagos o descuentos.                                                          | 1:1 con `PagoCuentaPorCobrar`.                                                        |

---

## 5. Módulos funcionales

### 5.1 Autenticación y roles

- Vista `index` maneja login utilizando `django.contrib.auth`. Redirige a `iniciocaja` tras autenticarse.
- Decoradores `login_required` protegen todas las vistas operativas. `superuser_required` restringe endpoints críticos.
- Vista `roles` y plantillas asociadas permiten administrar permisos básicos.

### 5.2 Dashboard y analítica

- Métricas diarias/mensuales, ventas contado, créditos, acumulados mensuales, evolución semanal, inventario disponible, productos con stock bajo, cuentas vencidas, top productos y últimas ventas.

### 5.3 Gestión de inventario

- Catálogo editable vía AJAX, control de stock, generación de códigos únicos y trazabilidad.
- `EntradaProducto.save()` genera códigos únicos, calcula ITBIS, costo total y margen. Cada variación de cantidad dispara `MovimientoStock`.

### 5.4 Clientes

- Registro, gestión y validación de crédito. Endpoints REST para integraciones.

### 5.5 Ventas y caja

- Formulario de ventas, validación de totales, descuentos, tipos de venta y facturación.
- Cada `DetalleVenta` descuenta stock y registra movimientos. El view final retorna respuesta JSON con desglose de totales.
- Cierre de caja, arqueos diarios y consolidación de datos.

### 5.6 Cuentas por cobrar y pagos

- Cartera con filtros por estado, vencimiento y cliente.
- Registro de pagos, generación de comprobantes, aplicación de descuentos y rebajas.

### 5.7 Devoluciones y anulaciones

- Control de devoluciones, restauración de stock y trazabilidad.
- Anulación de ventas y comprobantes.

### 5.8 Reporting y utilitarios

- Reportes PDF, exportaciones CSV, consultas tipo POS.

### 5.9 Organización de views.py

- Bloques temáticos: autenticación, dashboard, inventario, clientes, ventas, caja, cuentas por cobrar, devoluciones, utilitarios.

---

## 6. Flujo operativo end-to-end

1. Ingreso de mercancía y registro de productos.
2. Habilitación de caja por usuario.
3. Venta: selección de cliente, validación de stock, configuración de pago, creación de venta y actualización de dashboard.
4. Créditos: creación de cuenta por cobrar, registro de pagos y rebajas.
5. Devoluciones/anulaciones: reversión de ventas o productos, restauración de inventario.
6. Cierre: consolidación de datos y arqueos diarios.

---

## 7. Integraciones internas y archivos relevantes

- Rutas centralizadas en [urls.py](sytem_phone/facturacion/urls.py).
- Plantillas por funcionalidad en [templates/facturacion](sytem_phone/facturacion/templates/facturacion/).
- Assets en [facturacion/static/](sytem_phone/facturacion/static/) y compilados en [staticfiles/](sytem_phone/facturacion/staticfiles/).

---

## 8. Seguridad y cumplimiento

- Variables de entorno en `.env` (no versionado).
- CSRF habilitado globalmente; uso de `@csrf_exempt` solo cuando es imprescindible.
- Validaciones server-side para montos, stock y crédito.
- Soft delete en modelos críticos.

---

## 9. Despliegue y configuración

1. **Requisitos:**
   - Python 3.10+
   - Django 5.2
   - MySQL
   - Paquetes adicionales: `mysqlclient`, `pillow`, `reportlab`, `asgiref`, `sqlparse`, `tzdata`, `charset-normalizer`, `pandas`.

2. **Instalación de dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de base de datos:**
   - Edita las variables de entorno en `.env` para definir `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
   - El sistema utiliza MySQL con configuración estricta y soporte para zona horaria.

4. **Migraciones:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Creación de superusuario:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecución del servidor:**
   ```bash
   python manage.py runserver
   ```

---

## 10. Métricas y mejoras futuras sugeridas

- **KPI adicionales**: rotación de inventario, margen por marca, aging de cuentas.
- **Alertas proactivas**: notificaciones por correo o WhatsApp para cuentas vencidas o stock crítico.
- **API pública**: encapsular endpoints clave en una API REST (Django REST Framework) para integraciones externas.
- **Pruebas automatizadas**: ampliar [tests.py](sytem_phone/facturacion/tests.py) con casos de venta, rebaja de deuda y devoluciones.

---

## Modelos Clave

- **Proveedor:** Catálogo de suplidores con datos de contacto, país y términos de pago.
- **EntradaProducto:** Inventario granular (IMEI, marca, color, estado, costos, margen).
- **Cliente:** Registro de clientes con límite de crédito y datos de contacto.
- **Venta:** Encapsula cada transacción de venta, soportando contado, crédito y financiamiento.
- **DetalleVenta:** Desglose de productos vendidos, cantidades y precios unitarios.
- **CuentaPorCobrar:** Control de créditos, estados y cálculo de saldo.
- **PagoCuentaPorCobrar:** Registro de abonos y observaciones.
- **RebajaDeuda:** Bitácora de ajustes manuales al saldo de una cuenta.
- **Caja y CierreCaja:** Control de apertura/cierre de caja.
- **MovimientoStock:** Auditoría de entradas, salidas, devoluciones y ajustes.
- **Devolucion:** Registra devoluciones vinculadas a una venta.
- **ComprobantePago:** Emite comprobantes numerados para pagos o descuentos.

## Templates

La aplicación cuenta con templates personalizados para cada funcionalidad, con diseño moderno y sidebar fijo. Ejemplos:

- `facturacion.html`: Panel de facturación.
- `dashboard.html`: Dashboard de métricas.
- `entrada.html`: Registro de entradas de productos.
- `cuentaporcobrar.html`: Gestión de cuentas por cobrar.
- `cuentasAtrasada.html`: Reporte de cuentas vencidas.
- `cierredecaja.html`: Cierre de caja.
- `devoluciones.html`: Devoluciones y anulaciones.
- `comprobante_venta.html`: Comprobante de venta.
- `cuadre.html`: Arqueo de caja.
- `ventas.html`: Visualización de ventas.
- `listadecliente.html`: Listado de clientes.
- `registrodecliente.html`: Registro de clientes.
- `roles.html`: Gestión de usuarios y permisos.
- `anular.html`: Anulación de ventas.
- `imprimir_termica.html`: Factura para impresión térmica.
- `ticket_chef.html`: Ticket para cocina.
- `salida.html`: Registro de salidas de productos.
- `historial_pedidos.html`: Historial de pedidos pagados.

---

## Instalación

1. **Requisitos:**
   - Python 3.10+
   - Django 5.2
   - MySQL
   - Paquetes adicionales: `mysqlclient`, `pillow`, `reportlab`, `asgiref`, `sqlparse`, `tzdata`, `charset-normalizer`, `pandas`.

2. **Instalación de dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de base de datos:**
   - Edita las variables de entorno en `.env` para definir `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
   - El sistema utiliza MySQL con configuración estricta y soporte para zona horaria.

4. **Migraciones:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Creación de superusuario:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecución del servidor:**
   ```bash
   python manage.py runserver
   ```

---

## Uso

- Accede al sistema desde el navegador en `http://localhost:8000`.
- Inicia sesión con usuario registrado.
- Utiliza el dashboard para visualizar métricas.
- Gestiona inventario, ventas, facturación, devoluciones y clientes desde el menú lateral.
- Imprime facturas y tickets desde las vistas correspondientes.

---

## Seguridad y Roles

- El sistema implementa autenticación y autorización basada en usuarios, grupos y permisos de Django.
- Los roles permiten segmentar el acceso a funcionalidades críticas.

---

## Pruebas

- El archivo `tests.py` está preparado para pruebas unitarias con Django TestCase.
- Se recomienda implementar pruebas para cada modelo y vista crítica.

---

## Personalización

- Los templates pueden ser adaptados para branding propio.
- El sistema soporta ampliación de modelos y vistas para nuevas funcionalidades.

---

## Dependencias

Ver archivo [Requirements.txt](sytem_phone/requirements.txt) para la lista completa.

---

## Configuración

- Variables de entorno para seguridad y base de datos.
- Soporte para archivos estáticos y media.
- Configuración de zona horaria: `America/Santo_Domingo`.

---

## Contacto y Soporte

Para soporte, contactar al desarrollador o consultar la documentación de Django.

---

## Ejemplo de creación de archivo .env

```bash
SECRET_KEY="tu_clave_secreta"
DB_NAME="nombre_base_datos"
DB_USER="usuario"
DB_PASSWORD="contraseña"
DB_HOST="localhost"
DB_PORT="3306"
ALLOWED_HOSTS="localhost,127.0.0.1"
CSRF_TRUSTED_ORIGINS="http://localhost,http://127.0.0.1"
DEBUG=True
```
