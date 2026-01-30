from decimal import Decimal
from productos.models import Producto

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] += cantidad
        else:
            self.carrito[producto_id] = {'precio': str(producto.precio), 'cantidad': cantidad}
        self.guardar()
        
    def restar(self, producto):
        id_producto = str(producto.id)
        
        if id_producto in self.carrito:
            self.carrito[id_producto]['cantidad'] -= 1

            if self.carrito[id_producto]['cantidad'] <= 0:
                self.eliminar(producto)

        self.guardar()


    def guardar(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True
    
    def guardar(self):
        self.session.modified = True

    def __iter__(self):
        productos_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=productos_ids)

        for producto in productos:
            self.carrito[str(producto.id)]['producto'] = producto

        for item in self.carrito.values():
            item['precio'] = Decimal(item['precio'])
            item['total'] = item['precio'] * item['cantidad']
            yield item

    def total_carrito(self):
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.carrito.values()
        )
