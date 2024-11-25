from django.contrib import admin
from .models import Producto, Usuario, Carrito, CarritoProducto

# Register your models here.
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)