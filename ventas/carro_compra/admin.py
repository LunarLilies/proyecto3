from django.contrib import admin
from .models import Producto, Carrito, CarritoProducto, Venta, DetalleVenta

# Register your models here.
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)