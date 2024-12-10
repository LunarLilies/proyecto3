from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, CarritoProducto, Venta, DetalleVenta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer


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

        if request.user.is_authenticated:
            usuario = request.user
        else:
            usuario = None

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
    return render(request, 'carro_compra/compra_exitosa.html')


#------------------------    SECCIÓN DE LOGUEO    ----------------------
def login(request):
    context = {}
    return render(request, "carro_compra/login.html", context)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                "message": "Login exitoso",
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_html_view(request):
    print("estoy en login_html_view")
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect('base')
            else:
                error = "Cuenta desactivada."
        else:
            error = "Credenciales incorrectas."

    return render(request, 'carro_compra/login.html', {'error': error})


@login_required
def logout_html_view(request):
    logout(request)
    return render(request, 'carro_compra/logout.html')
#------------------------------------------------------


def quitar_del_carro(request, id_producto):
    try:
        carrito = Carrito.objects.get(activo=True)
        producto = get_object_or_404(Producto, id_producto=id_producto)
        carro_producto = CarritoProducto.objects.filter(carrito=carrito, producto=producto).first()
        
        if carro_producto:
            carro_producto.delete()
            print(f"Producto {id_producto} eliminado del carrito.")
        else:
            print(f"Producto {id_producto} no encontrado en el carrito.")
    except Carrito.DoesNotExist:
        print("No hay carrito activo.")
    
    return redirect('carrito')


# ---------- REGISTRO ------------

def registro(request):
    print("estoy en registro.HTML")
    return render(request, "carro_compra/registro.html")


def registro(request):
    print("estoy en registro.HTML")
    return render(request, "carro_compra/registro.html")


def validar_registro(request):
    print("Estoy en validar_registro")
    context = {}
    if request.method == "POST":
        print(request.POST) #imprimir lo del post.
        
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        if not all([username, first_name, last_name, password]):
            context["error"] = "Por favor, completa todos los campos."
            return render(request, "carro_compra/registro.html", context)

        nuevo_usuario = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        context["mensaje"] = "Usuario registrado con éxito"
        return render(request, "carro_compra/registro.html", context)

    return render(request, "carro_compra/registro.html", context)

