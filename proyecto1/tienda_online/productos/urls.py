from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('restar/<int:id>/', views.restar_producto, name='restar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),


]
