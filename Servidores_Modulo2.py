import numpy as np
from scipy.optimize import linear_sum_assignment

#Clase Servidor
class Servidor:
    #Inicializando la clase Servidor
    def __init__(self, identificador, capacidad):
        self.identificador = identificador
        self.capacidad = capacidad
        self.capacidad_actual = 0
        self.solicitudes = []

    #Agrega una solicitud al servidor si hay capacidad suficiente
    def agregar_solicitud(self, solicitud):
        if self.capacidad_actual + solicitud.requerimientos <= self.capacidad:
            self.solicitudes.append(solicitud)
            self.capacidad_actual += solicitud.requerimientos
            print(f"✅ Solicitud {solicitud.id} agregada al servidor {self.identificador}")
            return True
        else:
            print(f"❌ No hay capacidad suficiente en el servidor {self.identificador} para la solicitud {solicitud.id}")
            return False

    #Muestra la informacion del servidor con la capacidad actual y las solicitudes pendientes
    def mostrar_informacion(self):
        ids = [s.id for s in self.solicitudes]
        return f"Servidor {self.identificador} | Carga: {self.capacidad_actual}/{self.capacidad} | Solicitudes: {ids}"

#Clase Solicitud
class Solicitud:
    #Inicializando la clase Solicitud
    def __init__(self, id, requerimientos, prioridad):
        self.id = id
        self.requerimientos = requerimientos
        self.prioridad = prioridad

    #Muestra la informacion de la solicitud con el identificador, los requerimientos y la prioridad
    def mostrar_informacion(self):
        return f"Solicitud {self.id} | Requerimientos: {self.requerimientos} | Prioridad: {self.prioridad}"


#Optimiza la asignacion de solicitudes a servidores
def asignar_optimo(servidores, solicitudes, matriz_costos):
    prioridades = np.array([s.prioridad for s in solicitudes])
    matriz_ajustada = matriz_costos - prioridades * 1000

    filas, columnas = linear_sum_assignment(matriz_ajustada)
    asignaciones = []

    for i, j in zip(filas, columnas):
        servidor = servidores[i]
        solicitud = solicitudes[j]
        if servidor.agregar_solicitud(solicitud):
            asignaciones.append((servidor.identificador, solicitud.id, matriz_costos[i, j]))
    return asignaciones

#Utilidades

def validacion_numero_entero(msg, minimo=1):
    #Pide un numero entero al usuario
    while True:
        try:
            valor = int(input(msg))
            if valor >= minimo:
                return valor
            print(f"Ingrese un número mayor o igual a {minimo}")
        except ValueError:
            print("Ingrese un numero entero")

def crear_servidores():
    n = validacion_numero_entero("Cantidad de servidores: ")
    return [Servidor(i, validacion_numero_entero(f"Capacidad del servidor {i}: ")) for i in range(n)]

def crear_solicitudes():
    n = validacion_numero_entero("Cantidad de solicitudes: ")
    return [Solicitud(i,
                      validacion_numero_entero(f"Tamaño de la solicitud {i}: "),
                      validacion_numero_entero(f"Prioridad de la solicitud {i} (1-5): "))
            for i in range(n)]

def ingresar_matriz_costos(servidores, solicitudes):
    matriz = np.zeros((len(servidores), len(solicitudes)))
    print("\nIngrese los tiempos (costos) de asignación:")
    for i, s in enumerate(servidores):
        for j, r in enumerate(solicitudes):
            matriz[i, j] = validacion_numero_entero(f"Servidor {s.identificador} → Solicitud {r.id}: ")
    return matriz

