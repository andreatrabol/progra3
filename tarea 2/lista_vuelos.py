class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaVuelos:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0



    def insertar_al_frente(self, vuelo):
        nuevo = Nodo(vuelo)
        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            nuevo.siguiente = self.head
            self.head.anterior = nuevo
            self.head = nuevo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nuevo = Nodo(vuelo)
        if self.tail is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            self.tail.siguiente = nuevo
            nuevo.anterior = self.tail
            self.tail = nuevo
        self.size += 1


    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)
        elif posicion >= self.size:
            self.insertar_al_final(vuelo)
        else:
            nuevo = Nodo(vuelo)
            actual = self.head
            for _ in range(posicion):
                actual = actual.siguiente
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self.size += 1

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.size:
            return None
        if posicion == 0:
            vuelo = self.head.vuelo
            self.head = self.head.siguiente
            if self.head:
                self.head.anterior = None
            else:
                self.tail = None
        elif posicion == self.size - 1:
            vuelo = self.tail.vuelo
            self.tail = self.tail.anterior
            if self.tail:
                self.tail.siguiente = None
            else:
                self.head = None
        else:
            actual = self.head
            for _ in range(posicion):
                actual = actual.siguiente
            vuelo = actual.vuelo
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior
        self.size -= 1
        return vuelo
    
    def mostrar(self):  
        vuelos = []
        actual = self.head
        while actual:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos
    
    
    def obtener_primero(self):
        return self.head.vuelo if self.head else None

    def obtener_ultimo(self):
        return self.tail.vuelo if self.tail else None

    def longitud(self):
        return self.size



class GestorAcciones:
    def __init__(self):
        self.historial = []
        self.redo_stack = []

    def hacer(self, accion, dato, posicion=None):
        self.historial.append((accion, dato, posicion))
        self.redo_stack.clear()

    def deshacer(self, lista_vuelos):
        if not self.historial:
            return "Nada que deshacer."
        accion, dato, posicion = self.historial.pop()
        if accion == "agregar":
            lista_vuelos.extraer_de_posicion(posicion)
            self.redo_stack.append(("agregar", dato, posicion))
        elif accion == "eliminar":
            lista_vuelos.insertar_en_posicion(dato, posicion)
            self.redo_stack.append(("eliminar", dato, posicion))
        return "Acción deshecha."

    def rehacer(self, lista_vuelos):
        if not self.redo_stack:
            return "Nada que rehacer."
        accion, dato, posicion = self.redo_stack.pop()
        if accion == "agregar":
            lista_vuelos.insertar_en_posicion(dato, posicion)
            self.historial.append(("agregar", dato, posicion))
        elif accion == "eliminar":
            lista_vuelos.extraer_de_posicion(posicion)
            self.historial.append(("eliminar", dato, posicion))
        return "Acción rehecha."
    
    def mostrar(self):  
        vuelos = []
        actual = self.head
        while actual:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos