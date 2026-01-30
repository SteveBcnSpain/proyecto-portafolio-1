# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .carrito import Carrito
from django.contrib import messages
from django.db import transaction



def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'productos/carrito.html', {'carrito': carrito})

def agregar_al_carrito(request, id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=id)
    if producto.stock <= 0:
        messages.error(request, 'Producto sin stock')
        return redirect('lista_productos')
    carrito.agregar(producto)
    return redirect('ver_carrito')



def restar_producto(request, id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=id)
    carrito.restar(producto)
    return redirect('ver_carrito')

def eliminar_producto(request, id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=id)
    carrito.eliminar(producto)
    return redirect('ver_carrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('ver_carrito')

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {
        'productos': productos
    })
    
def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/detalle_producto.html', {
        'producto': producto
    })
    
def finalizar_compra(request):
    carrito = Carrito(request)

    if not carrito.carrito:
        return redirect('lista_productos')

    with transaction.atomic():
        for item in carrito.carrito.values():
            producto = Producto.objects.select_for_update().get(id=item['producto_id'])

            if producto.stock < item['cantidad']:
                messages.error(
                    request,
                    f'Stock insuficiente para {producto.nombre}'
                )
                return redirect('ver_carrito')

            producto.stock -= item['cantidad']
            producto.save()

    carrito.limpiar()
    messages.success(request, 'Compra realizada con éxito')

    return redirect('lista_productos')

    
