from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from facturacion.models import Proveedor, Cliente, EntradaProducto, Caja


class Command(BaseCommand):
    help = 'Crea datos de ejemplo para desarrollo (usuario, proveedores, clientes, productos, caja)'

    def handle(self, *args, **options):
        # ── Usuario ──────────────────────────────────────────────────────
        user, created = User.objects.get_or_create(
            username='pope',
            defaults={
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            user.set_password('pope2828')
            user.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario "pope" creado (password: pope2828)'))
        else:
            user.set_password('pope2828')
            user.save()
            self.stdout.write(self.style.SUCCESS('✓ Usuario "pope" actualizado'))

        # ── Proveedores ──────────────────────────────────────────────────
        proveedores_data = [
            {
                'nombre_empresa': 'Importadora Moto República',
                'rnc': '101234567',
                'nombre_contacto': 'Roberto Fernández',
                'email': 'ventas@importadoramotord.com',
                'telefono': '809-555-0101',
                'pais': 'DO',
                'ciudad': 'Santo Domingo',
                'direccion': 'Av. John F. Kennedy #45, Santo Domingo',
                'terminos_pago': '30-dias',
                'limite_credito': Decimal('500000.00'),
            },
            {
                'nombre_empresa': 'Distribuidora de Motores del Caribe',
                'rnc': '102345678',
                'nombre_contacto': 'María Santos',
                'email': 'info@dmcaribe.com',
                'telefono': '809-555-0202',
                'pais': 'DO',
                'ciudad': 'Santiago',
                'direccion': 'Calle El Sol #22, Santiago',
                'terminos_pago': '45-dias',
                'limite_credito': Decimal('750000.00'),
            },
            {
                'nombre_empresa': 'Taiwan Motors Supply',
                'rnc': '103456789',
                'nombre_contacto': 'Wei Chen',
                'email': 'sales@taiwanmotors.tw',
                'telefono': '+886-2-2555-0303',
                'pais': 'TW',
                'ciudad': 'Taipéi',
                'direccion': 'No. 88, Sec. 2, Zhongshan N. Rd., Taipei',
                'terminos_pago': 'contado',
                'limite_credito': Decimal('0.00'),
            },
        ]
        for p in proveedores_data:
            prov, created = Proveedor.objects.get_or_create(
                rnc=p['rnc'],
                defaults=p,
            )
            if created:
                self.stdout.write(f'  ✓ Proveedor "{prov.nombre_empresa}" creado')
            else:
                self.stdout.write(f'  ~ Proveedor "{prov.nombre_empresa}" ya existe')

        # ── Clientes ─────────────────────────────────────────────────────
        clientes_data = [
            {
                'full_name': 'Juan Pérez',
                'identification_number': '001-1234567-8',
                'primary_phone': '809-111-2233',
                'secondary_phone': '849-111-2233',
                'address': 'Calle Primera #10, Los Prados, Santo Domingo',
                'email': 'juan.perez@email.com',
                'credit_limit': Decimal('150000.00'),
            },
            {
                'full_name': 'María Rodríguez',
                'identification_number': '002-2345678-9',
                'primary_phone': '809-222-3344',
                'address': 'Av. Central #55, Ensanche Ozama, Santo Domingo Este',
                'email': 'maria.rodriguez@email.com',
                'credit_limit': Decimal('100000.00'),
            },
            {
                'full_name': 'Carlos Jiménez',
                'identification_number': '003-3456789-0',
                'primary_phone': '809-333-4455',
                'secondary_phone': '829-333-4455',
                'address': 'Calle Las Flores #8, Villa Consuelo, Santiago',
                'email': 'carlos.jimenez@email.com',
                'credit_limit': Decimal('200000.00'),
            },
            {
                'full_name': 'Ana Martínez',
                'identification_number': '004-4567890-1',
                'primary_phone': '809-444-5566',
                'address': 'Calle Duarte #100, La Vega',
                'email': 'ana.martinez@email.com',
                'credit_limit': Decimal('75000.00'),
            },
        ]
        for c in clientes_data:
            cli, created = Cliente.objects.get_or_create(
                identification_number=c['identification_number'],
                defaults=c,
            )
            if created:
                self.stdout.write(f'  ✓ Cliente "{cli.full_name}" creado')
            else:
                self.stdout.write(f'  ~ Cliente "{cli.full_name}" ya existe')

        # ── Productos (EntradaProducto) ──────────────────────────────────
        proveedor_moto = Proveedor.objects.get(rnc='101234567')
        proveedor_taiwan = Proveedor.objects.get(rnc='103456789')
        proveedor_caribe = Proveedor.objects.get(rnc='102345678')

        productos_data = [
            {
                'proveedor': proveedor_moto,
                'numero_factura': 'FACT-001',
                'nombre_producto': 'Suzuki AX-100',
                'marca': 'suzuki',
                'modelo': 'AX-100',
                'estado': 'nuevo',
                'color': 'rojo',
                'cantidad': 5,
                'cantidad_minima': 2,
                'costo_compra': Decimal('45000.00'),
                'costo_venta': Decimal('62000.00'),
            },
            {
                'proveedor': proveedor_moto,
                'numero_factura': 'FACT-001',
                'nombre_producto': 'Honda CG 150',
                'marca': 'honda',
                'modelo': 'CG150',
                'estado': 'nuevo',
                'color': 'negro',
                'cantidad': 8,
                'cantidad_minima': 3,
                'costo_compra': Decimal('38000.00'),
                'costo_venta': Decimal('52000.00'),
            },
            {
                'proveedor': proveedor_taiwan,
                'numero_factura': 'FACT-TW-001',
                'nombre_producto': 'Yamaha YBR 125',
                'marca': 'yamaha',
                'modelo': 'YBR125',
                'estado': 'nuevo',
                'color': 'azul',
                'cantidad': 6,
                'cantidad_minima': 2,
                'costo_compra': Decimal('42000.00'),
                'costo_venta': Decimal('58000.00'),
            },
            {
                'proveedor': proveedor_taiwan,
                'numero_factura': 'FACT-TW-002',
                'nombre_producto': 'X1000 250cc',
                'marca': 'x1000',
                'modelo': 'X1000-250',
                'estado': 'nuevo',
                'color': 'blanco',
                'cantidad': 3,
                'cantidad_minima': 1,
                'costo_compra': Decimal('55000.00'),
                'costo_venta': Decimal('75000.00'),
            },
            {
                'proveedor': proveedor_caribe,
                'numero_factura': 'FACT-CAR-001',
                'nombre_producto': 'KTM Duke 200',
                'marca': 'ktm',
                'modelo': 'Duke200',
                'estado': 'nuevo',
                'color': 'naranja',
                'cantidad': 2,
                'cantidad_minima': 1,
                'costo_compra': Decimal('95000.00'),
                'costo_venta': Decimal('130000.00'),
            },
            {
                'proveedor': proveedor_caribe,
                'numero_factura': 'FACT-CAR-002',
                'nombre_producto': 'Bajaj Pulsar NS200',
                'marca': 'bajaj',
                'modelo': 'NS200',
                'estado': 'nuevo',
                'color': 'negro',
                'cantidad': 4,
                'cantidad_minima': 2,
                'costo_compra': Decimal('65000.00'),
                'costo_venta': Decimal('88000.00'),
            },
        ]

        for prod in productos_data:
            nombre = prod['nombre_producto']
            codigo_serial = f"SEED-{nombre.replace(' ', '-').upper()}"
            obj, created = EntradaProducto.objects.get_or_create(
                codigo_producto__startswith='PROD-',
                nombre_producto=nombre,
                defaults=prod,
            )
            if created:
                self.stdout.write(f'  ✓ Producto "{nombre}" creado (código: {obj.codigo_producto})')
            else:
                self.stdout.write(f'  ~ Producto "{nombre}" ya existe (código: {obj.codigo_producto})')

        # ── Caja inicial abierta ─────────────────────────────────────────
        caja_abierta = Caja.objects.filter(usuario=user, estado='abierta').first()
        if not caja_abierta:
            Caja.objects.create(
                usuario=user,
                monto_inicial=Decimal('15000.00'),
                estado='abierta',
            )
            self.stdout.write(self.style.SUCCESS('✓ Caja inicial abierta creada (RD$15,000)'))
        else:
            self.stdout.write('~ Caja abierta ya existe para este usuario')

        self.stdout.write(self.style.SUCCESS('\n✅ Seed data completado exitosamente.'))
