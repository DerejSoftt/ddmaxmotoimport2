from django.shortcuts import render, redirect, get_object_or_404 
from .models import EntradaProducto, Proveedor,  Cliente, Caja, Venta, DetalleVenta, MovimientoStock
from django.contrib import messages

from django.http import JsonResponse
from django.db import models
from django.core.validators import ValidationError
from django.db import transaction
from decimal import Decimal
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.db.models import Q
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings
import random
import string
import time
from django.db.models import Max


# Create your views her
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('iniciocaja')  # Asegúrate de tener esta URL configurada
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, "facturacion/index.html")



def dashboard(request):
    return render(request, "facturacion/dashboard.html")




def inventario(request):
    return render(request, "facturacion/inventario.html")

@require_http_methods(["GET"])
def inventario_datos(request):
    try:
        # Versión simple para debugging
        productos = list(EntradaProducto.objects.all().values())
        proveedores = list(Proveedor.objects.all().values())
        
        return JsonResponse({
            'productos': productos,
            'proveedores': proveedores
        })
    except Exception as e:
        return JsonResponse({'error': 'Error interno del servidor: ' + str(e)}, status=500)



@require_http_methods(["PUT"])
@csrf_exempt
def inventario_editar(request, id):
    try:
        # Obtener el producto
        producto = EntradaProducto.objects.get(id=id)
        data = json.loads(request.body)
        
        # Actualizar campos
        producto.numero_factura = data.get('numero_factura', producto.numero_factura)
        
        
        # Manejar el proveedor (puede ser ID o objeto)
        proveedor_id = data.get('proveedor')
        if proveedor_id:
            try:
                producto.proveedor = Proveedor.objects.get(id=proveedor_id)
            except Proveedor.DoesNotExist:
                return JsonResponse({'error': 'Proveedor no encontrado'}, status=400)
        
        producto.ncf = data.get('ncf', producto.ncf)
        producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
        producto.marca = data.get('marca', producto.marca)
        producto.capacidad = data.get('capacidad', producto.capacidad)
        producto.estado = data.get('estado', producto.estado)
        producto.color = data.get('color', producto.color)
        producto.costo_compra = data.get('costo_compra', producto.costo_compra)
        producto.porcentaje_itbis = data.get('porcentaje_itbis', producto.porcentaje_itbis)
        producto.costo_venta = data.get('costo_venta', producto.costo_venta)
        producto.observaciones = data.get('observaciones', producto.observaciones)
        
        # Guardar cambios (los cálculos se harán automáticamente en el método save)
        producto.save()
        
        # Devolver el producto actualizado
        producto_actualizado = {
            'id': producto.id,
            'codigo_producto': producto.codigo_producto,
            'nombre_producto': producto.nombre_producto,
            'marca': producto.marca,
            'capacidad': producto.capacidad,
            'estado': producto.estado,
            'color': producto.color,
            'cantidad': producto.cantidad,
            'costo_compra': float(producto.costo_compra),
            'costo_venta': float(producto.costo_venta),
            'ncf': producto.ncf,
            'observaciones': producto.observaciones
        }
        
        return JsonResponse(producto_actualizado)
    except EntradaProducto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
@csrf_exempt
def inventario_eliminar(request, id):
    try:
        producto = EntradaProducto.objects.get(id=id)
        producto.delete()
        return JsonResponse({'success': True, 'message': 'Producto eliminado correctamente'})
    except EntradaProducto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@login_required
def iniciocaja(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        monto_inicial = request.POST.get('monto_inicial')
        
        # Validar el monto
        try:
            monto_inicial = float(monto_inicial)
            if monto_inicial < 0:
                messages.error(request, 'El monto inicial debe ser mayor o igual a cero.')
                return render(request, "facturacion/iniciocaja.html")
        except (ValueError, TypeError):
            messages.error(request, 'Por favor ingrese un monto válido.')
            return render(request, "facturacion/iniciocaja.html")
        
        # Verificar si el usuario ya tiene una caja abierta
        caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
        if caja_abierta:
            messages.error(request, 'Ya tienes una caja abierta. Debes cerrarla antes de abrir una nueva.')
            return render(request, "facturacion/iniciocaja.html")
        
        # Crear nueva caja
        try:
            nueva_caja = Caja(
                usuario=request.user,
                monto_inicial=monto_inicial,
                estado='abierta'
            )
            nueva_caja.save()
            
            messages.success(request, 'Caja iniciada correctamente. Redirigiendo a ventas...')
            # Redirigir a ventas después de un breve retraso para mostrar el mensaje
            return redirect('ventas')  # Asegúrate de tener una URL llamada 'ventas'
            
        except Exception as e:
            messages.error(request, f'Error al iniciar la caja: {str(e)}')
    
    return render(request, "facturacion/iniciocaja.html", {'user': request.user})


# @login_required
# def ventas(request):
#     # Verificar que el usuario tenga una caja abierta
#     caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
#     if not caja_abierta:
#         messages.error(request, 'Debes abrir una caja antes de realizar ventas.')
#         return redirect('iniciocaja')
    
#     if request.method == 'POST':
#         return procesar_venta(request, caja_abierta)
    
#     # Obtener clientes
#     clientes = Cliente.objects.filter(status=True)
    
#     return render(request, "facturacion/ventas.html", {
#         'user': request.user,
#         'caja_abierta': caja_abierta,
#         'clientes': clientes
#     })


# @transaction.atomic
# def procesar_venta(request, caja_abierta):
#     try:
#         # Obtener datos del formulario
#         payment_type = request.POST.get('payment_type')
#         payment_method = request.POST.get('payment_method')
#         client_id = request.POST.get('client_id')
#         client_name = request.POST.get('client_name')
#         client_document = request.POST.get('client_document')
#         subtotal = float(request.POST.get('subtotal', 0))
#         discount_percentage = float(request.POST.get('discount_percentage', 0))
#         discount_amount = float(request.POST.get('discount_amount', 0))
#         total = float(request.POST.get('total', 0))
#         cash_received = float(request.POST.get('cash_received', 0))
#         change_amount = float(request.POST.get('change_amount', 0))
#         sale_items = json.loads(request.POST.get('sale_items', '[]'))
        
#         # Validar que hay productos en la venta
#         if not sale_items:
#             messages.error(request, 'La venta debe contener al menos un producto.')
#             return redirect('ventas')
        
#         # Procesar cliente
#         cliente = None
#         if payment_type == 'credit' and client_id:
#             cliente = Cliente.objects.get(id=client_id, status=True)
            
#             # Validar límite de crédito para ventas a crédito
#             if total > cliente.credit_limit:
#                 messages.error(request, f'El monto de la venta (RD${total:.2f}) excede el límite de crédito del cliente (RD${cliente.credit_limit:.2f}).')
#                 return redirect('ventas')
                
#         elif client_name:
#             # Para ventas al contado, crear cliente rápido si no existe
#             if client_document:
#                 cliente = Cliente.objects.filter(identification_number=client_document, status=True).first()
            
#             if not cliente:
#                 cliente = Cliente.objects.create(
#                     full_name=client_name,
#                     identification_number=client_document or f"CLI-{int(timezone.now().timestamp())}",
#                     primary_phone="",
#                     address="",
#                     credit_limit=0,
#                     status=True
#                 )
        
#         # Crear la venta
#         venta = Venta.objects.create(
#             caja=caja_abierta,
#             cliente=cliente,
#             subtotal=subtotal,
#             descuento_porcentaje=discount_percentage,
#             descuento_monto=discount_amount,
#             total=total,
#             tipo_venta='credito' if payment_type == 'credit' else 'contado',
#             metodo_pago=payment_method
#         )
        
#         # Crear detalles de venta y actualizar stock
#         for item in sale_items:
#             try:
#                 # Buscar el producto por ID
#                 producto = EntradaProducto.objects.get(id=item['productId'])
                
#                 # Verificar stock
#                 if producto.cantidad < item['quantity']:
#                     raise Exception(f'Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.cantidad}')
                
#                 # Crear detalle
#                 DetalleVenta.objects.create(
#                     venta=venta,
#                     producto=producto,
#                     cantidad=item['quantity'],
#                     precio_unitario=item['price'],
#                     subtotal=item['subtotal']
#                 )
                
#                 # Actualizar stock - ¡ESTO ES LO IMPORTANTE!
#                 producto.cantidad -= item['quantity']
#                 producto.save()
                
#             except EntradaProducto.DoesNotExist:
#                 # Si el producto no existe, continuar con el siguiente pero registrar el error
#                 messages.warning(request, f'Producto con ID {item.get("productId")} no encontrado.')
#                 continue
        
#         # Si es venta a crédito, crear cuenta por cobrar
#         if payment_type == 'credit' and cliente:
#             fecha_vencimiento = date.today() + timedelta(days=30)  # 30 días para pagar
            
#             CuentaPorCobrar.objects.create(
#                 venta=venta,
#                 cliente=cliente,
#                 monto_total=total,
#                 saldo_pendiente=total,
#                 fecha_vencimiento=fecha_vencimiento,
#                 estado='pendiente'
#             )
        
#         messages.success(request, f'Venta #{venta.id} registrada exitosamente. Total: RD${total:.2f}')
#         return redirect('ventas')
    
#     except Exception as e:
#         messages.error(request, f'Error al procesar venta: {str(e)}')
#         return redirect('ventas')




# @login_required
# def buscar_productos(request):
#     """Vista para buscar productos via AJAX en la tabla EntradaProducto"""
#     if request.method == 'GET':
#         query = request.GET.get('q', '')
        
#         try:
#             # Buscar productos por nombre, código, modelo o marca
#             productos = EntradaProducto.objects.filter(
#                 cantidad__gt=0  # Solo productos con stock disponible
#             ).filter(
#                 Q(nombre_producto__icontains=query) | 
#                 Q(codigo_producto__icontains=query) |
#                 Q(modelo__icontains=query) |
#                 Q(marca__icontains=query) |
#                 Q(imei_serial__icontains=query)
#             )[:10]  # Limitar a 10 resultados
            
#             productos_data = []
#             for producto in productos:
#                 productos_data.append({
#                     'id': producto.id,
#                     'nombre': producto.nombre_producto,
#                     'codigo': producto.codigo_producto,
#                     'precio': float(producto.costo_venta),  # Usar el precio de venta
#                     'stock': producto.cantidad,
#                     'marca': producto.get_marca_display(),
#                     'modelo': producto.modelo,
#                     'imei': producto.imei_serial
#                 })
            
#             return JsonResponse({'productos': productos_data, 'success': True})
            
#         except Exception as e:
#             return JsonResponse({'error': str(e), 'success': False})
    
#     return JsonResponse({'error': 'Método no permitido', 'success': False})



@login_required
def ventas(request):
    # Verificar que el usuario tenga una caja abierta
    try:
        caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
        if not caja_abierta:
            messages.error(request, 'Debes abrir una caja antes de realizar ventas.')
            return redirect('iniciocaja')
        
        if request.method == 'POST':
            return procesar_venta(request)
        
        # Obtener clientes y productos activos
        clientes = Cliente.objects.filter(status=True)
        productos = EntradaProducto.objects.filter(activo=True, cantidad__gt=0)
        
        return render(request, "facturacion/ventas.html", {
            'user': request.user,
            'caja_abierta': caja_abierta,
            'clientes': clientes,
            'productos': productos
        })
    
    except Exception as e:
        messages.error(request, f'Error al cargar la página de ventas: {str(e)}')
        return redirect('inicio')

@csrf_exempt
@require_POST
@transaction.atomic
def procesar_venta(request):
    try:
        data = request.POST
        user = request.user
        
        # Función segura para conversión a Decimal
        def safe_decimal(value, default=0):
            if value is None or value == '':
                return Decimal(default)
            try:
                return Decimal(str(value).replace(',', '.'))
            except (InvalidOperation, ValueError):
                return Decimal(default)
        
        # Convertir valores
        payment_type = data.get('payment_type', 'contado')
        payment_method = data.get('payment_method', 'efectivo')
        subtotal = safe_decimal(data.get('subtotal', 0))
        discount_percentage = safe_decimal(data.get('discount_percentage', 0))
        discount_amount = safe_decimal(data.get('discount_amount', 0))
        total = safe_decimal(data.get('total', 0))
        cash_received = safe_decimal(data.get('cash_received', 0))
        change_amount = safe_decimal(data.get('change_amount', 0))
        
        # Validaciones
        if payment_type not in ['contado', 'credito']:
            return JsonResponse({'success': False, 'message': 'Tipo de pago inválido'})
        
        if payment_method not in ['efectivo', 'tarjeta', 'transferencia']:
            return JsonResponse({'success': False, 'message': 'Método de pago inválido'})
        
        # Procesar información del cliente
        client_id = data.get('client_id')
        client_name = data.get('client_name', '').strip()
        client_document = data.get('client_document', '').strip()
        
        cliente = None
        if payment_type == 'credito':
            if not client_id:
                return JsonResponse({'success': False, 'message': 'Debe seleccionar un cliente para ventas a crédito'})
            
            try:
                cliente = Cliente.objects.get(id=client_id, status=True)
                if total > cliente.credit_limit:
                    return JsonResponse({
                        'success': False, 
                        'message': f'El monto excede el límite de crédito del cliente (RD${cliente.credit_limit})'
                    })
            except Cliente.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Cliente no válido'})
        else:
            if not client_name:
                return JsonResponse({'success': False, 'message': 'Debe ingresar el nombre del cliente'})
        
        # Procesar items de la venta
        sale_items_json = data.get('sale_items')
        if not sale_items_json:
            return JsonResponse({'success': False, 'message': 'No hay productos en la venta'})
        
        sale_items = json.loads(sale_items_json)
        if not sale_items:
            return JsonResponse({'success': False, 'message': 'No hay productos en la venta'})
        
        # Verificar stock antes de procesar la venta
        for item in sale_items:
            try:
                producto = EntradaProducto.objects.get(id=item['productId'], activo=True)
                cantidad_solicitada = int(item['quantity'])
                
                if not producto.tiene_stock_suficiente(cantidad_solicitada):
                    return JsonResponse({
                        'success': False, 
                        'message': f'Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.cantidad}'
                    })
            except EntradaProducto.DoesNotExist:
                return JsonResponse({'success': False, 'message': f'Producto no encontrado: {item.get("name", "Desconocido")}'})
            except (ValueError, KeyError):
                return JsonResponse({'success': False, 'message': f'Cantidad inválida para producto: {item.get("name", "Desconocido")}'})
        
        # Crear la venta
        venta = Venta(
            vendedor=user,
            cliente=cliente,
            cliente_nombre=client_name,
            cliente_documento=client_document,
            tipo_venta=payment_type,
            metodo_pago=payment_method,
            subtotal=subtotal,
            descuento_porcentaje=discount_percentage,
            descuento_monto=discount_amount,
            total=total,
            efectivo_recibido=cash_received,
            cambio=change_amount,
            completada=True
        )
        venta.save()
        
        # Procesar detalles de venta y descontar stock
        for item in sale_items:
            producto = EntradaProducto.objects.get(id=item['productId'])
            cantidad = int(item['quantity'])
            precio_unitario = safe_decimal(item['price'])
            
            # Descontar stock con manejo de error por si no existe el método
            try:
                if not producto.restar_stock(
                    cantidad=cantidad,
                    usuario=user,
                    motivo="Venta",
                    referencia=venta.numero_factura
                ):
                    raise Exception(f'Error al procesar stock para {producto.nombre_producto}')
            except AttributeError:
                # Si el método registrar_movimiento_stock no existe, usar versión simple
                if not producto.tiene_stock_suficiente(cantidad):
                    raise Exception(f'Stock insuficiente para {producto.nombre_producto}')
                
                cantidad_anterior = producto.cantidad
                producto.cantidad -= cantidad
                producto.save(update_fields=['cantidad'])
                
                print(f"Stock actualizado (método simple): {producto.nombre_producto} -{cantidad} unidades")
            
            # Crear detalle de venta
            detalle = DetalleVenta(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=safe_decimal(item['subtotal'])
            )
            detalle.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Venta procesada correctamente',
            'venta_id': venta.id,
            'numero_factura': venta.numero_factura
        })
        
    except Exception as e:
        transaction.set_rollback(True)
        return JsonResponse({'success': False, 'message': f'Error al procesar la venta: {str(e)}'})

def buscar_productos(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'success': True, 'productos': []})
    
    try:
        # Buscar por nombre, código o IMEI
        productos = EntradaProducto.objects.filter(
            Q(nombre_producto__icontains=query) |
            Q(codigo_producto__icontains=query) |
            Q(imei_serial__icontains=query) |
            Q(modelo__icontains=query),
            activo=True,
            cantidad__gt=0
        )[:10]  # Limitar a 10 resultados
        
        resultados = []
        for producto in productos:
            resultados.append({
                'id': producto.id,
                'nombre': producto.nombre_producto,
                'codigo': producto.codigo_producto,
                'precio': float(producto.costo_venta),
                'stock': producto.cantidad,
                'marca': producto.get_marca_display(),
                'modelo': producto.modelo,
                'imei': producto.imei_serial
            })
        
        return JsonResponse({'success': True, 'productos': resultados})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error en la búsqueda: {str(e)}'})
    



# def comprobante_venta(request, venta_id):
#     # Obtener la venta
#     venta = get_object_or_404(Venta, id=venta_id)
    
#     # Crear un buffer para el PDF
#     buffer = BytesIO()
    
#     # Tamaño para papel de 80mm (80mm de ancho, alto dinámico)
#     width = 80 * mm
#     height = 1000 * mm  # Alto grande que se ajustará al contenido
    
#     # Crear el canvas
#     p = canvas.Canvas(buffer, pagesize=(width, height))
    
#     # Configuración
#     p.setFont("Helvetica", 7)
#     margin_left = 5 * mm
#     margin_right = 5 * mm
#     y_position = height - 10 * mm
#     line_height = 3 * mm
    
#     # Logo (si tienes uno)
#     try:
#         logo_path = os.path.join(settings.STATIC_ROOT, 'img', 'logo.png')
#         if os.path.exists(logo_path):
#             logo = ImageReader(logo_path)
#             p.drawImage(logo, margin_left, y_position, width=20*mm, height=15*mm)
#             y_position -= 18 * mm
#         else:
#             # Dibujar logo por defecto si no existe
#             p.setFont("Helvetica-Bold", 10)
#             p.drawString(margin_left, y_position, "D'URO CELL")
#             p.setFont("Helvetica", 7)
#             y_position -= line_height * 2
#     except:
#         p.setFont("Helvetica-Bold", 10)
#         p.drawString(margin_left, y_position, "D'URO CELL")
#         p.setFont("Helvetica", 7)
#         y_position -= line_height * 2
    
#     # Información de la empresa
#     p.setFont("Helvetica-Bold", 8)
#     p.drawString(margin_left, y_position, "D'URO CELL")
#     y_position -= line_height
    
#     p.setFont("Helvetica", 7)
#     p.drawString(margin_left, y_position, "Tel: (809) 123-4567")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, "Calle Principal #123")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, "Santo Domingo, RD")
#     y_position -= line_height * 2
    
#     # Línea separadora
#     p.line(margin_left, y_position, width - margin_right, y_position)
#     y_position -= line_height * 2
    
#     # Información de la factura
#     p.setFont("Helvetica-Bold", 8)
#     p.drawString(margin_left, y_position, f"FACTURA: {venta.numero_factura}")
#     y_position -= line_height
    
#     p.setFont("Helvetica", 7)
#     p.drawString(margin_left, y_position, f"Fecha: {venta.fecha_venta.strftime('%d/%m/%Y %H:%M')}")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, f"Vendedor: {venta.vendedor.get_full_name() or venta.vendedor.username}")
#     y_position -= line_height * 2
    
#     # Información del cliente
#     p.drawString(margin_left, y_position, f"Cliente: {venta.cliente_nombre}")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, f"Documento: {venta.cliente_documento}")
#     y_position -= line_height * 2
    
#     # Línea separadora
#     p.line(margin_left, y_position, width - margin_right, y_position)
#     y_position -= line_height * 2
    
#     # Encabezado de productos
#     p.setFont("Helvetica-Bold", 8)
#     p.drawString(margin_left, y_position, "DESCRIPCIÓN")
#     p.drawString(width - margin_right - 20*mm, y_position, "TOTAL")
#     y_position -= line_height
    
#     p.line(margin_left, y_position, width - margin_right, y_position)
#     y_position -= line_height
    
#     # Detalles de productos
#     p.setFont("Helvetica", 7)
#     for detalle in venta.detalles.all():
#         # Nombre del producto (truncar si es muy largo)
#         nombre = detalle.producto.nombre_producto
#         if len(nombre) > 25:
#             nombre = nombre[:22] + "..."
        
#         # Primera línea: nombre del producto
#         p.drawString(margin_left, y_position, nombre)
#         y_position -= line_height
        
#         # Segunda línea: cantidad y precio unitario
#         linea_detalle = f"{detalle.cantidad} x RD$ {detalle.precio_unitario:.2f}"
#         p.drawString(margin_left + 5*mm, y_position, linea_detalle)
        
#         # Subtotal alineado a la derecha
#         subtotal_text = f"RD$ {detalle.subtotal:.2f}"
#         p.drawString(width - margin_right - 20*mm, y_position, subtotal_text)
#         y_position -= line_height
        
#         # IMEI si está disponible
#         if detalle.producto.imei_serial:
#             p.drawString(margin_left + 5*mm, y_position, f"IMEI: {detalle.producto.imei_serial}")
#             y_position -= line_height
        
#         # Espacio entre productos
#         y_position -= line_height * 0.5
        
#         # Verificar si necesitamos nueva página
#         if y_position < 50 * mm:
#             p.showPage()
#             p.setFont("Helvetica", 7)
#             y_position = height - 10 * mm
    
#     # Línea separadora
#     p.line(margin_left, y_position, width - margin_right, y_position)
#     y_position -= line_height * 2
    
#     # Totales
#     p.drawString(margin_left, y_position, f"Subtotal:")
#     p.drawString(width - margin_right - 20*mm, y_position, f"RD$ {venta.subtotal:.2f}")
#     y_position -= line_height
    
#     if venta.descuento_monto > 0:
#         p.drawString(margin_left, y_position, f"Descuento ({venta.descuento_porcentaje}%):")
#         p.drawString(width - margin_right - 20*mm, y_position, f"-RD$ {venta.descuento_monto:.2f}")
#         y_position -= line_height
    
#     p.setFont("Helvetica-Bold", 9)
#     p.drawString(margin_left, y_position, "TOTAL:")
#     p.drawString(width - margin_right - 20*mm, y_position, f"RD$ {venta.total:.2f}")
#     y_position -= line_height * 2
    
#     p.setFont("Helvetica", 7)
    
#     # Información de pago
#     p.drawString(margin_left, y_position, f"Tipo: {venta.get_tipo_venta_display()}")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, f"Método: {venta.get_metodo_pago_display()}")
#     y_position -= line_height
    
#     if venta.tipo_venta == 'contado' and venta.metodo_pago == 'efectivo':
#         p.drawString(margin_left, y_position, f"Recibido: RD$ {venta.efectivo_recibido:.2f}")
#         y_position -= line_height
#         p.drawString(margin_left, y_position, f"Cambio: RD$ {venta.cambio:.2f}")
#         y_position -= line_height
    
#     # Línea separadora
#     p.line(margin_left, y_position, width - margin_right, y_position)
#     y_position -= line_height * 2
    
#     # Pie de página
#     p.drawString(margin_left, y_position, "¡Gracias por su compra!")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, "Garantía según política de la tienda")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, "Presentar esta factura para garantía")
#     y_position -= line_height
#     p.drawString(margin_left, y_position, "No se aceptan devoluciones sin factura")
#     y_position -= line_height * 2
    
#     # Código de barras o QR (opcional)
#     p.drawString(margin_left, y_position, f"Ref: {venta.numero_factura}")
    
#     # Finalizar el PDF
#     p.showPage()
#     p.save()
    
#     # Obtener el valor del buffer y crear la respuesta
#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="factura-{venta.numero_factura}.pdf"'
    
#     return response


def comprobante_venta(request, venta_id):
    # Obtener la venta y sus detalles
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all()
    
    # Renderizar el template HTML
    return render(request, 'facturacion/comprobante_venta.html', {
        'venta': venta,
        'detalles': detalles
    })

# Vista para ver el historial de ventas
# @login_required
# def historial_ventas(request):
#     caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
    
#     # Obtener ventas de la caja actual o todas las ventas del usuario
#     if caja_abierta:
#         ventas = Venta.objects.filter(caja=caja_abierta).order_by('-fecha_venta')
#     else:
#         # Si no hay caja abierta, mostrar las últimas ventas del usuario
#         cajas_usuario = Caja.objects.filter(usuario=request.user)
#         ventas = Venta.objects.filter(caja__in=cajas_usuario).order_by('-fecha_venta')[:50]
    
#     return render(request, "facturacion/historial_ventas.html", {
#         'ventas': ventas,
#         'caja_abierta': caja_abierta
#     })

# Vista para ver los detalles de una venta
@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    # Verificar que la venta pertenece al usuario actual
    if venta.caja.usuario != request.user:
        messages.error(request, 'No tienes permisos para ver esta venta.')
        return redirect('historial_ventas')
    
    return render(request, "facturacion/detalle_venta.html", {
        'venta': venta,
        'detalles': venta.detalles.all()
    })

def listadecliente(request):
    return render(request, "facturacion/listadecliente.html")


@require_GET
def obtener_clientes(request):
    try:
        # Obtener todos los clientes activos
        clientes = Cliente.objects.filter(status=True).values(
            'id', 'full_name', 'identification_number', 
            'address', 'primary_phone', 'secondary_phone', 
            'credit_limit', 'fecha_registro'   # 👈 corregido
        )
        
        # Convertir a lista y formatear fechas
        clientes_list = list(clientes)
        for cliente in clientes_list:
            cliente['fecha_registro'] = cliente['fecha_registro'].isoformat()
        
        return JsonResponse({
            'success': True,
            'clientes': clientes_list
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener clientes: {str(e)}'
        })



@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_cliente(request, cliente_id):
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        
        # En lugar de eliminar físicamente, cambiamos el estado
        cliente.status = False
        cliente.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cliente eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar cliente: {str(e)}'
        })

@csrf_exempt
@require_POST
def editar_cliente(request, cliente_id):
    try:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        data = json.loads(request.body)
        
        # Validar campos requeridos
        campos_requeridos = ['fullName', 'identificationNumber', 'address', 'primaryPhone']
        for campo in campos_requeridos:
            if campo not in data or not data[campo].strip():
                return JsonResponse({
                    'success': False,
                    'message': f'El campo {campo} es requerido'
                })
        
        # Verificar si ya existe otro cliente con el mismo número de identificación
        if Cliente.objects.filter(identification_number=data['identificationNumber']).exclude(id=cliente_id).exists():
            return JsonResponse({
                'success': False,
                'message': 'Ya existe otro cliente con este número de identificación'
            })
        
        # Actualizar los datos del cliente
        cliente.full_name = data['fullName']
        cliente.identification_number = data['identificationNumber']
        cliente.address = data['address']
        cliente.primary_phone = data['primaryPhone']
        cliente.secondary_phone = data.get('secondaryPhone', '')
        cliente.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cliente actualizado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al editar cliente: {str(e)}'
        })











def registrodecliente(request):
    return render(request, "facturacion/registrodecliente.html")


@csrf_exempt
@require_POST
def guardar_cliente(request):
    try:
        # Parsear los datos JSON recibidos
        data = json.loads(request.body)
        
        # Validar campos requeridos
        campos_requeridos = ['fullName', 'identificationNumber', 'address', 'primaryPhone']
        for campo in campos_requeridos:
            if campo not in data or not data[campo].strip():
                return JsonResponse({
                    'success': False,
                    'message': f'El campo {campo} es requerido'
                })
        
        # Verificar si ya existe un cliente con el mismo número de identificación
        if Cliente.objects.filter(identification_number=data['identificationNumber']).exists():
            return JsonResponse({
                'success': False,
                'message': 'Ya existe un cliente con este número de identificación'
            })
        
        # Procesar el límite de crédito (valor por defecto 0 si no se proporciona)
        credit_limit = data.get('creditLimit', '0')
        try:
            credit_limit = Decimal(credit_limit)
        except (InvalidOperation, ValueError):
            credit_limit = Decimal('0')
        
        # Crear y guardar el nuevo cliente
        cliente = Cliente(
            full_name=data['fullName'],
            identification_number=data['identificationNumber'],
            address=data['address'],
            primary_phone=data['primaryPhone'],
            secondary_phone=data.get('secondaryPhone', ''),
            credit_limit=credit_limit
        )
        cliente.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cliente registrado exitosamente',
            'client_id': cliente.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en el servidor: {str(e)}'
        })


@csrf_exempt
def obtener_datos_entrada(request, entrada_id):
    """Obtiene datos de una entrada existente para autocompletar el formulario"""
    if request.method == 'GET':
        try:
            entrada = EntradaProducto.objects.get(id=entrada_id)
            data = {
                'success': True,
                'entrada': {
                    'marca': entrada.marca,
                    'modelo': entrada.modelo,
                    'capacidad': entrada.capacidad or '',
                    'costo_compra': float(entrada.costo_compra),
                    'costo_venta': float(entrada.costo_venta),
                    'color': entrada.color or '',
                    'estado': entrada.estado or '',
                    'porcentaje_itbis': float(entrada.porcentaje_itbis),
                    'nombre_producto': entrada.nombre_producto
                }
            }
            return JsonResponse(data)
        except EntradaProducto.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Entrada no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@require_POST
@csrf_exempt
def agregar_nuevo_producto(request):
    """Crea una nueva plantilla de producto con datos mínimos para el modal"""
    if request.method == 'POST':
        try:
            nombre = request.POST.get('newProductName', '').strip()
            marca = request.POST.get('newProductBrand', '').strip()
            
            if not nombre:
                return JsonResponse({'success': False, 'error': 'El nombre del producto es requerido'})
            
            if not marca:
                return JsonResponse({'success': False, 'error': 'La marca es requerida'})
            
            # Verificar si ya existe una plantilla similar
            existe = EntradaProducto.objects.filter(
                nombre_producto__iexact=nombre,
                marca=marca,
                es_producto_base=True,
                activo=True
            ).exists()
            
            if existe:
                return JsonResponse({
                    'success': False, 
                    'error': 'Ya existe una plantilla con este nombre y marca'
                })
            
            # Obtener un proveedor por defecto para plantillas
            try:
                proveedor_default = Proveedor.objects.filter(activo=True).first()
                if not proveedor_default:
                    proveedor_default = Proveedor.objects.create(
                        nombre_empresa="Proveedor General",
                        contacto="Contacto general",
                        telefono="000-000-0000",
                        activo=True
                    )
            except Exception:
                proveedor_default = Proveedor.objects.create(
                    nombre_empresa="Proveedor General",
                    contacto="Contacto general",
                    telefono="000-000-0000",
                    activo=True
                )
            
            # Crear la plantilla de producto (solo datos base)
            nueva_plantilla = EntradaProducto(
                numero_factura=f"PLANTILLA-{int(time.time())}",
                fecha_entrada=timezone.now().date(),
                proveedor=proveedor_default,
                nombre_producto=nombre,
                marca=marca,
                modelo=nombre,  # Usar el nombre como modelo inicial
                capacidad="128",
                imei_serial=f"PLANTILLA-{int(time.time())}",
                estado="nuevo",
                color="negro",
                cantidad=1,
                cantidad_minima=2,
                costo_compra=0.00,
                porcentaje_itbis=18.00,
                costo_venta=0.00,
                observaciones="Plantilla creada mediante modal rápido",
                activo=True,
                es_producto_base=True  # Marcar como plantilla
            )
            
            nueva_plantilla.save()
            
            return JsonResponse({
                'success': True,
                'plantilla_id': nueva_plantilla.id,
                'nombre_producto': nueva_plantilla.nombre_producto,
                'marca': nueva_plantilla.get_marca_display(),
                'marca_valor': nueva_plantilla.marca,
                'mensaje': 'Plantilla creada exitosamente. Complete los detalles en el formulario.'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error al crear la plantilla: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def obtener_productos_disponibles(request):
    """Obtiene plantillas de productos para el dropdown"""
    try:
        # Obtener solo plantillas (productos base)
        plantillas = EntradaProducto.objects.filter(
            es_producto_base=True, 
            activo=True
        ).order_by('nombre_producto', 'marca', 'modelo')
        
        plantillas_data = []
        
        for plantilla in plantillas:
            plantillas_data.append({
                'id': plantilla.id,
                'texto_completo': f"{plantilla.nombre_producto} - {plantilla.get_marca_display()} - {plantilla.modelo}",
                'nombre_producto': plantilla.nombre_producto,
                'marca': plantilla.marca,
                'marca_display': plantilla.get_marca_display(),
                'modelo': plantilla.modelo,
                'capacidad': plantilla.capacidad or '128',
                'estado': plantilla.estado or 'nuevo',
                'color': plantilla.color or 'negro',
                'costo_compra': float(plantilla.costo_compra),
                'costo_venta': float(plantilla.costo_venta)
            })
        
        return JsonResponse({'success': True, 'plantillas': plantillas_data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def obtener_datos_plantilla(request, plantilla_id):
    """Obtiene datos de una plantilla para autocompletar campos"""
    if request.method == 'GET':
        try:
            plantilla = EntradaProducto.objects.get(id=plantilla_id, es_producto_base=True, activo=True)
            data = {
                'success': True,
                'data': {
                    'marca': plantilla.marca,
                    'modelo': plantilla.modelo,
                    'capacidad': plantilla.capacidad or '',
                    'estado': plantilla.estado or '',
                    'color': plantilla.color or '',
                    'costo_compra': float(plantilla.costo_compra),
                    'costo_venta': float(plantilla.costo_venta)
                }
            }
            return JsonResponse(data)
        except EntradaProducto.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Plantilla no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})




def entrada(request):
    """Vista principal para registro de entradas de productos"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            numero_factura = request.POST.get('numero_factura', '').strip()
            fecha_entrada = request.POST.get('fecha_entrada', '')
            proveedor_id = request.POST.get('proveedor', '')
            ncf = request.POST.get('ncf', '').strip()
            nombre_producto = request.POST.get('nombre_producto', '').strip()  # ✅ AQUÍ ESTÁ EL CAMPO FALTANTE
            marca = request.POST.get('marca', '').strip()
            modelo = request.POST.get('modelo', '').strip()
            capacidad = request.POST.get('capacidad', '')
            imei_serial = request.POST.get('imei_serial', '').strip()
            estado = request.POST.get('estado', '')
            color = request.POST.get('color', '')
            
            # Manejar valores numéricos
            try:
                cantidad = int(request.POST.get('cantidad', 1))
            except (ValueError, TypeError):
                cantidad = 1
                
            try:
                costo_compra = float(request.POST.get('costo_compra', 0))
            except (ValueError, TypeError):
                costo_compra = 0.0
                
            try:
                porcentaje_itbis = float(request.POST.get('porcentaje_itbis', 18))
            except (ValueError, TypeError):
                porcentaje_itbis = 18.0
                
            try:
                costo_venta = float(request.POST.get('costo_venta', 0))
            except (ValueError, TypeError):
                costo_venta = 0.0
                
            observaciones = request.POST.get('observaciones', '').strip()
            
            # Validaciones básicas
            required_fields = [
                ('numero_factura', numero_factura, 'Número de factura'),
                ('fecha_entrada', fecha_entrada, 'Fecha de entrada'),
                ('proveedor', proveedor_id, 'Proveedor'),
                ('nombre_producto', nombre_producto, 'Nombre del producto'),  # ✅ AGREGAR ESTA VALIDACIÓN
                ('marca', marca, 'Marca'),
                ('modelo', modelo, 'Modelo'),
                ('imei_serial', imei_serial, 'IMEI/Serial'),
                ('estado', estado, 'Estado'),
                ('cantidad', cantidad, 'Cantidad'),
                ('costo_compra', costo_compra, 'Costo de compra'),
                ('costo_venta', costo_venta, 'Costo de venta')
            ]
            
            for field_name, field_value, field_display in required_fields:
                if not field_value:
                    messages.error(request, f'{field_display} es requerido')
                    return redirect('entrada')
            
            if cantidad <= 0:
                messages.error(request, 'La cantidad debe ser mayor a 0')
                return redirect('entrada')
                
            if costo_compra <= 0:
                messages.error(request, 'El costo de compra debe ser mayor a 0')
                return redirect('entrada')
                
            if costo_venta <= 0:
                messages.error(request, 'El costo de venta debe ser mayor a 0')
                return redirect('entrada')
            
            # Verificar si el IMEI ya existe
            if EntradaProducto.objects.filter(
                imei_serial=imei_serial, 
                activo=True
            ).exists():
                messages.error(request, 'El IMEI/Serial ya existe en la base de datos')
                return redirect('entrada')
            
            # Verificar si el número de factura ya existe
            if EntradaProducto.objects.filter(
                numero_factura=numero_factura, 
                activo=True
            ).exists():
                messages.error(request, 'El número de factura ya existe en la base de datos')
                return redirect('entrada')
            
            # Obtener el proveedor
            try:
                proveedor = Proveedor.objects.get(id=proveedor_id, activo=True)
            except Proveedor.DoesNotExist:
                messages.error(request, 'Proveedor no válido')
                return redirect('entrada')
            
            # Calcular montos automáticamente
            monto_itbis = (costo_compra * porcentaje_itbis) / 100
            costo_total = costo_compra + monto_itbis
            
            # Crear la entrada de producto
            entrada_producto = EntradaProducto(
                numero_factura=numero_factura,
                fecha_entrada=fecha_entrada,
                proveedor=proveedor,
                ncf=ncf,
                nombre_producto=nombre_producto,  # ✅ AHORA SÍ ESTÁ DEFINIDO
                marca=marca,
                modelo=modelo,
                capacidad=capacidad,
                imei_serial=imei_serial,
                estado=estado,
                color=color,
                cantidad=cantidad,
                cantidad_minima=2,
                costo_compra=costo_compra,
                porcentaje_itbis=porcentaje_itbis,
                monto_itbis=monto_itbis,
                costo_total=costo_total,
                costo_venta=costo_venta,
                observaciones=observaciones,
                activo=True
            )
            
            entrada_producto.save()
            
            messages.success(request, '✅ Producto registrado exitosamente en el inventario')
            return redirect('entrada')
            
        except ValueError as e:
            messages.error(request, f'Error en los datos numéricos: {str(e)}')
            return redirect('entrada')
        except Exception as e:
            messages.error(request, f'Error al registrar el producto: {str(e)}')
            return redirect('entrada')
    
    # GET request - mostrar el formulario
    proveedores = Proveedor.objects.filter(activo=True)
    
    # Establecer fecha actual por defecto
    fecha_actual = timezone.now().date().isoformat()
    
    return render(request, 'facturacion/entrada.html', {
        'proveedores': proveedores,
        'fecha_actual': fecha_actual
    })


@csrf_exempt
def buscar_productos_similares(request):
    """Busca productos similares para autocompletar"""
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return JsonResponse({'success': True, 'productos': []})
        
        try:
            # Buscar productos similares por NOMBRE o marca
            productos = EntradaProducto.objects.filter(
                Q(nombre_producto__icontains=query) | Q(marca__icontains=query),
                activo=True
            ).distinct().order_by('marca', 'nombre_producto')[:10]
            
            resultados = []
            for producto in productos:
                resultados.append({
                    'marca': producto.marca,
                    'marca_display': producto.get_marca_display(),
                    'modelo': producto.modelo,
                    'nombre_producto': producto.nombre_producto,  # ✅ AÑADIR ESTA LÍNEA
                    'capacidad': producto.capacidad or '',
                    'estado': producto.estado or '',
                    'color': producto.color or '',
                    'costo_compra': float(producto.costo_compra),
                    'costo_venta': float(producto.costo_venta)
                })
            
            return JsonResponse({'success': True, 'productos': resultados})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def cuentaporcobrar(request):
    return render(request, "facturacion/cuentaporcobrar.html")

def gestiondesuplidores(request):
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    paises = Proveedor.PAIS_CHOICES
    categorias = Proveedor.CATEGORIA_CHOICES
    terminos_pago = Proveedor.TERMINOS_PAGO_CHOICES
    
    context = {
        'proveedores': proveedores,
        'paises': paises,
        'categorias': categorias,
        'terminos_pago': terminos_pago,
    }
    return render(request, "facturacion/gestiondesuplidores.html", context)

def agregar_proveedor(request):
    if request.method == 'POST':
        try:
            Proveedor.objects.create(
                nombre_empresa=request.POST.get('companyName'),
                rnc=request.POST.get('rnc'),
                nombre_contacto=request.POST.get('contactName'),
                email=request.POST.get('email'),
                telefono=request.POST.get('phone'),
                whatsapp=request.POST.get('whatsapp', ''),
                pais=request.POST.get('country'),
                ciudad=request.POST.get('city'),
                categoria=request.POST.get('category'),
                direccion=request.POST.get('address', ''),
                terminos_pago=request.POST.get('paymentTerms', ''),
                limite_credito=request.POST.get('creditLimit', 0) or 0,
                notas=request.POST.get('notes', ''),
                activo=request.POST.get('isActive') == 'on'
            )
            messages.success(request, 'Proveedor agregado exitosamente')
            return redirect('gestiondesuplidores')
        except Exception as e:
            messages.error(request, f'Error al agregar proveedor: {str(e)}')
            return redirect('gestiondesuplidores')
    
    return redirect('gestiondesuplidores')

def editar_proveedor(request):
    if request.method == 'POST':
        try:
            proveedor = get_object_or_404(Proveedor, id=request.POST.get('supplierId'))
            proveedor.nombre_empresa = request.POST.get('companyName')
            proveedor.rnc = request.POST.get('rnc')
            proveedor.nombre_contacto = request.POST.get('contactName')
            proveedor.email = request.POST.get('email')
            proveedor.telefono = request.POST.get('phone')
            proveedor.whatsapp = request.POST.get('whatsapp', '')
            proveedor.pais = request.POST.get('country')
            proveedor.ciudad = request.POST.get('city')
            proveedor.categoria = request.POST.get('category')
            proveedor.direccion = request.POST.get('address', '')
            proveedor.terminos_pago = request.POST.get('paymentTerms', '')
            proveedor.limite_credito = request.POST.get('creditLimit', 0) or 0
            proveedor.notas = request.POST.get('notes', '')
            proveedor.activo = request.POST.get('isActive') == 'on'
            proveedor.save()
            
            messages.success(request, 'Proveedor actualizado exitosamente')
            return redirect('gestiondesuplidores')
        except Exception as e:
            messages.error(request, f'Error al actualizar proveedor: {str(e)}')
            return redirect('gestiondesuplidores')
    
    return redirect('gestiondesuplidores')

@require_POST
def eliminar_proveedor(request):
    try:
        proveedor = get_object_or_404(Proveedor, id=request.POST.get('supplierId'))
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente')
    except Exception as e:
        messages.error(request, f'Error al eliminar proveedor: {str(e)}')
    
    return redirect('gestiondesuplidores')

def get_proveedor_data(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    data = {
        'id': proveedor.id,
        'nombre_empresa': proveedor.nombre_empresa,
        'rnc': proveedor.rnc,
        'nombre_contacto': proveedor.nombre_contacto,
        'email': proveedor.email,
        'telefono': proveedor.telefono,
        'whatsapp': proveedor.whatsapp or '',
        'pais': proveedor.pais,
        'ciudad': proveedor.ciudad,
        'categoria': proveedor.categoria,
        'direccion': proveedor.direccion or '',
        'terminos_pago': proveedor.terminos_pago or '',
        'limite_credito': str(proveedor.limite_credito),
        'notas': proveedor.notas or '',
        'activo': proveedor.activo
    }
    return JsonResponse(data)

def registrosuplidores(request):
    if request.method == 'POST':
        # Crear el proveedor directamente desde los datos del request
        try:
            proveedor = Proveedor(
                nombre_empresa=request.POST.get('nombre_empresa'),
                rnc=request.POST.get('rnc'),
                nombre_contacto=request.POST.get('nombre_contacto'),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono'),
                whatsapp=request.POST.get('whatsapp', ''),  # Campo opcional
                pais=request.POST.get('pais'),
                ciudad=request.POST.get('ciudad'),
                categoria=request.POST.get('categoria'),
                direccion=request.POST.get('direccion', ''),  # Campo opcional
                terminos_pago=request.POST.get('terminos_pago', ''),  # Campo opcional
                limite_credito=request.POST.get('limite_credito', 0) or 0,  # Valor por defecto 0
                notas=request.POST.get('notas', ''),  # Campo opcional
                activo=request.POST.get('activo') == 'on'  # Checkbox
            )
            proveedor.full_clean()  # Validar los datos según las reglas del modelo
            proveedor.save()
            messages.success(request, 'Suplidor registrado exitosamente')
            return redirect('registrosuplidores')
            
        except Exception as e:
            # Manejar errores de validación
            messages.error(request, f'Error al registrar el suplidor: {str(e)}')
            # Pasar los valores ingresados de vuelta al template para mantenerlos en el formulario
            context = {
                'valores': request.POST,
                'error': str(e)
            }
            return render(request, "facturacion/registrosuplidores.html", context)
    
    # Si es GET, mostrar el formulario vacío
    return render(request, "facturacion/registrosuplidores.html")