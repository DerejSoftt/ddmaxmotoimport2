"""
SCRIPT: migrar_movimientos_financieros.py
==========================================
Migra datos históricos a la tabla MovimientoFinanciero desde:
  1. Ventas (contado)         → INGRESO / VENTA
  2. Ventas (crédito)         → INGRESO / VENTA  (monto inicial pagado)
  3. PagoCuentaPorCobrar      → INGRESO / PAGO_CXC
  4. Devoluciones             → EGRESO  / DEVOLUCION
  5. Ventas anuladas          → INGRESO / VENTA estado=REVERTIDO

USO:
  1. Ajusta DJANGO_SETTINGS_MODULE abajo según tu proyecto.
  2. Corre primero con DRY_RUN = True para revisar el resumen.
  3. Cuando todo se vea bien, cambia a DRY_RUN = False.

  python migrar_movimientos_financieros.py
"""

import os
import django

# ─── CONFIGURA AQUÍ ────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sytem_phone.settings')  # ← cambia si es necesario
django.setup()
# ───────────────────────────────────────────────────────────────────────────────

from decimal import Decimal
from django.db import transaction

from facturacion.models import (   # ← cambia 'facturacion' por el nombre real de tu app
    Venta,
    PagoCuentaPorCobrar,
    Devolucion,
    MovimientoFinanciero,
)

# ─── MODO ──────────────────────────────────────────────────────────────────────
DRY_RUN = False   # ← True = simulación sin escritura | False = escritura real
# ───────────────────────────────────────────────────────────────────────────────

# Contadores globales
stats = {
    'ventas_contado':      0,
    'ventas_credito':      0,
    'ventas_anuladas':     0,
    'pagos_cxc':           0,
    'devoluciones':        0,
    'ya_existian':         0,
    'omitidas':            0,
    'errores':             [],
}


def log(tipo, origen, monto, referencia, estado='ACTIVO', extra=''):
    print(
        f"  [{'SIM' if DRY_RUN else 'OK '}] "
        f"{tipo:7} | {origen:10} | RD${monto:>12,.2f} | {referencia:<20} | {estado} {extra}"
    )


# ==============================================================================
# 1. VENTAS
# ==============================================================================
def migrar_ventas():
    print("\n" + "─" * 70)
    print("SECCIÓN 1 — VENTAS")
    print("─" * 70)

    ventas = (
        Venta.objects
        .select_related('cliente')
        .prefetch_related('movimientos_financieros')
        .order_by('fecha_venta')
    )

    for venta in ventas:
        # Saltar si ya tiene movimiento VENTA para evitar duplicados
        ya_tiene = venta.movimientos_financieros.filter(origen='VENTA').exists()
        if ya_tiene:
            stats['ya_existian'] += 1
            continue

        # Venta anulada
        if venta.anulada:
            # Solo generamos movimiento si el total es > 0
            if venta.total <= 0:
                stats['omitidas'] += 1
                continue

            datos = dict(
                tipo='INGRESO',
                origen='VENTA',
                estado='REVERTIDO',
                monto=venta.total,
                fecha_operacion=venta.fecha_venta,
                factura=venta,
                cliente=venta.cliente,
                metodo_pago=venta.metodo_pago,
                creado_por=None,
                descripcion=f"[MIGRADO] Venta {venta.numero_factura} (anulada)",
                referencia=f"MIGRADO-{venta.numero_factura}",
            )
            if DRY_RUN:
                log('INGRESO', 'VENTA', venta.total, venta.numero_factura, 'REVERTIDO', '← anulada')
            else:
                try:
                    with transaction.atomic():
                        MovimientoFinanciero.objects.create(**datos)
                    stats['ventas_anuladas'] += 1
                except Exception as e:
                    stats['errores'].append(f"Venta anulada {venta.numero_factura}: {e}")
                    continue
            stats['ventas_anuladas'] += 1
            continue

        # Venta de contado — monto completo al momento de la venta
        if venta.tipo_venta == 'contado':
            datos = dict(
                tipo='INGRESO',
                origen='VENTA',
                estado='ACTIVO',
                monto=venta.total,
                fecha_operacion=venta.fecha_venta,
                factura=venta,
                cliente=venta.cliente,
                metodo_pago=venta.metodo_pago,
                creado_por=None,
                descripcion=f"[MIGRADO] Venta contado {venta.numero_factura}",
                referencia=f"MIGRADO-{venta.numero_factura}",
            )
            if DRY_RUN:
                log('INGRESO', 'VENTA', venta.total, venta.numero_factura)
            else:
                try:
                    with transaction.atomic():
                        MovimientoFinanciero.objects.create(**datos)
                    stats['ventas_contado'] += 1
                except Exception as e:
                    stats['errores'].append(f"Venta contado {venta.numero_factura}: {e}")
                    continue
            stats['ventas_contado'] += 1

        # Venta de crédito — solo registramos el monto inicial (inicial pagado en el acto)
        elif venta.tipo_venta == 'credito':
            monto_inicial = venta.montoinicial or Decimal('0')

            # Solo creamos movimiento si efectivamente se recibió un pago inicial
            if monto_inicial > 0:
                datos = dict(
                    tipo='INGRESO',
                    origen='VENTA',
                    estado='ACTIVO',
                    monto=monto_inicial,
                    fecha_operacion=venta.fecha_venta,
                    factura=venta,
                    cliente=venta.cliente,
                    metodo_pago=venta.metodo_pago,
                    creado_por=None,
                    descripcion=f"[MIGRADO] Inicial crédito {venta.numero_factura}",
                    referencia=f"MIGRADO-{venta.numero_factura}",
                )
                if DRY_RUN:
                    log('INGRESO', 'VENTA', monto_inicial, venta.numero_factura,
                        extra=f'← crédito (inicial de RD${venta.total:,.2f})')
                else:
                    try:
                        with transaction.atomic():
                            MovimientoFinanciero.objects.create(**datos)
                        stats['ventas_credito'] += 1
                    except Exception as e:
                        stats['errores'].append(f"Venta crédito {venta.numero_factura}: {e}")
                        continue
                stats['ventas_credito'] += 1
            else:
                # Crédito sin inicial — aún así registramos la venta con monto=0
                # para mantener trazabilidad del documento
                datos = dict(
                    tipo='INGRESO',
                    origen='VENTA',
                    estado='ACTIVO',
                    monto=Decimal('0.00'),
                    fecha_operacion=venta.fecha_venta,
                    factura=venta,
                    cliente=venta.cliente,
                    metodo_pago=venta.metodo_pago,
                    creado_por=None,
                    descripcion=f"[MIGRADO] Venta crédito sin inicial {venta.numero_factura}",
                    referencia=f"MIGRADO-{venta.numero_factura}",
                )
                if DRY_RUN:
                    log('INGRESO', 'VENTA', Decimal('0'), venta.numero_factura,
                        extra='← crédito SIN inicial')
                else:
                    try:
                        with transaction.atomic():
                            MovimientoFinanciero.objects.create(**datos)
                        stats['ventas_credito'] += 1
                    except Exception as e:
                        stats['errores'].append(f"Venta crédito sin inicial {venta.numero_factura}: {e}")
                        continue
                stats['ventas_credito'] += 1


# ==============================================================================
# 2. PAGOS DE CUENTAS POR COBRAR
# ==============================================================================
def migrar_pagos_cxc():
    print("\n" + "─" * 70)
    print("SECCIÓN 2 — PAGOS DE CUENTAS POR COBRAR")
    print("─" * 70)

    pagos = (
        PagoCuentaPorCobrar.objects
        .select_related('cuenta__venta', 'cuenta__cliente')
        .prefetch_related('movimientos_financieros')
        .order_by('fecha_pago')
    )

    for pago in pagos:
        # Saltar si ya tiene movimiento PAGO_CXC
        ya_tiene = pago.movimientos_financieros.filter(origen='PAGO_CXC').exists()
        if ya_tiene:
            stats['ya_existian'] += 1
            continue

        # Pago anulado — se migra como REVERTIDO para mantener historial
        estado_mov = 'REVERTIDO' if pago.anulado else 'ACTIVO'

        venta = pago.cuenta.venta if pago.cuenta else None
        cliente = pago.cuenta.cliente if pago.cuenta else None
        ref = venta.numero_factura if venta else f"PAGO-{pago.id}"

        datos = dict(
            tipo='INGRESO',
            origen='PAGO_CXC',
            estado=estado_mov,
            monto=pago.monto,
            fecha_operacion=pago.fecha_pago,
            factura=venta,
            pago_cxc=pago,
            cliente=cliente,
            metodo_pago=pago.metodo_pago,
            creado_por=None,
            descripcion=f"[MIGRADO] Pago CxC #{pago.id} — {ref}"
                        + (" (anulado)" if pago.anulado else ""),
            referencia=f"MIGRADO-PAGO-{pago.id}",
        )

        if DRY_RUN:
            log('INGRESO', 'PAGO_CXC', pago.monto, ref, estado_mov,
                '← anulado' if pago.anulado else '')
        else:
            try:
                with transaction.atomic():
                    MovimientoFinanciero.objects.create(**datos)
                stats['pagos_cxc'] += 1
            except Exception as e:
                stats['errores'].append(f"Pago CxC #{pago.id}: {e}")
                continue
        stats['pagos_cxc'] += 1


# ==============================================================================
# 3. DEVOLUCIONES
# ==============================================================================
def migrar_devoluciones():
    print("\n" + "─" * 70)
    print("SECCIÓN 3 — DEVOLUCIONES")
    print("─" * 70)

    devoluciones = (
        Devolucion.objects
        .select_related('venta', 'venta__cliente', 'producto')
        .prefetch_related('movimientos_financieros')
        .order_by('fecha_devolucion')
    )

    for dev in devoluciones:
        # Saltar si ya tiene movimiento DEVOLUCION
        ya_tiene = dev.movimientos_financieros.filter(origen='DEVOLUCION').exists()
        if ya_tiene:
            stats['ya_existian'] += 1
            continue

        # Calcular monto devuelto: cantidad × precio unitario del DetalleVenta
        try:
            detalle = dev.venta.detalles.get(producto=dev.producto)
            monto_devuelto = detalle.precio_unitario * dev.cantidad
        except Exception:
            # Si no se encuentra el detalle, usar costo_venta del producto
            monto_devuelto = dev.producto.costo_venta * dev.cantidad

        if monto_devuelto <= 0:
            stats['omitidas'] += 1
            if DRY_RUN:
                print(f"  [SKIP] DEVOLUCION #{dev.id} — monto=0, se omite")
            continue

        datos = dict(
            tipo='EGRESO',
            origen='DEVOLUCION',
            estado='ACTIVO',
            monto=monto_devuelto,
            fecha_operacion=dev.fecha_devolucion,
            factura=dev.venta,
            devolucion=dev,
            cliente=dev.venta.cliente,
            metodo_pago=dev.venta.metodo_pago,
            creado_por=None,
            descripcion=(
                f"[MIGRADO] Devolución #{dev.id} — "
                f"{dev.cantidad}x {dev.producto.nombre_producto} — "
                f"Venta {dev.venta.numero_factura}"
            ),
            referencia=f"MIGRADO-DEV-{dev.id}",
        )

        if DRY_RUN:
            log('EGRESO', 'DEVOLUCION', monto_devuelto, dev.venta.numero_factura,
                extra=f'← {dev.cantidad}x {dev.producto.nombre_producto}')
        else:
            try:
                with transaction.atomic():
                    MovimientoFinanciero.objects.create(**datos)
                stats['devoluciones'] += 1
            except Exception as e:
                stats['errores'].append(f"Devolucion #{dev.id}: {e}")
                continue
        stats['devoluciones'] += 1


# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print(f"  MIGRACIÓN — MovimientoFinanciero")
    print(f"  MODO: {'⚙️  SIMULACIÓN (DRY RUN)' if DRY_RUN else '⚠️  ESCRITURA REAL'}")
    print("=" * 70)

    migrar_ventas()
    migrar_pagos_cxc()
    migrar_devoluciones()

    total_creados = (
        stats['ventas_contado'] +
        stats['ventas_credito'] +
        stats['ventas_anuladas'] +
        stats['pagos_cxc'] +
        stats['devoluciones']
    )

    print("\n" + "=" * 70)
    print("  RESUMEN FINAL")
    print("=" * 70)
    accion = "a crear" if DRY_RUN else "creados"
    print(f"  Movimientos {accion}:")
    print(f"    Ventas contado          : {stats['ventas_contado']}")
    print(f"    Ventas crédito (inicial): {stats['ventas_credito']}")
    print(f"    Ventas anuladas         : {stats['ventas_anuladas']}")
    print(f"    Pagos CxC               : {stats['pagos_cxc']}")
    print(f"    Devoluciones            : {stats['devoluciones']}")
    print(f"    ─────────────────────────────")
    print(f"    TOTAL                   : {total_creados}")
    print(f"  Ya existían (saltados)    : {stats['ya_existian']}")
    print(f"  Omitidos (monto=0/vacíos) : {stats['omitidas']}")
    print(f"  Errores                   : {len(stats['errores'])}")
    if stats['errores']:
        print("\n  DETALLE DE ERRORES:")
        for e in stats['errores']:
            print(f"    ❌ {e}")
    print("=" * 70 + "\n")


    #python migrar_movimientos.py  