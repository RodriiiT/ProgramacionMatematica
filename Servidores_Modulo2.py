# Importación de bibliotecas necesarias
import numpy as np
from scipy.optimize import linear_sum_assignment

# Clase que representa un servidor con capacidad y manejo de solicitudes
class Servidor:
    #Inicializando la clase Servidor
    def __init__(self, identificador, capacidad):
        self.identificador = identificador
        self.capacidad = capacidad
        self.capacidad_actual = 0
        self.solicitudes = []

    # Método para agregar una solicitud al servidor si hay espacio disponible
    def agregar_solicitud(self, solicitud):
        if self.capacidad_actual + solicitud.requerimientos <= self.capacidad:
            self.solicitudes.append(solicitud)
            self.capacidad_actual += solicitud.requerimientos
            print(f"✅ Solicitud {solicitud.id} agregada al servidor {self.identificador}")
            return True
        else:
            print(f"❌ No hay capacidad suficiente en el servidor {self.identificador} para la solicitud {solicitud.id}")
            return False

    # Método para mostrar el estado actual del servidor
    def mostrar_informacion(self):
        ids = [s.id for s in self.solicitudes]
        return f"Servidor {self.identificador} | Carga: {self.capacidad_actual}/{self.capacidad} | Solicitudes: {[ id for id in ids]}"

# Clase que representa una solicitud con sus características
class Solicitud:
    #Inicializando la clase Solicitud
    def __init__(self, id, requerimientos, prioridad):
        self.id = id
        self.requerimientos = requerimientos
        self.prioridad = prioridad

    # Método para mostrar los detalles de la solicitud
    def mostrar_informacion(self):
        return f"Solicitud {self.id} | Requerimientos: {self.requerimientos} | Prioridad: {self.prioridad}"

# Función que optimiza la asignación de solicitudes a servidores usando el algoritmo húngaro
def asignar_optimo(servidores, solicitudes, matriz_costos):
    # Ajusta la matriz de costos considerando las prioridades
    prioridades = np.array([s.prioridad for s in solicitudes])
    matriz_ajustada = matriz_costos - prioridades * 1000

    # Encuentra la asignación óptima usando el algoritmo húngaro
    filas, columnas = linear_sum_assignment(matriz_ajustada)
    asignaciones = []

    # Procesa las asignaciones encontradas
    for i, j in zip(filas, columnas):
        servidor = servidores[i]
        solicitud = solicitudes[j]
        if servidor.agregar_solicitud(solicitud):
            asignaciones.append((servidor.identificador, solicitud.id, matriz_costos[i, j]))
    return asignaciones

# Función para validar entrada de números enteros
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

# Función para crear servidores con sus capacidades
def crear_servidores():
    n = validacion_numero_entero("Cantidad de servidores: ")
    return [Servidor(i, validacion_numero_entero(f"Capacidad del servidor {i}: ")) for i in range(n)]

# Función para crear solicitudes con sus requerimientos y prioridades
def crear_solicitudes():
    n = validacion_numero_entero("Cantidad de solicitudes: ")
    return [Solicitud(i,
                      validacion_numero_entero(f"Tamaño de la solicitud {i}: "),
                      validacion_numero_entero(f"Prioridad de la solicitud {i} (1-5): "))
            for i in range(n)]

# Función para ingresar la matriz de costos de asignación
def ingresar_matriz_costos(servidores, solicitudes):
    matriz = np.zeros((len(servidores), len(solicitudes)))
    print("\nIngrese los tiempos (costos) de asignación:")
    for i, s in enumerate(servidores):
        for j, r in enumerate(solicitudes):
            matriz[i, j] = validacion_numero_entero(f"Servidor {s.identificador} → Solicitud {r.id}: ")
    return matriz

# Función que carga datos de ejemplo predefinidos
def cargar_datos_ejemplo():
    servidores = [Servidor(0, 10), Servidor(1, 8), Servidor(2, 6)]
    for s in servidores:
        print(s.mostrar_informacion())
    solicitudes = [Solicitud(0, 3, 2),Solicitud(1, 2, 1),Solicitud(2, 4, 3),Solicitud(3, 1, 2)]
    for r in solicitudes:
        print(r.mostrar_informacion())
    matriz_costos = np.array([[10, 12, 9, 8],[7, 9, 11, 5],[8, 7, 6, 9]])
    return servidores, solicitudes, matriz_costos

# Función que muestra el menú principal y obtiene la opción del usuario
def menu():
    print("\n###### ASIGNADOR ÓPTIMO DE SOLICITUDES ######")
    print("1. Usar datos de ejemplo")
    print("2. Ingresar datos manualmente")
    while True:
        opcion = input("Seleccione una opción (1 o 2): ")
        if opcion in ("1", "2"):
            return opcion
        print("Opción inválida. Intente de nuevo.")

# Función para preguntar si el usuario desea continuar
def desea_continuar():
    while True:
        respuesta = input("\n¿Desea realizar otra asignación? (s/n): ").lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta no válida. Escriba 's' o 'n'.")

# Función principal que ejecuta el programa
def main():
    continuar = True
    while continuar:
        opcion = menu()
        if opcion == "1":
            servidores, solicitudes, matriz = cargar_datos_ejemplo()
        else:
            servidores = crear_servidores()
            solicitudes = crear_solicitudes()
            matriz = ingresar_matriz_costos(servidores, solicitudes)

        # Realiza la asignación óptima y muestra los resultados
        asignaciones = asignar_optimo(servidores, solicitudes, matriz)

        print("\n--- Resultados de la Asignación ---")
        for id_servidor, id_solicitud, costo in asignaciones:
            print(f"Servidor {id_servidor} → Solicitud {id_solicitud} | Tiempo: {costo}")

        print("\n--- Estado Final de los Servidores ---")
        for servidor in servidores:
            print(servidor.mostrar_informacion())

        print("\nTiempo total:", sum(costo for _, _, costo in asignaciones))

        continuar = desea_continuar()
    #Salida del programa
    print("\n👋 Programa finalizado.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
