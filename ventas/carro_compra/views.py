from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoProducto, Usuario, Venta, DetalleVenta
from django.db.models import Sum
from datetime import datetime

# Create your views here.
def base(request):
    context = {}
    if "user" in request.session:
        context["usuario"] = request.session["user"]
    else:
        context["usuario"] = None
    return render(request, 'carro_compra/base.html', context)


def productos(request):
    print("estoy en la lista de productos")
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'carro_compra/productos.html', context)


def producto_seleccionado(request, id_producto):
    print("estoy viendo un producto seleccionado")
    producto = get_object_or_404(Producto, id_producto = id_producto)
    context = {'producto': producto}
    return render(request, 'carro_compra/producto_seleccionado.html', context)


def carrito(request):
    carrito = Carrito.objects.filter(activo=True).first()
    
    if carrito:
        productos_carrito = CarritoProducto.objects.filter(carrito=carrito)
        total_carrito = sum(item.subtotal for item in productos_carrito)
    else:
        productos_carrito = []
        total_carrito = 0
    
    return render(request, 'carro_compra/carrito.html', {'productos_carrito': productos_carrito, 'total_carrito': total_carrito})


def agregar_carrito(request):
    print("Intentando agregar al carrito")
    print(request.POST)
    
    id_producto = request.POST['id_producto']
    c_cant_compra = int(request.POST['cantidad'])
    c_subtotal = float(request.POST['subtotal'])

    try:
        producto = Producto.objects.get(id_producto=id_producto)
    except Producto.DoesNotExist:
        print("Producto no encontrado")
        return redirect('productos')
    
    carrito, created = Carrito.objects.get_or_create(activo=True)
    carro_producto = CarritoProducto.objects.filter(carrito=carrito, producto=producto).first()

    if carro_producto:
        carro_producto.cant_compra = c_cant_compra
        carro_producto.subtotal = carro_producto.cant_compra * producto.precio
        carro_producto.total_carro = carro_producto.subtotal
        carro_producto.save()
        print("Producto actualizado en el carrito")
    else:
        carro_producto = CarritoProducto.objects.create(
            carrito=carrito,
            producto=producto,
            cant_compra=c_cant_compra,
            subtotal=c_subtotal,
            total_carro=c_subtotal
        )
        print("Producto guardado en CarritoProducto")
    productos_carrito = CarritoProducto.objects.filter(carrito=carrito)
    if carrito:
        productos_carrito = CarritoProducto.objects.filter(carrito=carrito)
        total_carrito = sum(item.subtotal for item in productos_carrito)
    else:
        productos_carrito = []
        total_carrito = 0
    return render(request, 'carro_compra/carrito.html', {'productos_carrito': productos_carrito, 'total_carrito': total_carrito})


def pagar_compra(request):
    if request.method == "POST":
        productos_carrito = CarritoProducto.objects.all()

        if not productos_carrito.exists():
            return redirect('carrito')

        user_session = request.session.get("user")
        usuario = None
        if user_session:
            try:
                usuario = Usuario.objects.get(nom_usuario=user_session.split()[0])
            except Usuario.DoesNotExist:
                pass

        total_compra = sum(item.subtotal for item in productos_carrito)

        venta = Venta.objects.create(
            fecha=datetime.now(),
            usuario=usuario,
            total=total_compra
        )
        
        for item in productos_carrito:
            producto = item.producto
            if producto.stock < item.cant_compra:
                return render(request, 'carro_compra/compra_exitosa.html', {
                    'productos_carrito': productos_carrito,
                    'total_carrito': sum(p.subtotal for p in productos_carrito),
                    'mensaje_error': f"No hay suficiente stock para {producto.nombre_prod}."
                })

            producto.stock -= item.cant_compra
            producto.save()

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item.cant_compra,
                subtotal=item.subtotal,
            )

        productos_carrito.delete()

        return render(request, 'carro_compra/compra_exitosa.html', {'venta': venta})


def compra_exitosa(request):
    return redirect(request, 'carro_compra/compra_exitosa.html')


#------------------------    SECCIÓN DE LOGUEO    ----------------------
def login(request):
    context = {}
    return render(request, "carro_compra/login.html", context)


def validar_login(request):
    print("Estoy en validar login")
    context = {}
    
    if request.method == "POST":
        print("Ingreso al POST")

        nom_usuario = request.POST["nom_usuario"]
        contraseña = request.POST["contraseña"]

        try:
            usuario = Usuario.objects.get(nom_usuario=nom_usuario)
            if usuario.contraseña == contraseña:
                request.session["user"] = f"{usuario.nombre} {usuario.apellido}"
                return redirect('base')
            else:
                context['mensaje'] = 'Contraseña incorrecta'
        except Usuario.DoesNotExist:
            context['mensaje'] = 'Usuario no encontrado'
    
    return render(request, 'carro_compra/login.html', context)
    

def cerrar_sesion(request):
    print("Hola estoy en cerrar sesión")
    if "user" in request.session:
        del request.session["user"]
        print("sesión cerrada")
        return render(request, 'carro_compra/cerrar_sesion.html')
    else:
        return redirect('base')
    
#------------------------------------------------------