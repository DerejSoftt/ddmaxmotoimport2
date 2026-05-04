import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sytem_phone.settings")
django.setup()

from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from facturacion.views import entrada
from facturacion.models import Proveedor
from django.utils import timezone

proveedor, created = Proveedor.objects.get_or_create(
    nombre_empresa="Test Proveedor",
    rnc="123456789",
    nombre_contacto="Test Contacto",
    email="test@test.com",
    telefono="1234567890",
    activo=True
)

factory = RequestFactory()
request = factory.post('/entrada', {
    'numero_factura': 'FAC-TEST-003',
    'fecha_entrada': timezone.now().date().isoformat(),
    'proveedor': proveedor.id,
    'ncf': '',
    'nombre_producto': 'Test Product',
    'marca': 'honda',
    'modelo': 'Test Model',
    'capacidad': '128',
    'imei_serial': '',
    'estado': 'nuevo',
    'color': 'negro',
    'numero_maquina': 'MAQ001',
    'cantidad': '1',
    'costo_compra': '1000',
    'porcentaje_itbis': '18',
    'costo_venta': '1500',
    'observaciones': ''
})

setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)

try:
    response = entrada(request)
    print("Response status:", response.status_code)
    for msg in messages:
        print(f"Message: {msg}")
except Exception as e:
    import traceback
    traceback.print_exc()
