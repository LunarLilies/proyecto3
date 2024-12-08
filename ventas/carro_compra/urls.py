from django.urls import path, include
from . import views

# DRF
from carro_compra.views import LoginView, login_html_view, logout_html_view # , home_view

urlpatterns = [
    # URLs del login
    path('login/', LoginView.as_view(), name='login'),
    path('login-html/', login_html_view, name='login_html'),
    path('logout-html/', logout_html_view, name='logout_html'),
    # path('base/', home_view, name='home_view'),

    path('', views.base, name='base'),
    path('base/', views.base, name='base'),
    path('carrito/', views.carrito, name='carrito'),
    path('carro_compra/login/', views.login, name='login'),
    path('producto/<int:id_producto>/', views.producto_seleccionado, name='producto_seleccionado'),
    path('carro_compra/productos/', views.productos, name='productos'),
    path('carro_compra/agregar_carrito/', views.agregar_carrito, name='agregar_carrito'),
    path('pagar_compra/', views.pagar_compra, name='pagar_compra'),
    path('compra_exitosa/', views.compra_exitosa, name='compra_exitosa'),
    path('quitar_del_carro/<int:id_producto>/', views.quitar_del_carro, name='quitar_del_carro'),
    path('registro/', views.registro, name="registro"),
    path('validar_registro/', views.validar_registro, name='validar_registro'),
]
