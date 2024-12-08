from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    foto        = models.ImageField(upload_to='fotos/', blank=True, null=True)
    nombre_prod = models.CharField(max_length=100, blank=False)
    stock       = models.IntegerField(default=0, blank=False, null=False)
    precio      = models.IntegerField(blank=False, null=False)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return str(f"(ID: {self.id_producto}) Nombre Producto: {self.nombre_prod}")


class Carrito(models.Model):
    id_carrito  = models.AutoField(primary_key=True)
    usuario     = models.ForeignKey(User, related_name="usuario_carrito", on_delete=models.CASCADE, null=True, blank=True)
    activo      = models.BooleanField(default=True)

    def __str__(self):
        if self.usuario:
            return f"Carrito {self.id_carrito} - Usuario: {self.usuario.first_name} {self.usuario.last_name}"
        else:
            return f"Carrito {self.id_carrito} - Usuario: None"

class CarritoProducto(models.Model):
    carrito     = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto    = models.ForeignKey(Producto, related_name="productos_carrito", on_delete=models.CASCADE)
    cant_compra = models.IntegerField(default=1)
    subtotal    = models.IntegerField(null=False)
    total_carro = models.IntegerField(null=False)

    def __str__(self):
        return f"Carrito {self.carrito.id_carrito} - Producto {self.producto.nombre_prod} - Cantidad {self.cant_compra}"


class Venta(models.Model):
    fecha   = models.DateTimeField(auto_now_add=True)
    total   = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    usuario = models.ForeignKey(User, related_name="venta_usuario", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.usuario:
            return f"Venta {self.id} - Usuario: {self.usuario.first_name} {self.usuario.last_name}"
        else:
            return f"Venta {self.id} - Usuario: None"


class DetalleVenta(models.Model):
    venta    = models.ForeignKey(Venta , related_name="detalle_venta" , on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto , related_name="detalle_producto" , on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)