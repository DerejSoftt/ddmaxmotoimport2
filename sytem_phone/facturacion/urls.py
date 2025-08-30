from django.urls import path
from . import views

urlpatterns = [
       path('', views.index, name='login'),  # Página de login
    path("" , views.index, name="index"),
    path("dashboard" , views.dashboard, name="dashboard"),
    path("inventario", views.inventario, name="inventario"),
    path('inventario/datos/', views.inventario_datos, name='inventario_datos'),
    path('inventario/editar/<int:id>/', views.inventario_editar, name='inventario_editar'),
    path('inventario/eliminar/<int:id>/', views.inventario_eliminar, name='inventario_eliminar'),
    # path("facturacion", views.facturacion, name="facturacion"),
    path("listadecliente", views.listadecliente, name="listadecliente"),
    path("registrodecliente", views.registrodecliente,  name="registrodecliente"),
    path("entrada", views.entrada, name="entrada"),
    path('agregar-nuevo-producto/', views.agregar_nuevo_producto, name='agregar_nuevo_producto'),
    path('productos-disponibles/', views.obtener_productos_disponibles, name='obtener_productos_disponibles'),
    path('producto/<int:entrada_id>/', views.obtener_datos_entrada, name='obtener_datos_entrada'),
    path('obtener-datos-plantilla/<int:plantilla_id>/', views.obtener_datos_plantilla, name='obtener_datos_plantilla'),
    path("cuentaporcobrar", views.cuentaporcobrar, name="cuentaporcobrar"),
    path("gestiondesuplidores", views.gestiondesuplidores, name="gestiondesuplidores"),
    path("registrosuplidores", views.registrosuplidores, name="registrosuplidores"),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedores/<int:id>/data/', views.get_proveedor_data, name='get_proveedor_data'),
    path('guardar-cliente/', views.guardar_cliente, name='guardar_cliente'),
    path('obtener-clientes/', views.obtener_clientes, name='obtener_clientes'),
    path('eliminar-cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('iniciocaja', views.iniciocaja, name='iniciocaja'),
    path('ventas', views.ventas, name='ventas'),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('procesar-venta/', views.procesar_venta, name='procesar_venta'),
    #   path('historial-ventas/', views.historial_ventas, name='historial_ventas'),
    path('comprobante-venta/<int:venta_id>/', views.comprobante_venta, name='comprobante_venta'),
    path('buscar-productos/', views.buscar_productos_similares, name='buscar_productos'),
    

      
]
