from django.shortcuts import render, redirect, get_object_or_404 
from .models import EntradaProducto, Proveedor,  Cliente, Caja, Venta, DetalleVenta, MovimientoStock, CuentaPorCobrar, PagoCuentaPorCobrar, CierreCaja, ComprobantePago
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
from django.db.models import Sum, Q, F
from datetime import datetime, timedelta
import pandas as pd
from decimal import Decimal, InvalidOperation
import logging

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group, Permission
import csv
from reportlab.pdfgen import canvas

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

# @csrf_exempt
# @require_POST
# @transaction.atomic
# def procesar_venta(request):
#     try:
#         data = request.POST
#         user = request.user
        
#         # Función segura para conversión a Decimal
#         def safe_decimal(value, default=0):
#             if value is None or value == '':
#                 return Decimal(default)
#             try:
#                 return Decimal(str(value).replace(',', '.'))
#             except (InvalidOperation, ValueError):
#                 return Decimal(default)
        
#         # Convertir valores
#         payment_type = data.get('payment_type', 'contado')
#         payment_method = data.get('payment_method', 'efectivo')
#         subtotal = safe_decimal(data.get('subtotal', 0))
#         discount_percentage = safe_decimal(data.get('discount_percentage', 0))
#         discount_amount = safe_decimal(data.get('discount_amount', 0))
#         total = safe_decimal(data.get('total', 0))
#         cash_received = safe_decimal(data.get('cash_received', 0))
#         change_amount = safe_decimal(data.get('change_amount', 0))
        
#         # Validaciones
#         if payment_type not in ['contado', 'credito']:
#             return JsonResponse({'success': False, 'message': 'Tipo de pago inválido'})
        
#         if payment_method not in ['efectivo', 'tarjeta', 'transferencia']:
#             return JsonResponse({'success': False, 'message': 'Método de pago inválido'})
        
#         # Procesar información del cliente
#         client_id = data.get('client_id')
#         client_name = data.get('client_name', '').strip()
#         client_document = data.get('client_document', '').strip()
        
#         cliente = None
#         if payment_type == 'credito':
#             if not client_id:
#                 return JsonResponse({'success': False, 'message': 'Debe seleccionar un cliente para ventas a crédito'})
            
#             try:
#                 cliente = Cliente.objects.get(id=client_id, status=True)
#                 if total > cliente.credit_limit:
#                     return JsonResponse({
#                         'success': False, 
#                         'message': f'El monto excede el límite de crédito del cliente (RD${cliente.credit_limit})'
#                     })
#             except Cliente.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': 'Cliente no válido'})
#         else:
#             if not client_name:
#                 return JsonResponse({'success': False, 'message': 'Debe ingresar el nombre del cliente'})
        
#         # Procesar items de la venta
#         sale_items_json = data.get('sale_items')
#         if not sale_items_json:
#             return JsonResponse({'success': False, 'message': 'No hay productos en la venta'})
        
#         sale_items = json.loads(sale_items_json)
#         if not sale_items:
#             return JsonResponse({'success': False, 'message': 'No hay productos en la venta'})
        
#         # Verificar stock antes de procesar la venta
#         for item in sale_items:
#             try:
#                 producto = EntradaProducto.objects.get(id=item['productId'], activo=True)
#                 cantidad_solicitada = int(item['quantity'])
                
#                 if not producto.tiene_stock_suficiente(cantidad_solicitada):
#                     return JsonResponse({
#                         'success': False, 
#                         'message': f'Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.cantidad}'
#                     })
#             except EntradaProducto.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': f'Producto no encontrado: {item.get("name", "Desconocido")}'})
#             except (ValueError, KeyError):
#                 return JsonResponse({'success': False, 'message': f'Cantidad inválida para producto: {item.get("name", "Desconocido")}'})
        
#         # Crear la venta
#         venta = Venta(
#             vendedor=user,
#             cliente=cliente,
#             cliente_nombre=client_name,
#             cliente_documento=client_document,
#             tipo_venta=payment_type,
#             metodo_pago=payment_method,
#             subtotal=subtotal,
#             descuento_porcentaje=discount_percentage,
#             descuento_monto=discount_amount,
#             total=total,
#             efectivo_recibido=cash_received,
#             cambio=change_amount,
#             completada=True
#         )
#         venta.save()
        
#         # Procesar detalles de venta y descontar stock
#         for item in sale_items:
#             producto = EntradaProducto.objects.get(id=item['productId'])
#             cantidad = int(item['quantity'])
#             precio_unitario = safe_decimal(item['price'])
            
#             # Descontar stock con manejo de error por si no existe el método
#             try:
#                 if not producto.restar_stock(
#                     cantidad=cantidad,
#                     usuario=user,
#                     motivo="Venta",
#                     referencia=venta.numero_factura
#                 ):
#                     raise Exception(f'Error al procesar stock para {producto.nombre_producto}')
#             except AttributeError:
#                 # Si el método registrar_movimiento_stock no existe, usar versión simple
#                 if not producto.tiene_stock_suficiente(cantidad):
#                     raise Exception(f'Stock insuficiente para {producto.nombre_producto}')
                
#                 cantidad_anterior = producto.cantidad
#                 producto.cantidad -= cantidad
#                 producto.save(update_fields=['cantidad'])
                
#                 print(f"Stock actualizado (método simple): {producto.nombre_producto} -{cantidad} unidades")
            
#             # Crear detalle de venta
#             detalle = DetalleVenta(
#                 venta=venta,
#                 producto=producto,
#                 cantidad=cantidad,
#                 precio_unitario=precio_unitario,
#                 subtotal=safe_decimal(item['subtotal'])
#             )
#             detalle.save()
        
#         return JsonResponse({
#             'success': True, 
#             'message': 'Venta procesada correctamente',
#             'venta_id': venta.id,
#             'numero_factura': venta.numero_factura
#         })
        
#     except Exception as e:
#         transaction.set_rollback(True)
#         return JsonResponse({'success': False, 'message': f'Error al procesar la venta: {str(e)}'})

def safe_decimal(value, default=0):
    """
    Convierte de forma segura un valor a Decimal.
    Maneja strings, números, y valores nulos/vacíos.
    """
    if value is None or value == '':
        return Decimal(default)
    
    try:
        # Convertir a string y reemplazar comas por puntos
        value_str = str(value).strip().replace(',', '.')
        # Eliminar caracteres no numéricos excepto punto y signo negativo
        value_str = ''.join(c for c in value_str if c.isdigit() or c in ['.', '-'])
        return Decimal(value_str)
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)

def safe_int(value, default=0):
    """
    Convierte de forma segura un valor a entero.
    Maneja strings vacíos, None, y valores inválidos.
    """
    if value is None:
        return default
    
    if isinstance(value, int):
        return value
    
    if isinstance(value, float):
        return int(value)
    
    value_str = str(value).strip()
    if not value_str:
        return default
    
    try:
        # Eliminar caracteres no numéricos excepto signo negativo
        cleaned_str = ''.join(c for c in value_str if c.isdigit() or c == '-')
        if cleaned_str and cleaned_str != '-':
            return int(cleaned_str)
        return default
    except (ValueError, TypeError):
        return default



def safe_decimal(value, default=0):
    """
    Convierte de forma segura un valor a Decimal.
    Maneja strings, números, y valores nulos/vacíos.
    """
    if value is None or value == '':
        return Decimal(default)
    
    try:
        # Convertir a string y reemplazar comas por puntos
        value_str = str(value).strip().replace(',', '.')
        # Eliminar caracteres no numéricos excepto punto y signo negativo
        value_str = ''.join(c for c in value_str if c.isdigit() or c in ['.', '-'])
        return Decimal(value_str)
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)

def safe_int(value, default=0):
    """
    Convierte de forma segura un valor a entero.
    Maneja strings vacíos, None, y valores inválidos.
    """
    if value is None:
        return default
    
    if isinstance(value, int):
        return value
    
    if isinstance(value, float):
        return int(value)
    
    value_str = str(value).strip()
    if not value_str:
        return default
    
    try:
        # Eliminar caracteres no numéricos excepto signo negativo
        cleaned_str = ''.join(c for c in value_str if c.isdigit() or c == '-')
        if cleaned_str and cleaned_str != '-':
            return int(cleaned_str)
        return default
    except (ValueError, TypeError):
        return default



@csrf_exempt
@require_POST
@transaction.atomic
@login_required
def procesar_venta(request):
    try:
        data = request.POST
        user = request.user
        
        # Validar que hay datos
        if not data:
            return JsonResponse({'success': False, 'message': 'No se recibieron datos'})
        
        # Convertir valores usando safe_decimal y safe_int
        payment_type = data.get('payment_type', 'contado')
        payment_method = data.get('payment_method', 'efectivo')
        subtotal = safe_decimal(data.get('subtotal', 0))
        discount_percentage = safe_decimal(data.get('discount_percentage', 0))
        discount_amount = safe_decimal(data.get('discount_amount', 0))
        total = safe_decimal(data.get('total', 0))
        cash_received = safe_decimal(data.get('cash_received', 0))
        change_amount = safe_decimal(data.get('change_amount', 0))
        
        # Campos de financiamiento - usar safe_int para enteros
        plazo_meses = safe_int(data.get('plazo_meses', 0))
        monto_inicial = safe_decimal(data.get('monto_inicial', 0))
        tasa_interes = safe_decimal(data.get('tasa_interes', 0))
        monto_financiado = safe_decimal(data.get('monto_financiado', 0))
        interes_mensual = safe_decimal(data.get('interes_mensual', 0))
        cuota_mensual = safe_decimal(data.get('cuota_mensual', 0))
        ganancia_interes = safe_decimal(data.get('ganancia_interes', 0))
        total_con_interes = safe_decimal(data.get('total_con_interes', 0))
        total_a_pagar = safe_decimal(data.get('total_a_pagar', 0))
        
        # Para ventas a contado, resetear campos de crédito
        if payment_type != 'credito':
            plazo_meses = 0
            monto_inicial = 0
            tasa_interes = 0
            monto_financiado = 0
            interes_mensual = 0
            cuota_mensual = 0
            ganancia_interes = 0
            total_con_interes = 0
            total_a_pagar = total  # Usar el total normal
        
        # Validaciones
        if payment_type not in ['contado', 'credito']:
            return JsonResponse({'success': False, 'message': 'Tipo de pago inválido'})
        
        if payment_method not in ['efectivo', 'tarjeta', 'transferencia']:
            return JsonResponse({'success': False, 'message': 'Método de pago inválido'})
        
        if subtotal <= 0:
            return JsonResponse({'success': False, 'message': 'El subtotal debe ser mayor a 0'})
        
        if total <= 0:
            return JsonResponse({'success': False, 'message': 'El total debe ser mayor a 0'})
        
        # Validaciones específicas para crédito
        if payment_type == 'credito':
            if plazo_meses <= 0:
                return JsonResponse({'success': False, 'message': 'El plazo debe ser mayor a 0'})
            if tasa_interes < 0:
                return JsonResponse({'success': False, 'message': 'La tasa de interés no puede ser negativa'})
            if monto_inicial < 0:
                return JsonResponse({'success': False, 'message': 'El monto inicial no puede ser negativo'})
        
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
                
                # Validar límite de crédito
                total_a_validar = total_a_pagar if total_a_pagar > 0 else total
                
                if total_a_validar > cliente.credit_limit:
                    return JsonResponse({
                        'success': False, 
                        'message': f'El monto excede el límite de crédito del cliente. Límite: RD${cliente.credit_limit}, Solicitado: RD${total_a_validar}'
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
                producto = EntradaProducto.objects.get(id=item['id'], activo=True)
                cantidad_solicitada = int(item['quantity'])
                
                if producto.cantidad < cantidad_solicitada:
                    return JsonResponse({
                        'success': False, 
                        'message': f'Stock insuficiente para {producto.nombre_producto}. Disponible: {producto.cantidad}'
                    })
            except EntradaProducto.DoesNotExist:
                return JsonResponse({'success': False, 'message': f'Producto no encontrado: {item.get("name", "Desconocido")}'})
            except (ValueError, KeyError):
                return JsonResponse({'success': False, 'message': f'Cantidad inválida para producto: {item.get("name", "Desconocido")}'})
        
        # Determinar si es financiada
        es_financiada = payment_type == 'credito' and monto_financiado > 0
        
        # Usar el total con interés si es financiada, de lo contrario usar el total normal
        total_final = total_con_interes if es_financiada and total_con_interes > 0 else total
        
        # Crear la venta con todos los campos
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
            total=total_final,
            montoinicial=monto_inicial,
            efectivo_recibido=cash_received,
            cambio=change_amount,
            completada=True,
            fecha_venta=timezone.now(),
            # Campos de financiamiento
            es_financiada=es_financiada,
            tasa_interes=tasa_interes,
            plazo_meses=plazo_meses,
            monto_financiado=monto_financiado,
            interes_total=ganancia_interes,
            cuota_mensual=cuota_mensual,
            total_con_interes=total_con_interes,
            total_a_pagar=total_a_pagar if payment_type == 'credito' else total_final
        )
        
        # Guardar para generar número de factura
        venta.save()
        
        # Registrar en logs los valores guardados
        print(f"=== VENTA CREADA ===")
        print(f"Factura: {venta.numero_factura}")
        print(f"Subtotal: RD${venta.subtotal}")
        print(f"Descuento %: {venta.descuento_porcentaje}%")
        print(f"Descuento monto: RD${venta.descuento_monto}")
        print(f"Total: RD${venta.total}")
        print(f"Efectivo recibido: RD${venta.efectivo_recibido}")
        print(f"Cambio: RD${venta.cambio}")
        print(f"Tipo: {venta.tipo_venta}")
        print(f"Método: {venta.metodo_pago}")
        
        if es_financiada:
            print(f"=== FINANCIAMIENTO ===")
            print(f"Monto Inicial: RD${venta.montoinicial}")
            print(f"Tasa interés: {venta.tasa_interes}%")
            print(f"Plazo meses: {venta.plazo_meses}")
            print(f"Monto financiado: RD${venta.monto_financiado}")
            print(f"Interés mensual: RD${interes_mensual}")
            print(f"Cuota mensual: RD${venta.cuota_mensual}")
            print(f"Ganancia por interés: RD${venta.interes_total}")
            print(f"Total con interés: RD${venta.total_con_interes}")
            print(f"Total a pagar: RD${total_a_pagar}")
        
        # Procesar detalles de venta y descontar stock
        productos_para_cuenta = []
        for item in sale_items:
            try:
                producto = EntradaProducto.objects.get(id=item['id'])
                cantidad = int(item['quantity'])
                precio_unitario = safe_decimal(item['price'])
                subtotal_item = safe_decimal(item['subtotal'])
                
                # Validar que los cálculos sean consistentes
                calculated_subtotal = precio_unitario * cantidad
                if abs(calculated_subtotal - subtotal_item) > Decimal('0.01'):
                    print(f"Advertencia: Subtotal inconsistente para {producto.nombre_producto}")
                    print(f"Calculado: {calculated_subtotal}, Recibido: {subtotal_item}")
                    # Usar el valor calculado para consistencia
                    subtotal_item = calculated_subtotal
                
                # Descontar stock
                cantidad_anterior = producto.cantidad
                producto.cantidad -= cantidad
                producto.save(update_fields=['cantidad'])
                
                print(f"Stock actualizado: {producto.nombre_producto} -{cantidad} unidades ({cantidad_anterior} -> {producto.cantidad})")
                
                # Crear detalle de venta
                detalle = DetalleVenta(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal_item
                )
                detalle.save()
                
                # Agregar a lista para cuenta por cobrar
                productos_para_cuenta.append(f"{producto.nombre_producto} x{cantidad} - RD${precio_unitario:.2f}")
                
            except EntradaProducto.DoesNotExist:
                transaction.set_rollback(True)
                return JsonResponse({'success': False, 'message': f'Producto no encontrado: ID {item.get("id", "Desconocido")}'})
            except Exception as e:
                transaction.set_rollback(True)
                return JsonResponse({'success': False, 'message': f'Error al procesar producto: {str(e)}'})
        
        # Crear cuenta por cobrar si es venta a crédito
        if payment_type == 'credito' and cliente:
            try:
                fecha_vencimiento = timezone.now().date() + timedelta(days=30)
                
                # Crear string con los productos
                productos_str = "\n".join(productos_para_cuenta)
                
                # Información adicional para financiamiento
                info_financiamiento = ""
                if es_financiada:
                    info_financiamiento = f"""
FINANCIAMIENTO:
- Monto Inicial: RD${monto_inicial:.2f}
- Tasa de interés: {tasa_interes}% mensual
- Plazo: {plazo_meses} meses
- Monto a Financiar: RD${monto_financiado:.2f}
- Interés Mensual: RD${interes_mensual:.2f}
- Cuota mensual: RD${cuota_mensual:.2f}
- Ganancia por Interés: RD${ganancia_interes:.2f}
- Total con Interés: RD${total_con_interes:.2f}
- Total a Pagar: RD${total_a_pagar:.2f}
"""
                
                cuenta_por_cobrar = CuentaPorCobrar(
                    venta=venta,
                    cliente=cliente,
                    monto_total=total_final,
                    monto_pagado=monto_inicial,  # El pago inicial ya se hizo
                    fecha_vencimiento=fecha_vencimiento,
                    productos=productos_str,
                    estado='pendiente',
                    observaciones=f"""Venta a crédito - Factura: {venta.numero_factura}
Cliente: {cliente.full_name}
Productos:
{productos_str}
{info_financiamiento}"""
                )
                cuenta_por_cobrar.save()
                
                print(f"Cuenta por cobrar creada exitosamente: {cuenta_por_cobrar.id}")
                print(f"Monto total: RD${cuenta_por_cobrar.monto_total}")
                print(f"Monto pagado: RD${cuenta_por_cobrar.monto_pagado}")
                print(f"Saldo pendiente: RD${cuenta_por_cobrar.saldo_pendiente}")
                print(f"Productos incluidos:\n{productos_str}")
                
            except Exception as e:
                transaction.set_rollback(True)
                return JsonResponse({'success': False, 'message': f'Error al crear cuenta por cobrar: {str(e)}'})
        
        # Validar que los totales sean consistentes
        venta_refreshed = Venta.objects.get(id=venta.id)
        detalles_total = sum(detalle.subtotal for detalle in venta_refreshed.detalles.all())
        calculated_total = detalles_total - venta_refreshed.descuento_monto

        if abs(venta_refreshed.total - calculated_total) > Decimal('0.01') and not es_financiada:
            print(f"Advertencia: Total inconsistente en venta {venta.numero_factura}")
            print(f"Total guardado: RD${venta_refreshed.total}")
            print(f"Total calculado: RD${calculated_total}")
            # Corregir automáticamente solo si no es financiada
            venta_refreshed.total = calculated_total
            venta_refreshed.save(update_fields=['total'])
            print(f"Total corregido: RD${venta_refreshed.total}")
        
        return JsonResponse({
            'success': True, 
            'message': 'Venta procesada correctamente',
            'venta_id': venta.id,
            'numero_factura': venta.numero_factura,
            'detalles': {
                'subtotal': float(venta.subtotal),
                'descuento_porcentaje': float(venta.descuento_porcentaje),
                'descuento_monto': float(venta.descuento_monto),
                'total': float(venta.total),
                'efectivo_recibido': float(venta.efectivo_recibido),
                'cambio': float(venta.cambio),
                'items_count': len(sale_items),
                'es_financiada': venta.es_financiada,
                'monto_inicial': float(venta.montoinicial),
                'tasa_interes': float(venta.tasa_interes),
                'plazo_meses': venta.plazo_meses,
                'monto_financiado': float(venta.monto_financiado),
                'interes_total': float(venta.interes_total),
                'cuota_mensual': float(venta.cuota_mensual),
                'total_con_interes': float(venta.total_con_interes)
            }
        })
        
    except Exception as e:
        transaction.set_rollback(True)
        import traceback
        print(f"Error completo: {traceback.format_exc()}")
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
    
    # Calcular total de artículos
    total_articulos = sum(detalle.cantidad for detalle in detalles)
    
    # Renderizar el template HTML
    return render(request, 'facturacion/comprobante_venta.html', {
        'venta': venta,
        'detalles': detalles,
        'total_articulos': total_articulos,
        'now': timezone.now().strftime('%d/%m/%Y')  # Fecha actual formateada
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
    # Obtener parámetros de filtrado
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Filtrar cuentas por cobrar (excluir anuladas)
    cuentas = CuentaPorCobrar.objects.select_related('venta', 'cliente').filter(anulada=False)
    
    if search:
        cuentas = cuentas.filter(
            Q(cliente__full_name__icontains=search) |
            Q(venta__numero_factura__icontains=search) |
            Q(cliente__identification_number__icontains=search)
        )
    
    if status_filter:
        cuentas = cuentas.filter(estado=status_filter)
    
    if date_from:
        cuentas = cuentas.filter(venta__fecha_venta__gte=date_from)
    
    if date_to:
        cuentas = cuentas.filter(venta__fecha_venta__lte=date_to)
    
    # Calcular estadísticas usando monto_total (solo cuentas no anuladas)
    total_pendiente = cuentas.filter(estado__in=['pendiente', 'parcial']).aggregate(
        total=Sum(F('monto_total') - F('monto_pagado'))
    )['total'] or Decimal('0.00')
    
    total_vencido = cuentas.filter(estado='vencida').aggregate(
        total=Sum(F('monto_total') - F('monto_pagado'))
    )['total'] or Decimal('0.00')
    
    # Pagos del mes actual (solo de cuentas no anuladas)
    mes_actual = timezone.now().month
    año_actual = timezone.now().year
    pagos_mes = PagoCuentaPorCobrar.objects.filter(
        fecha_pago__month=mes_actual,
        fecha_pago__year=año_actual,
        cuenta__anulada=False
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    total_por_cobrar = cuentas.exclude(estado='pagada').aggregate(
        total=Sum(F('monto_total') - F('monto_pagado'))
    )['total'] or Decimal('0.00')
    
    # Preparar datos para el template
    cuentas_data = []
    for cuenta in cuentas:
        # Obtener productos de la venta
        productos = []
        
        # Primero intentar usar el campo productos (JSON) si existe
        if cuenta.productos:
            try:
                productos_json = json.loads(cuenta.productos)
                for producto in productos_json:
                    productos.append({
                        'nombre': producto.get('nombre', 'Producto'),
                        'cantidad': producto.get('cantidad', 1),
                        'precio': float(producto.get('precio', 0))
                    })
            except json.JSONDecodeError:
                # Si no es JSON válido, tratar como texto plano
                productos.append({
                    'nombre': cuenta.productos,
                    'cantidad': 1,
                    'precio': float(cuenta.monto_total)
                })
        else:
            # Si no hay productos en el campo, intentar obtener de la venta
            try:
                if cuenta.venta and hasattr(cuenta.venta, 'detalles'):
                    for detalle in cuenta.venta.detalles.all():
                        nombre_producto = 'Servicio'
                        if hasattr(detalle, 'producto') and detalle.producto:
                            nombre_producto = detalle.producto.nombre
                        elif hasattr(detalle, 'servicio') and detalle.servicio:
                            nombre_producto = detalle.servicio.nombre
                        elif hasattr(detalle, 'descripcion') and detalle.descripcion:
                            nombre_producto = detalle.descripcion
                        
                        precio = 0
                        if hasattr(detalle, 'precio'):
                            precio = float(detalle.precio)
                        elif hasattr(detalle, 'precio_unitario'):
                            precio = float(detalle.precio_unitario)
                        
                        cantidad = 1
                        if hasattr(detalle, 'cantidad'):
                            cantidad = float(detalle.cantidad)
                        
                        productos.append({
                            'nombre': nombre_producto,
                            'cantidad': cantidad,
                            'precio': precio
                        })
                else:
                    # Si no hay venta o detalles
                    productos.append({
                        'nombre': 'Producto/Servicio',
                        'cantidad': 1,
                        'precio': float(cuenta.monto_total)
                    })
            except Exception as e:
                # En caso de cualquier error
                productos.append({
                    'nombre': f'Error: {str(e)}',
                    'cantidad': 1,
                    'precio': float(cuenta.monto_total)
                })
        
        # Obtener información del cliente de manera segura
        client_name = 'Cliente no disponible'
        client_phone = 'N/A'
        
        if cuenta.cliente:
            client_name = cuenta.cliente.full_name or 'Cliente sin nombre'
            client_phone = cuenta.cliente.primary_phone or 'N/A'
        
        # Obtener información de la factura de manera segura
        invoice_number = 'N/A'
        sale_date = ''
        
        if cuenta.venta:
            invoice_number = cuenta.venta.numero_factura or 'N/A'
            if cuenta.venta.fecha_venta:
                sale_date = cuenta.venta.fecha_venta.strftime('%Y-%m-%d')
        
        # Obtener fecha de vencimiento
        due_date = ''
        if cuenta.fecha_vencimiento:
            due_date = cuenta.fecha_vencimiento.strftime('%Y-%m-%d')
        
        # USAR MONTO_TOTAL PARA TODOS LOS CÁLCULOS
        monto_total = float(cuenta.monto_total)
        monto_pagado = float(cuenta.monto_pagado)
        saldo_pendiente = monto_total - monto_pagado
        
        # Asegurarse de que el saldo pendiente no sea negativo
        if saldo_pendiente < 0:
            saldo_pendiente = 0
        
        cuentas_data.append({
            'id': cuenta.id,
            'invoiceNumber': invoice_number,
            'clientName': client_name,
            'clientPhone': client_phone,
            'products': productos,
            'saleDate': sale_date,
            'dueDate': due_date,
            'totalAmount': monto_total,  # Usar monto_total aquí
            'paidAmount': monto_pagado,
            'pendingBalance': saldo_pendiente,  # Calculado con monto_total
            'status': cuenta.estado,
            'observations': cuenta.observaciones or ''
        })
    
    # Convertir a JSON para pasarlo al template
    cuentas_json = json.dumps(cuentas_data)
    
    context = {
        'cuentas_json': cuentas_json,
        'total_pendiente': float(total_pendiente),
        'total_vencido': float(total_vencido),
        'pagos_mes': float(pagos_mes),
        'total_por_cobrar': float(total_por_cobrar),
        'search': search,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, "facturacion/cuentaporcobrar.html", context)

def registrar_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cuenta_id = data.get('cuenta_id')
            monto = Decimal(data.get('monto'))
            metodo_pago = data.get('metodo_pago')
            referencia = data.get('referencia', '')
            observaciones = data.get('observaciones', '')
            
            cuenta = get_object_or_404(CuentaPorCobrar, id=cuenta_id)
            
            # Verificar que la cuenta no esté anulada
            if cuenta.anulada:
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede registrar pago en una cuenta anulada'
                })
            
            # Validar que el monto no exceda el saldo pendiente
            saldo_pendiente = cuenta.monto_total - cuenta.monto_pagado
            if monto > saldo_pendiente:
                return JsonResponse({
                    'success': False,
                    'message': f'El monto excede el saldo pendiente de RD${saldo_pendiente}'
                })
            
            # Crear el pago
            pago = PagoCuentaPorCobrar(
                cuenta=cuenta,
                monto=monto,
                metodo_pago=metodo_pago,
                referencia=referencia,
                observaciones=observaciones
            )
            pago.save()
            
            # Crear comprobante de pago
            comprobante = ComprobantePago(
                pago=pago,
                cuenta=cuenta,
                cliente=cuenta.cliente,
                tipo_comprobante='recibo'
            )
            comprobante.save()
            
            # Actualizar la cuenta
            cuenta.monto_pagado += monto
            
            # Actualizar el estado basado en el monto total
            if cuenta.monto_pagado >= cuenta.monto_total:
                cuenta.estado = 'pagada'
            elif cuenta.monto_pagado > 0:
                cuenta.estado = 'parcial'
            
            cuenta.save()
            
            # Calcular nuevo saldo pendiente
            nuevo_saldo = cuenta.monto_total - cuenta.monto_pagado
            
            return JsonResponse({
                'success': True,
                'message': f'Pago registrado exitosamente. Comprobante: {comprobante.numero_comprobante}',
                'comprobante_numero': comprobante.numero_comprobante,
                'comprobante_id': comprobante.id,  # AÑADIR ESTO PARA EL PDF
                'nuevo_saldo_pendiente': float(nuevo_saldo),
                'monto_total_original': float(cuenta.monto_total),
                'monto_pagado_total': float(cuenta.monto_pagado),
                'estado_actual': cuenta.estado  # AÑADIR ESTADO ACTUALIZADO
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al registrar pago: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

# Vista para generar PDF del comprobante (completa)
def generar_comprobante_pdf(request, comprobante_id):
    try:
        comprobante = get_object_or_404(ComprobantePago, id=comprobante_id)
        
        # Crear respuesta HTTP con tipo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="comprobante_{comprobante.numero_comprobante}.pdf"'
        
        # Crear el objeto PDF
        p = canvas.Canvas(response)
        
        # Agregar contenido al PDF
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "COMPROBANTE DE PAGO")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 770, f"Número: {comprobante.numero_comprobante}")
        p.drawString(100, 750, f"Fecha: {comprobante.fecha_emision.strftime('%d/%m/%Y %H:%M')}")
        p.drawString(100, 730, f"Cliente: {comprobante.cliente.full_name}")
        p.drawString(100, 710, f"Factura: {comprobante.cuenta.venta.numero_factura}")
        p.drawString(100, 690, f"Monto: RD$ {comprobante.pago.monto:,.2f}")
        p.drawString(100, 670, f"Método: {comprobante.pago.get_metodo_pago_display()}")
        
        if comprobante.pago.referencia:
            p.drawString(100, 650, f"Referencia: {comprobante.pago.referencia}")
        
        p.drawString(100, 630, "¡Gracias por su pago!")
        
        # Finalizar el PDF
        p.showPage()
        p.save()
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al generar comprobante: {str(e)}'
        })
# ===== VISTA PARA LISTAR COMPROBANTES =====
def lista_comprobantes(request):
    comprobantes = ComprobantePago.objects.select_related(
        'pago', 'cuenta', 'cliente'
    ).order_by('-fecha_emision')
    
    # Filtros opcionales
    search = request.GET.get('search', '')
    if search:
        comprobantes = comprobantes.filter(
            Q(numero_comprobante__icontains=search) |
            Q(cliente__full_name__icontains=search) |
            Q(cuenta__venta__numero_factura__icontains=search)
        )
    
    context = {
        'comprobantes': comprobantes,
        'search': search,
    }
    
    return render(request, 'facturacion/lista_comprobantes.html', context)

def anular_cuenta(request, cuenta_id):
    if request.method == 'POST':
        try:
            cuenta = get_object_or_404(CuentaPorCobrar, id=cuenta_id)
            
            # Verificar que la cuenta no esté ya pagada completamente (usando monto_total)
            if cuenta.monto_pagado >= cuenta.monto_total:
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede anular una cuenta completamente pagada'
                })
            
            # Anular la cuenta
            cuenta.anular_cuenta()
            
            return JsonResponse({
                'success': True,
                'message': 'Cuenta anulada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al anular cuenta: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def detalle_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(
        CuentaPorCobrar.objects.select_related('venta', 'cliente'), 
        id=cuenta_id
    )
    
    pagos = PagoCuentaPorCobrar.objects.filter(cuenta=cuenta).order_by('-fecha_pago')
    
    data = {
        'id': cuenta.id,
        'factura': cuenta.venta.numero_factura,
        'cliente': cuenta.cliente.full_name,
        'telefono': cuenta.cliente.primary_phone or 'N/A',
        'productos': [
            {
                'nombre': item.producto.nombre if hasattr(item, 'producto') else 'Servicio',
                'cantidad': item.cantidad,
                'precio': item.precio
            }
            for item in cuenta.venta.detalles.all()
        ],
        'fecha_venta': cuenta.venta.fecha_venta.strftime('%Y-%m-%d'),
        'fecha_vencimiento': cuenta.fecha_vencimiento.strftime('%Y-%m-%d'),
        'monto_total': float(cuenta.monto_total),
        'monto_pagado': float(cuenta.monto_pagado),
        'saldo_pendiente': float(cuenta.saldo_pendiente),
        'estado': cuenta.get_estado_display(),
        'observaciones': cuenta.observaciones or 'N/A',
        'pagos': [
            {
                'fecha': pago.fecha_pago.strftime('%Y-%m-%d %H:%M'),
                'monto': float(pago.monto),
                'metodo': pago.get_metodo_pago_display(),
                'referencia': pago.referencia or 'N/A',
                'observaciones': pago.observaciones or 'N/A'
            }
            for pago in pagos
        ]
    }
    
    return JsonResponse(data)




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


    #ESTE ES EL NUEVO DE CIEERE DE CAJA
logger = logging.getLogger(__name__)

@login_required
def cierredecaja(request):
    # Verificar si hay una caja abierta
    caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
    
    if not caja_abierta:
        messages.error(request, 'No hay una caja abierta. Debe abrir una caja primero.')
        return redirect('iniciocaja')
    
    # Obtener ventas desde la apertura de caja para el usuario actual
    ventas_periodo = Venta.objects.filter(
        vendedor=request.user,
        fecha_venta__gte=caja_abierta.fecha_apertura,
        completada=True,
        anulada=False
    )
    
    # VENTAS AL CONTADO - Usamos el TOTAL FINAL
    ventas_contado_efectivo = ventas_periodo.filter(
        tipo_venta='contado',
        metodo_pago='efectivo'
    ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
    ventas_contado_tarjeta = ventas_periodo.filter(
        tipo_venta='contado',
        metodo_pago='tarjeta'
    ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
    ventas_contado_transferencia = ventas_periodo.filter(
        tipo_venta='contado',
        metodo_pago='transferencia'
    ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
    # VENTAS A CRÉDITO - Usamos solo el MONTO INICIAL
    ventas_credito_efectivo = ventas_periodo.filter(
        tipo_venta='credito',
        metodo_pago='efectivo'
    ).aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
    
    ventas_credito_tarjeta = ventas_periodo.filter(
        tipo_venta='credito',
        metodo_pago='tarjeta'
    ).aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
    
    ventas_credito_transferencia = ventas_periodo.filter(
        tipo_venta='credito',
        metodo_pago='transferencia'
    ).aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
    
    # CALCULAR TOTALES AJUSTADOS
    # Efectivo: contado (total final) + crédito (solo monto inicial)
    ventas_efectivo_ajustado = ventas_contado_efectivo + ventas_credito_efectivo
    
    # Tarjeta: contado (total final) + crédito (solo monto inicial)
    ventas_tarjeta_ajustado = ventas_contado_tarjeta + ventas_credito_tarjeta
    
    # Transferencia: contado (total final) + crédito (solo monto inicial)
    ventas_transferencia_ajustado = ventas_contado_transferencia + ventas_credito_transferencia
    
    # Total general de ventas
    total_ventas_ajustado = (ventas_contado_efectivo + ventas_contado_tarjeta + ventas_contado_transferencia +
                            ventas_credito_efectivo + ventas_credito_tarjeta + ventas_credito_transferencia)
    
    # Totales por tipo de venta para reporte
    total_ventas_contado = ventas_contado_efectivo + ventas_contado_tarjeta + ventas_contado_transferencia
    total_ventas_credito = ventas_credito_efectivo + ventas_credito_tarjeta + ventas_credito_transferencia
    
    # Obtener cantidad de ventas
    cantidad_ventas = ventas_periodo.count()
    
    # Obtener información de clientes
    clientes_count = Cliente.objects.filter(
        venta__in=ventas_periodo
    ).distinct().count()
    
    # Log para depuración
    logger.info(f"Caja abierta: {caja_abierta}")
    logger.info(f"Ventas encontradas: {cantidad_ventas}")
    logger.info(f"Ventas contado efectivo: {ventas_contado_efectivo}")
    logger.info(f"Ventas contado tarjeta: {ventas_contado_tarjeta}")
    logger.info(f"Ventas contado transferencia: {ventas_contado_transferencia}")
    logger.info(f"Ventas crédito efectivo (monto inicial): {ventas_credito_efectivo}")
    logger.info(f"Ventas crédito tarjeta (monto inicial): {ventas_credito_tarjeta}")
    logger.info(f"Ventas crédito transferencia (monto inicial): {ventas_credito_transferencia}")
    
    context = {
        'caja_abierta': caja_abierta,
        'total_ventas': total_ventas_ajustado,
        'ventas_efectivo': ventas_efectivo_ajustado,
        'ventas_tarjeta': ventas_tarjeta_ajustado,
        'ventas_transferencia': ventas_transferencia_ajustado,
        'total_ventas_contado': total_ventas_contado,
        'total_ventas_credito': total_ventas_credito,
        'cantidad_ventas': cantidad_ventas,
        'clientes_hoy': clientes_count,
        'hoy': timezone.now().date(),
    }
    
    return render(request, "facturacion/cierredecaja.html", context)



@login_required
def procesar_cierre_caja(request):
    if request.method == 'POST':
        # Obtener la caja abierta actual
        caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
        
        if not caja_abierta:
            messages.error(request, 'No hay una caja abierta para cerrar.')
            return redirect('cierredecaja')
        
        # Obtener ventas desde la apertura de caja
        ventas_periodo = Venta.objects.filter(
            vendedor=request.user,
            fecha_venta__gte=caja_abierta.fecha_apertura,
            completada=True,
            anulada=False
        )
        
        # VENTAS AL CONTADO - Usamos el TOTAL FINAL
        ventas_contado_efectivo = ventas_periodo.filter(
            tipo_venta='contado',
            metodo_pago='efectivo'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        
        ventas_contado_tarjeta = ventas_periodo.filter(
            tipo_venta='contado',
            metodo_pago='tarjeta'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        
        ventas_contado_transferencia = ventas_periodo.filter(
            tipo_venta='contado',
            metodo_pago='transferencia'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        
        # VENTAS A CRÉDITO - Usamos solo el MONTO INICIAL
        ventas_credito_efectivo = ventas_periodo.filter(
            tipo_venta='credito',
            metodo_pago='efectivo'
        ).aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
        
        ventas_credito_tarjeta = ventas_periodo.filter(
            tipo_venta='credito',
            metodo_pago='tarjeta'
        ).aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
        
        ventas_credito_transferencia = ventas_periodo.filter(
            tipo_venta='credito',
            metodo_pago='transferencia'
        ).aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
        
        # Calcular total esperado
        total_esperado = (ventas_contado_efectivo + ventas_contado_tarjeta + ventas_contado_transferencia +
                         ventas_credito_efectivo + ventas_credito_tarjeta + ventas_credito_transferencia)
        
        # Resto del código permanece igual...
        # Obtener datos del formulario
        monto_efectivo_real = request.POST.get('cash-amount')
        monto_tarjeta_real = request.POST.get('card-amount') or '0'
        observaciones = request.POST.get('observations', '')
        
        # Validaciones
        if not monto_efectivo_real:
            messages.error(request, 'Debe ingresar el monto en efectivo real.')
            return redirect('cierredecaja')
        
        try:
            # Convertir a Decimal en lugar de float
            monto_efectivo_real = Decimal(monto_efectivo_real)
            monto_tarjeta_real = Decimal(monto_tarjeta_real)
        except (ValueError, InvalidOperation):
            messages.error(request, 'Los montos deben ser valores numéricos válidos.')
            return redirect('cierredecaja')
        
        # Calcular diferencia (todos son Decimal ahora)
        total_real = monto_efectivo_real + monto_tarjeta_real
        diferencia = total_real - total_esperado
        
        # Actualizar la caja
        caja_abierta.monto_final = total_real
        caja_abierta.fecha_cierre = timezone.now()
        caja_abierta.estado = 'cerrada'
        caja_abierta.observaciones = observaciones
        caja_abierta.save()
        
        # Crear registro de cierre
        cierre = CierreCaja.objects.create(
            caja=caja_abierta,
            monto_efectivo_real=monto_efectivo_real,
            monto_tarjeta_real=monto_tarjeta_real,
            total_esperado=total_esperado,
            diferencia=diferencia,
            observaciones=observaciones
        )
        
        # Guardar información en sesión para mostrar en el cuadre
        request.session['cierre_info'] = {
            'fecha': timezone.now().date().strftime('%d/%m/%Y'),
            'hora_cierre': timezone.now().strftime('%H:%M:%S'),
            'monto_efectivo_real': float(monto_efectivo_real),
            'monto_tarjeta_real': float(monto_tarjeta_real),
            'total_esperado': float(total_esperado),
            'diferencia': float(diferencia),
            'observaciones': observaciones,
            'ventas_count': ventas_periodo.count(),
            'clientes_count': Cliente.objects.filter(
                venta__in=ventas_periodo
            ).distinct().count()
        }
        
        messages.success(request, f'Caja cerrada exitosamente. Diferencia: RD${diferencia:,.2f}')
        return redirect('cuadre')
    
    return redirect('cierredecaja')


#ESTE ES EL CODGO COMENTADO DEL CIERRE DE CAJA, POR SI SE NECESITA EN EL FUTURO
# logger = logging.getLogger(__name__)

# @login_required
# def cierredecaja(request):
#     # Verificar si hay una caja abierta
#     caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
    
#     if not caja_abierta:
#         messages.error(request, 'No hay una caja abierta. Debe abrir una caja primero.')
#         return redirect('iniciocaja')
    
#     # Obtener ventas desde la apertura de caja para el usuario actual
#     ventas_periodo = Venta.objects.filter(
#         vendedor=request.user,
#         fecha_venta__gte=caja_abierta.fecha_apertura,
#         completada=True,
#         anulada=False
#     )
    
#     # Calcular totales usando agregación de Django
#     total_ventas = ventas_periodo.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
#     # Calcular ventas por método de pago
#     ventas_efectivo = ventas_periodo.filter(
#         metodo_pago='efectivo'
#     ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
#     ventas_tarjeta = ventas_periodo.filter(
#         metodo_pago='tarjeta'
#     ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
#     ventas_transferencia = ventas_periodo.filter(
#         metodo_pago='transferencia'
#     ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
#     # Obtener información adicional para el reporte
#     total_ventas_contado = ventas_periodo.filter(
#         tipo_venta='contado'
#     ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
#     total_ventas_credito = ventas_periodo.filter(
#         tipo_venta='credito'
#     ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
    
#     # Obtener cantidad de ventas
#     cantidad_ventas = ventas_periodo.count()
    
#     # Obtener información de clientes
#     clientes_count = Cliente.objects.filter(
#         venta__in=ventas_periodo
#     ).distinct().count()
    
#     # CALCULAR EL TOTAL ESPERADO (MONTO INICIAL + TOTAL VENTAS)
#     total_esperado = caja_abierta.monto_inicial + total_ventas
    
#     # CALCULAR EL EFECTIVO TOTAL EN CAJA (MONTO INICIAL + VENTAS EN EFECTIVO)
#     efectivo_en_caja = caja_abierta.monto_inicial + ventas_efectivo
    
#     # Log para depuración
#     logger.info(f"Caja abierta: {caja_abierta}")
#     logger.info(f"Ventas encontradas: {cantidad_ventas}")
#     logger.info(f"Total ventas: {total_ventas}")
#     logger.info(f"Ventas efectivo: {ventas_efectivo}")
#     logger.info(f"Ventas tarjeta: {ventas_tarjeta}")
#     logger.info(f"Total esperado: {total_esperado}")
#     logger.info(f"Efectivo total en caja: {efectivo_en_caja}")
    
#     context = {
#         'caja_abierta': caja_abierta,
#         'total_ventas': total_ventas,
#         'total_esperado': total_esperado,  # Nuevo campo para el total esperado
#         'ventas_efectivo': ventas_efectivo,
#         'efectivo_en_caja': efectivo_en_caja,  # Efectivo total en caja
#         'ventas_tarjeta': ventas_tarjeta,
#         'ventas_transferencia': ventas_transferencia,
#         'total_ventas_contado': total_ventas_contado,
#         'total_ventas_credito': total_ventas_credito,
#         'cantidad_ventas': cantidad_ventas,
#         'clientes_hoy': clientes_count,
#         'hoy': timezone.now().date(),
#     }
    
#     return render(request, "facturacion/cierredecaja.html", context)




# @login_required
# def procesar_cierre_caja(request):
#     if request.method == 'POST':
#         # Obtener la caja abierta actual
#         caja_abierta = Caja.objects.filter(usuario=request.user, estado='abierta').first()
        
#         if not caja_abierta:
#             messages.error(request, 'No hay una caja abierta para cerrar.')
#             return redirect('cierredecaja')
        
#         # Obtener ventas desde la apertura de caja
#         ventas_periodo = Venta.objects.filter(
#             vendedor=request.user,
#             fecha_venta__gte=caja_abierta.fecha_apertura,
#             completada=True,
#             anulada=False
#         )
        
#         # CORRECCIÓN: Incluir el monto inicial en el total esperado
#         total_ventas = ventas_periodo.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
#         total_esperado = caja_abierta.monto_inicial + total_ventas
        
#         # Obtener datos del formulario
#         monto_efectivo_real = request.POST.get('cash-amount')
#         monto_tarjeta_real = request.POST.get('card-amount') or '0'
#         observaciones = request.POST.get('observations', '')
        
#         # Validaciones
#         if not monto_efectivo_real:
#             messages.error(request, 'Debe ingresar el monto en efectivo real.')
#             return redirect('cierredecaja')
        
#         try:
#             # Convertir a Decimal en lugar de float
#             monto_efectivo_real = Decimal(monto_efectivo_real)
#             monto_tarjeta_real = Decimal(monto_tarjeta_real)
#         except (ValueError, InvalidOperation):
#             messages.error(request, 'Los montos deben ser valores numéricos válidos.')
#             return redirect('cierredecaja')
        
#         # Calcular diferencia (todos son Decimal ahora)
#         total_real = monto_efectivo_real + monto_tarjeta_real
#         diferencia = total_real - total_esperado
        
#         # Actualizar la caja
#         caja_abierta.monto_final = total_real
#         caja_abierta.fecha_cierre = timezone.now()
#         caja_abierta.estado = 'cerrada'
#         caja_abierta.observaciones = observaciones
#         caja_abierta.save()
        
#         # Crear registro de cierre
#         cierre = CierreCaja.objects.create(
#             caja=caja_abierta,
#             monto_efectivo_real=monto_efectivo_real,
#             monto_tarjeta_real=monto_tarjeta_real,
#             total_esperado=total_esperado,
#             diferencia=diferencia,
#             observaciones=observaciones
#         )
        
#         # Guardar información en sesión para mostrar en el cuadre
#         request.session['cierre_info'] = {
#             'fecha': timezone.now().date().strftime('%d/%m/%Y'),
#             'hora_cierre': timezone.now().strftime('%H:%M:%S'),
#             'monto_efectivo_real': float(monto_efectivo_real),
#             'monto_tarjeta_real': float(monto_tarjeta_real),
#             'total_esperado': float(total_esperado),
#             'diferencia': float(diferencia),
#             'observaciones': observaciones,
#             'ventas_count': ventas_periodo.count(),
#             'clientes_count': Cliente.objects.filter(
#                 venta__in=ventas_periodo
#             ).distinct().count(),
#             'monto_inicial': float(caja_abierta.monto_inicial)  # Agregar para referencia
#         }
        
#         messages.success(request, f'Caja cerrada exitosamente. Diferencia: RD${diferencia:,.2f}')
#         return redirect('cuadre')
    
#     return redirect('cierredecaja')





@login_required
def cuadre(request):
    # Obtener la caja abierta actual o la última cerrada
    caja_actual = Caja.objects.filter(usuario=request.user, estado='abierta').first()
    
    if not caja_actual:
        # Si no hay caja abierta, usar la última cerrada para este usuario
        caja_actual = Caja.objects.filter(usuario=request.user, estado='cerrada').order_by('-fecha_cierre').first()
    
    context = {
        'caja': None,
        'ventas': {},
        'cierre': None
    }
    
    if caja_actual:
        # Obtener ventas de esta caja (período de la caja)
        ventas = Venta.objects.filter(
            vendedor=request.user,  # Solo ventas del usuario actual
            fecha_venta__gte=caja_actual.fecha_apertura,
            completada=True,
            anulada=False
        )
        
        if caja_actual.fecha_cierre:
            ventas = ventas.filter(fecha_venta__lte=caja_actual.fecha_cierre)
        
        # Obtener cierre de caja si existe
        cierre = CierreCaja.objects.filter(caja=caja_actual).first()
        
        # Calcular totales por método de pago
        ventas_efectivo = ventas.filter(metodo_pago='efectivo').aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        ventas_tarjeta = ventas.filter(metodo_pago='tarjeta').aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        ventas_transferencia = ventas.filter(metodo_pago='transferencia').aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        
        # Separar ventas por tipo (contado vs crédito)
        ventas_contado = ventas.filter(tipo_venta='contado')
        ventas_credito = ventas.filter(tipo_venta='credito')
        
        # Calcular totales por tipo de venta
        total_contado = ventas_contado.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        montoinicial_credito = ventas_credito.aggregate(total=Sum('montoinicial'))['total'] or Decimal('0.00')
        total_credito = ventas_credito.aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        
        # CALCULAR MONTO CONTADO según los requisitos:
        # monto contado = monto inicial de caja + total a pagar (ventas contado) + monto inicial (ventas crédito)
        monto_inicial_caja = caja_actual.monto_inicial
        monto_contado = monto_inicial_caja + total_contado + montoinicial_credito
        
        # Preparar datos para el template
        context = {
            'caja': caja_actual,  # Pasar el objeto completo de caja
            'ventas': {
                'efectivo': ventas_efectivo,
                'tarjeta': ventas_tarjeta,
                'transferencia': ventas_transferencia,
                'credito': total_credito,
                'total': ventas_efectivo + ventas_tarjeta + ventas_transferencia + total_credito,
                'contado': total_contado,
                'montoinicial_credito': montoinicial_credito
            },
            'cierre': cierre  # Pasar el objeto completo de cierre
        }
    
    return render(request, 'facturacion/cuadre.html', context)


def reavastecer(request):
    # Obtener todos los productos activos
    productos = EntradaProducto.objects.filter(activo=True)
    
    # Preparar datos para el template
    productos_data = []
    for producto in productos:
        productos_data.append({
            'id': producto.id,
            'name': producto.nombre_producto,
            'brand': producto.get_marca_display(),
            'model': f"{producto.modelo} {producto.capacidad if producto.capacidad else ''}",
            'stock': producto.cantidad,
            'price': float(producto.costo_venta),
            'min_stock': producto.cantidad_minima
        })
    
    context = {
        'productos': productos_data,
        'total_productos': productos.count(),
        'productos_stock_bajo': productos.filter(cantidad__lte=models.F('cantidad_minima')).count(),
        'valor_total': sum(p.cantidad * p.costo_venta for p in productos)
    }
    
    return render(request, "facturacion/reavastecer.html", context)

@csrf_exempt
@require_POST
def actualizar_stock(request):
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        nueva_cantidad = data.get('nueva_cantidad')
        
        # Validar datos
        if not producto_id or nueva_cantidad is None:
            return JsonResponse({'success': False, 'error': 'Datos incompletos'})
        
        # Buscar y actualizar el producto
        producto = EntradaProducto.objects.get(id=producto_id, activo=True)
        
        # Guardar cantidad anterior para el movimiento de stock
        cantidad_anterior = producto.cantidad
        
        # Actualizar cantidad
        producto.cantidad = nueva_cantidad
        producto.save()
        
        # Registrar movimiento de stock
        producto.registrar_movimiento_stock(
            tipo_movimiento='ajuste',
            cantidad=abs(cantidad_anterior - nueva_cantidad),
            cantidad_anterior=cantidad_anterior,
            cantidad_nueva=nueva_cantidad,
            motivo="Ajuste manual desde sistema de reabastecimiento",
            usuario=request.user if request.user.is_authenticated else None
        )
        
        return JsonResponse({'success': True, 'nuevo_stock': producto.cantidad})
    
    except EntradaProducto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    


def devoluciones(request):
    return render(request, "facturacion/devoluciones.html")


@csrf_exempt
@require_http_methods(["POST"])
def buscar_factura_devolucion(request):
    try:
        data = json.loads(request.body)
        numero_factura = data.get('numero_factura', '').strip()
        
        if not numero_factura:
            return JsonResponse({'error': 'Por favor, ingrese un número de factura.'}, status=400)
        
        # Buscar la factura
        try:
            venta = Venta.objects.get(numero_factura=numero_factura, anulada=False)
        except Venta.DoesNotExist:
            return JsonResponse({'error': 'No se encontró ninguna factura con ese número.'}, status=404)
        
        # Obtener detalles de la venta
        detalles = DetalleVenta.objects.filter(venta=venta)
        
        # Preparar información de productos
        productos = []
        for detalle in detalles:
            producto = detalle.producto
            productos.append({
                'id': detalle.id,
                'codigo': producto.codigo_producto,
                'producto': producto.nombre_producto,
                'marca': producto.get_marca_display(),
                'capacidad': producto.get_capacidad_display() if producto.capacidad else 'N/A',
                'color': producto.get_color_display() if producto.color else 'N/A',
                'estado': producto.get_estado_display(),
                'cantidad': detalle.cantidad,
                'precio': str(detalle.precio_unitario),
                'chasis': producto.imei_serial,
                'imagen': '/static/images/default-product.png'  # Imagen por defecto
            })
        
        # Información de la factura
        factura_info = {
            'id': venta.numero_factura,
            'fecha': venta.fecha_venta.strftime('%d/%m/%Y'),
            'cliente': venta.cliente_nombre,
            'total': str(venta.total),
            'estado': 'Pagada' if venta.completada else 'Pendiente',
            'vendedor': venta.vendedor.get_full_name() or venta.vendedor.username,
            'productos': productos
        }
        
        return JsonResponse({'factura': factura_info})
    
    except Exception as e:
        return JsonResponse({'error': f'Error al buscar la factura: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@transaction.atomic
def procesar_devolucion(request):
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        required_fields = ['factura_id', 'producto_id', 'motivo', 'cantidad']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'error': f'El campo {field} es requerido.'}, status=400)
        
        # Obtener la venta y el detalle
        venta = get_object_or_404(Venta, numero_factura=data['factura_id'], anulada=False)
        detalle = get_object_or_404(DetalleVenta, id=data['producto_id'], venta=venta)
        
        # Validar cantidad
        cantidad_devolver = int(data['cantidad'])
        if cantidad_devolver <= 0:
            return JsonResponse({'error': 'La cantidad a devolver debe ser mayor a 0.'}, status=400)
        
        if cantidad_devolver > detalle.cantidad:
            return JsonResponse({'error': 'No puede devolver más unidades de las vendidas.'}, status=400)
        
        # Realizar la devolución
        producto = detalle.producto
        producto.sumar_stock(
            cantidad=cantidad_devolver,
            usuario=request.user,
            motivo=f"Devolución - {data['motivo']}",
            referencia=f"Factura: {venta.numero_factura}"
        )
        
        # Registrar la devolución (aquí puedes crear un modelo Devolucion si lo necesitas)
        # Por ahora, simplemente actualizamos el detalle de venta
        detalle.cantidad -= cantidad_devolver
        if detalle.cantidad == 0:
            detalle.delete()
        else:
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario
            detalle.save()
        
        # Recalcular totales de la venta
        detalles_restantes = DetalleVenta.objects.filter(venta=venta)
        venta.subtotal = sum(detalle.subtotal for detalle in detalles_restantes)
        venta.total = venta.subtotal - venta.descuento_monto
        venta.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Devolución procesada correctamente. Se han devuelto {cantidad_devolver} unidades.',
            'numero_devolucion': f'DEV-{timezone.now().strftime("%Y%m%d")}-{venta.id}'
        })
    
    except Exception as e:
        return JsonResponse({'error': f'Error al procesar la devolución: {str(e)}'}, status=500)



# Función para verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='/admin/login/')
def roles(request):
    # Obtener todos los grupos (roles)
    groups = Group.objects.all()
    
    # Obtener todos los usuarios
    users = User.objects.all().prefetch_related('groups')
    
    # Procesar datos para los templates
    roles_data = []
    for group in groups:
        user_count = group.user_set.count()
        permissions = list(group.permissions.values_list('codename', flat=True))
        
        roles_data.append({
            'id': group.id,
            'name': group.name,
            'description': '',
            'status': 'activo',
            'isGlobal': True,
            'permissions': permissions,
            'userCount': user_count
        })
    
    users_data = []
    for user in users:
        user_group = user.groups.first()
        role_name = user_group.name if user_group else 'Sin rol'
        
        users_data.append({
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
            'role': role_name,
            'status': 'activo' if user.is_active else 'inactivo',
            'lastAccess': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Nunca'
        })
    
    # Estadísticas
    total_roles = groups.count()
    active_roles = total_roles
    inactive_roles = 0
    
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    inactive_users = total_users - active_users
    
    context = {
        'roles_data': roles_data,
        'users_data': users_data,
        'total_roles': total_roles,
        'active_roles': active_roles,
        'inactive_roles': inactive_roles,
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
    }
    
    # Manejar búsquedas y filtros
    search_role = request.GET.get('search_role', '')
    status_filter = request.GET.get('status_filter', '')
    
    if search_role:
        context['roles_data'] = [r for r in context['roles_data'] 
                                if search_role.lower() in r['name'].lower()]
    
    if status_filter:
        context['roles_data'] = [r for r in context['roles_data'] 
                                if r['status'] == status_filter]
    
    # Manejar búsquedas y filtros para usuarios
    search_user = request.GET.get('search_user', '')
    role_filter = request.GET.get('role_filter', '')
    user_status_filter = request.GET.get('user_status_filter', '')
    
    if search_user:
        context['users_data'] = [u for u in context['users_data'] 
                                if search_user.lower() in u['name'].lower() or 
                                search_user.lower() in u['email'].lower()]
    
    if role_filter:
        context['users_data'] = [u for u in context['users_data'] 
                                if u['role'] == role_filter]
    
    if user_status_filter:
        context['users_data'] = [u for u in context['users_data'] 
                                if u['status'] == user_status_filter]
    
    # Manejar acciones POST (crear, editar, eliminar)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_role':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            
            if not name:
                messages.error(request, 'El nombre del rol es obligatorio.')
            elif Group.objects.filter(name=name).exists():
                messages.error(request, 'Ya existe un rol con este nombre.')
            else:
                group = Group.objects.create(name=name)
                messages.success(request, 'Rol creado exitosamente.')
                return redirect('roles')
        
        elif action == 'edit_role':
            role_id = request.POST.get('role_id')
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            status = request.POST.get('status', 'activo')
            
            if not name:
                messages.error(request, 'El nombre del rol es obligatorio.')
            else:
                group = get_object_or_404(Group, id=role_id)
                
                if Group.objects.filter(name=name).exclude(id=role_id).exists():
                    messages.error(request, 'Ya existe otro rol con este nombre.')
                else:
                    group.name = name
                    group.save()
                    messages.success(request, 'Rol actualizado exitosamente.')
                    return redirect('roles')
        
        elif action == 'delete_role':
            role_id = request.POST.get('role_id')
            group = get_object_or_404(Group, id=role_id)
            
            if group.user_set.exists():
                messages.error(request, 'No se puede eliminar un rol que tiene usuarios asignados.')
            else:
                group.delete()
                messages.success(request, 'Rol eliminado exitosamente.')
                return redirect('roles')
        
        elif action == 'create_user':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            role_id = request.POST.get('role_id')
            is_active = request.POST.get('status', 'activo') == 'activo'
            
            if not all([username, email, password, role_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Ya existe un usuario con este nombre de usuario.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un usuario con este email.')
            else:
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password=password,
                            first_name=first_name,
                            last_name=last_name,
                            is_active=is_active
                        )
                        
                        group = get_object_or_404(Group, id=role_id)
                        user.groups.add(group)
                    
                    messages.success(request, 'Usuario creado exitosamente.')
                    return redirect('roles')
                except Exception as e:
                    messages.error(request, f'Error al crear usuario: {str(e)}')
        
        elif action == 'edit_user':
            user_id = request.POST.get('user_id')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password', None)
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            role_id = request.POST.get('role_id')
            is_active = request.POST.get('status', 'activo') == 'activo'
            
            if not all([username, email, role_id]):
                messages.error(request, 'Todos los campos obligatorios deben ser completados.')
            else:
                user = get_object_or_404(User, id=user_id)
                
                if User.objects.filter(username=username).exclude(id=user_id).exists():
                    messages.error(request, 'Ya existe otro usuario con este nombre de usuario.')
                elif User.objects.filter(email=email).exclude(id=user_id).exists():
                    messages.error(request, 'Ya existe otro usuario con este email.')
                else:
                    try:
                        with transaction.atomic():
                            user.username = username
                            user.email = email
                            user.first_name = first_name
                            user.last_name = last_name
                            user.is_active = is_active
                            
                            if password:
                                user.set_password(password)
                            
                            user.save()
                            
                            # Actualizar el rol
                            user.groups.clear()
                            group = get_object_or_404(Group, id=role_id)
                            user.groups.add(group)
                        
                        messages.success(request, 'Usuario actualizado exitosamente.')
                        return redirect('roles')
                    except Exception as e:
                        messages.error(request, f'Error al actualizar usuario: {str(e)}')
        
        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            if user == request.user:
                messages.error(request, 'No puedes eliminar tu propio usuario.')
            else:
                user.delete()
                messages.success(request, 'Usuario eliminado exitosamente.')
                return redirect('roles')
        
        elif action == 'export_roles_csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="roles.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Nombre', 'Descripción', 'Estado', 'Usuarios Asignados'])
            
            for group in Group.objects.all():
                user_count = group.user_set.count()
                writer.writerow([group.name, '', 'activo', user_count])
            
            return response
        
        elif action == 'export_users_csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Nombre', 'Email', 'Rol', 'Estado', 'Último Acceso'])
            
            for user in User.objects.all().prefetch_related('groups'):
                user_group = user.groups.first()
                role_name = user_group.name if user_group else 'Sin rol'
                
                writer.writerow([
                    f"{user.first_name} {user.last_name}".strip() or user.username,
                    user.email,
                    role_name,
                    'activo' if user.is_active else 'inactivo',
                    user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Nunca'
                ])
            
            return response
    
    return render(request, "facturacion/roles.html", context)



def anular(request):
    return render(request, "facturacion/anular.html")




def buscar_factura(request):
    if request.method == 'POST':
        try:
            numero_factura = request.POST.get('numero_factura', '').strip()
            
            if not numero_factura:
                return JsonResponse({'error': 'Número de factura requerido'}, status=400)
            
            # Buscar la factura
            try:
                venta = Venta.objects.get(numero_factura=numero_factura)
            except Venta.DoesNotExist:
                return JsonResponse({'error': 'Factura no encontrada'}, status=404)
            
            # Obtener detalles de la venta
            detalles = DetalleVenta.objects.filter(venta=venta)
            
            # Información básica del cliente
            cliente_info = {
                'nombre': venta.cliente_nombre,
                'cedula': venta.cliente_documento,
                'telefono': 'N/A',
                'direccion': 'N/A',
            }
            
            # Determinar tipo de venta
            tipo_venta = 'Contado' if venta.tipo_venta == 'contado' else 'Crédito'
            
            # Formatear datos para la respuesta
            factura_data = {
                'id': venta.id,
                'numero_factura': venta.numero_factura,
                'fecha': venta.fecha_venta.strftime('%Y-%m-%d'),
                'estado': 'anulada' if venta.anulada else 'activa',
                'tipo_venta': tipo_venta,
                'cliente': cliente_info,
                'vendedor': f"{venta.vendedor.first_name} {venta.vendedor.last_name}",
                'items': [],
                'subtotal': float(venta.subtotal),
                'itbis': float(venta.total - venta.subtotal),
                'total': float(venta.total),
                'forma_pago': venta.get_metodo_pago_display(),
                'monto_inicial': float(venta.montoinicial) if venta.montoinicial else 0,
                'es_financiada': venta.es_financiada,
                'monto_financiado': float(venta.monto_financiado) if venta.monto_financiado else 0,
                'tasa_interes': float(venta.tasa_interes) if venta.tasa_interes else 0,
                'plazo_meses': venta.plazo_meses if venta.plazo_meses else 0,
                'cuota_mensual': float(venta.cuota_mensual) if venta.cuota_mensual else 0,
            }
            
            # Agregar items
            for detalle in detalles:
                factura_data['items'].append({
                    'producto': detalle.producto.nombre_producto,
                    'cantidad': detalle.cantidad,
                    'precio': float(detalle.precio_unitario),
                    'subtotal': float(detalle.subtotal)
                })
            
            return JsonResponse(factura_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)



def anular_factura(request):
    if request.method == 'POST':
        try:
            factura_id = request.POST.get('factura_id')
            motivo = request.POST.get('motivo', '').strip()
            
            if not motivo:
                return JsonResponse({'error': 'Motivo de anulación requerido'}, status=400)
            
            # Buscar la factura
            try:
                venta = Venta.objects.get(id=factura_id, anulada=False)
            except Venta.DoesNotExist:
                return JsonResponse({'error': 'Factura no encontrada o ya anulada'}, status=404)
            
            # Anular la factura
            venta.anulada = True
            venta.motivo_anulacion = motivo
            venta.fecha_anulacion = timezone.now()
            venta.usuario_anulacion = request.user
            venta.save()
            
            # Restaurar el inventario
            detalles = DetalleVenta.objects.filter(venta=venta)
            for detalle in detalles:
                producto = detalle.producto
                producto.cantidad += detalle.cantidad
                producto.save()
            
            return JsonResponse({'success': True, 'message': 'Factura anulada correctamente'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)