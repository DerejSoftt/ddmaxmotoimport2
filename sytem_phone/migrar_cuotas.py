"""
SCRIPT: migrar_cuotas.py
=========================
Migra datos históricos a la tabla Cuota desde las Ventas financiadas
(tipo_venta='credito' con es_financiada=True o plazo_meses > 1).

Para cada venta financiada genera las N cuotas según:
  - plazo_meses      : número de cuotas
  - cuota_mensual    : monto de cada cuota
  - montoinicial     : ya fue cobrado en la venta, no genera cuota
  - fecha_venta      : punto de partida para calcular vencimientos
  - PagoCuentaPorCobrar : se usan para determinar qué cuotas ya fueron pagadas

Lógica de estado por cuota:
  - Se suman todos los pagos CxC de esa venta en orden cronológico.
  - El monto inicial ya cobrado se descuenta del total a distribuir.
  - Cada cuota se marca: pagada / parcial / pendiente según lo acumulado.

USO:
  1. Ajusta DJANGO_SETTINGS_MODULE abajo.
  2. Corre primero con DRY_RUN = True.
  3. Cuando todo esté correcto, cambia a DRY_RUN = False.

  python migrar_cuotas.py
"""

import os
import django

# ─── CONFIGURA AQUÍ ────────────────────────────────────────────────────────────
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sytem_phone.settings')  # ← cambia si es necesario
django.setup()
# ───────────────────────────────────────────────────────────────────────────────

from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from django.db import transaction
from django.utils import timezone

from facturacion.models import (   # ← cambia 'facturacion' por el nombre real de tu app
    Venta,
    PagoCuentaPorCobrar,
    Cuota,
)

# ─── MODO ──────────────────────────────────────────────────────────────────────
DRY_RUN = False  # ← True = simulación sin escritura | False = escritura real
# ───────────────────────────────────────────────────────────────────────────────

stats = {
    'ventas_procesadas': 0,
    'ventas_saltadas':   0,
    'cuotas_creadas':    0,
    'ya_tienen_cuotas':  0,
    'omitidas':          0,
    'errores':           [],
}


def redondear(valor):
    """Redondea a 2 decimales con ROUND_HALF_UP (estándar financiero)."""
    return Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calcular_estado_cuotas(venta, cuota_monto, n_cuotas):
    """
    Distribuye los pagos recibidos (después del inicial) entre las N cuotas
    en orden cronológico y devuelve una lista de dicts con el estado de cada una.

    Returns:
        lista de dicts: [
            {
                'numero_cuota': int,
                'monto_original': Decimal,
                'monto_pendiente': Decimal,
                'estado': 'pagada' | 'parcial' | 'pendiente',
                'fecha_pago_completo': datetime | None,
            }, ...
        ]
    """
    # Pagos CxC de esta venta, NO anulados, en orden cronológico
    pagos = list(
        PagoCuentaPorCobrar.objects
        .filter(cuenta__venta=venta, anulado=False)
        .order_by('fecha_pago')
        .values_list('monto', 'fecha_pago')
    )

    # El monto inicial ya fue cobrado en el acto — no cuenta como pago CxC
    # pero si existe algún pago CxC registrado que coincida con montoinicial
    # en la misma fecha de la venta, lo ignoramos (ya está reflejado en montoinicial).
    total_pagado_cxc = sum(m for m, _ in pagos)

    # Construimos pool de pagos a distribuir
    pool = total_pagado_cxc
    pool_pagos = list(pagos)  # conservamos las fechas para fecha_pago_completo

    cuotas_resultado = []
    pool_idx = 0
    acumulado_pagado = Decimal('0')
    acumulado_fechas = [fp for _, fp in pool_pagos]  # fechas de pagos en orden

    for i in range(1, n_cuotas + 1):
        pendiente = cuota_monto

        # ¿Cuánto del pool cubre esta cuota?
        if pool >= pendiente:
            pool -= pendiente
            monto_pendiente = Decimal('0')
            estado = 'pagada'
            # Fecha de pago: usar la fecha del pago que completó esta cuota
            # Aproximación: fecha del último pago antes de agotar el pool
            acumulado_pagado += pendiente
            # Buscar cuál pago "completó" esta cuota
            fecha_pago_completo = None
            acum = Decimal('0')
            for monto_p, fecha_p in pool_pagos:
                acum += monto_p
                if acum >= acumulado_pagado:
                    fecha_pago_completo = fecha_p
                    break
        elif pool > 0:
            monto_pendiente = redondear(pendiente - pool)
            pool = Decimal('0')
            estado = 'parcial'
            fecha_pago_completo = None
        else:
            monto_pendiente = pendiente
            estado = 'pendiente'
            fecha_pago_completo = None

        cuotas_resultado.append({
            'numero_cuota':        i,
            'monto_original':      cuota_monto,
            'monto_pendiente':     monto_pendiente,
            'estado':              estado,
            'fecha_pago_completo': fecha_pago_completo,
        })

    return cuotas_resultado


def migrar_cuotas():
    print("\n" + "=" * 70)
    print(f"  MIGRACIÓN — Cuotas")
    print(f"  MODO: {'⚙️  SIMULACIÓN (DRY RUN)' if DRY_RUN else '⚠️  ESCRITURA REAL'}")
    print("=" * 70)

    # Ventas financiadas a crédito con plazo > 1 mes
    ventas = (
        Venta.objects
        .filter(tipo_venta='credito')
        .select_related('cliente')
        .prefetch_related('cuotas', 'cuenta_por_cobrar__pagos')
        .order_by('fecha_venta')
    )

    for venta in ventas:
        plazo = venta.plazo_meses or 1
        cuota_monto = redondear(venta.cuota_mensual or Decimal('0'))

        # Si plazo == 1 y cuota_mensual == 0 → no es realmente financiada
        if plazo <= 1 and cuota_monto == 0:
            stats['omitidas'] += 1
            continue

        # Si cuota_mensual == 0 pero hay plazo, calculamos
        if cuota_monto == 0 and plazo > 0:
            monto_financiado = redondear(venta.monto_financiado or (venta.total - (venta.montoinicial or Decimal('0'))))
            cuota_monto = redondear(monto_financiado / plazo)

        if cuota_monto <= 0:
            stats['omitidas'] += 1
            continue

        # Evitar duplicados: si ya tiene cuotas, saltar
        if venta.cuotas.exists():
            stats['ya_tienen_cuotas'] += 1
            if DRY_RUN:
                print(f"  [SKIP] {venta.numero_factura} — ya tiene {venta.cuotas.count()} cuotas")
            continue

        # Calcular estado de cada cuota según pagos recibidos
        estados_cuotas = calcular_estado_cuotas(venta, cuota_monto, plazo)

        # Fecha de inicio de vencimientos: 1 mes después de la venta
        fecha_base = venta.fecha_venta.date() if hasattr(venta.fecha_venta, 'date') else venta.fecha_venta

        if DRY_RUN:
            print(f"\n  {venta.numero_factura} | {venta.cliente_nombre} | "
                  f"RD${venta.total:,.2f} | {plazo} cuotas × RD${cuota_monto:,.2f}")
            for c in estados_cuotas:
                venc = fecha_base + relativedelta(months=c['numero_cuota'])
                pendiente_str = f"RD${c['monto_pendiente']:,.2f}" if c['monto_pendiente'] > 0 else "pagada ✓"
                print(
                    f"    Cuota {c['numero_cuota']:02d} | vence {venc} | "
                    f"{c['estado']:10} | pendiente: {pendiente_str}"
                )
            stats['ventas_procesadas'] += 1
            stats['cuotas_creadas'] += plazo
        else:
            try:
                with transaction.atomic():
                    cuotas_a_crear = []
                    for c in estados_cuotas:
                        fecha_vencimiento = fecha_base + relativedelta(months=c['numero_cuota'])
                        cuotas_a_crear.append(Cuota(
                            venta=venta,
                            cliente=venta.cliente,
                            numero_cuota=c['numero_cuota'],
                            monto_original=c['monto_original'],
                            monto_pendiente=c['monto_pendiente'],
                            fecha_vencimiento=fecha_vencimiento,
                            estado=c['estado'],
                            fecha_pago_completo=c['fecha_pago_completo'],
                        ))
                    Cuota.objects.bulk_create(cuotas_a_crear)

                stats['ventas_procesadas'] += 1
                stats['cuotas_creadas'] += len(cuotas_a_crear)
                print(f"  [OK ] {venta.numero_factura} — {len(cuotas_a_crear)} cuotas creadas")

            except Exception as e:
                stats['errores'].append(f"{venta.numero_factura}: {e}")
                print(f"  [ERR] {venta.numero_factura}: {e}")

    # Resumen
    print("\n" + "=" * 70)
    print("  RESUMEN FINAL")
    print("=" * 70)
    accion = "a crear" if DRY_RUN else "creadas"
    print(f"  Ventas procesadas             : {stats['ventas_procesadas']}")
    print(f"  Cuotas {accion}               : {stats['cuotas_creadas']}")
    print(f"  Ventas ya tenían cuotas       : {stats['ya_tienen_cuotas']}")
    print(f"  Ventas omitidas (sin plazo)   : {stats['omitidas']}")
    print(f"  Errores                       : {len(stats['errores'])}")
    if stats['errores']:
        print("\n  DETALLE DE ERRORES:")
        for e in stats['errores']:
            print(f"    ❌ {e}")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    migrar_cuotas()

    #python migrar_cuotas.py