#Modulo 2: Servidores y Solicitudes

#Clase Servidor
class Servidor:
    #Inicializando la clase Servidor con los atributos: identificador, capacidad, solicitudes y capacidad_actual
    def __init__(self, identificador, capacidad):
        self.identificador = identificador
        self.capacidad = capacidad
        self.solicitudes = []
        self.capacidad_actual = 0

    def mostrar_informacion(self):
        #Muestra la informacion del servidor con la capacidad actual y las solicitudes pendientes
        return f"Servidor {self.identificador} | Carga actual: {self.capacidad_actual} de {self.capacidad}\nSolicitudes: {[solicitud.id for solicitud in self.solicitudes]}"

    def agregar_solicitud(self, solicitud):
        #Agrega una solicitud al servidor si hay capacidad suficiente
        if self.capacidad_actual + solicitud.tamaño <= self.capacidad:
            self.solicitudes.append(solicitud)
            self.capacidad_actual += solicitud.tamaño
            return print(f"Solicitud {solicitud.id} agregada al servidor {self.identificador}")
        else:
            return print(f"No hay capacidad suficiente en el servidor {self.identificador} para agregar la solicitud {solicitud.id}")



#Clase Solicitud
class Solicitud:
    #Inicializando la clase Solicitud con los atributos: identificador, tamaño
    def __init__(self, id, requerimientos, prioridad):
        self.id = id
        self.requerimientos = requerimientos
        self.prioridad = prioridad

    def mostrar_informacion(self):
        #Muestra la informacion de la solicitud con el identificador, los requerimientos y la prioridad
        return f"Solicitud {self.id} | Requerimientos: {self.requerimientos} | Prioridad: {self.prioridad}"



















