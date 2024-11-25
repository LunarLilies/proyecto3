"""
URL configuration for ventas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from carro_compra import views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('carrito', views.carrito, name='carrito'),
    path('carro_compra/login', views.login, name='login'),
    path('producto/<int:id_producto>/', views.producto_seleccionado, name='producto_seleccionado'),
    path('carro_compra/productos/', views.productos, name='productos'),
    path('carro_compra/agregar_carrito', views.agregar_carrito, name='agregar_carrito'),
    path('pagar_compra/', views.pagar_compra, name='pagar_compra'),
    path('compra_exitosa/', views.compra_exitosa, name='compra_exitosa'),
    path('login/',views.login,name='login'),
    path('validar_login', views.validar_login, name='validar_login'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)