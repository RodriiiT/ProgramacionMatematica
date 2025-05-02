# Importar la librería para la solucion
import pulp

# Primero definimos las clases POO Para los programadores y las tareas:
class Programador:
    def __init__(self, id_programador, max_tareas):
        self.id = id_programador
        self.max_tareas = max_tareas

class Tarea:
    def __init__(self, id_tarea, programadores_requeridos):
        self.id = id_tarea
        self.programadores_requeridos = programadores_requeridos

# Después definimos una función donde permite el programa puede leer datos desde un archivo de txt:
"""
Para el caso de archivo de txt:
La primer linea te indica cantidad de programador y tarea
La segunda linea indica la capacidad maxima de tarea para cada programador
Después a partir en la tercer linea se muestra la costo combinado (desempeño + transporte) para cada programador
(Estos para entender bien como debe tener el formato de archivo txt)
"""
def leer_datos_desde_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            lineas = file.readlines()
            
            # Leer N y M (primera línea)
            N, M = map(int, lineas[0].strip().split())
            
            # Leer capacidades de programadores (segunda línea)
            capacidades = list(map(int, lineas[1].strip().split()))
            
            # Leer demandas de tareas (tercera línea)
            demandas = list(map(int, lineas[2].strip().split()))
            
            # Leer matriz de costos (resto de líneas)
            C = []
            for i in range(N):
                fila = list(map(float, lineas[3+i].strip().split()))
                C.append(fila)
                
            return N, M, capacidades, demandas, C
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

# Aqui empezamos definir el main y con su validacion
def main():
    while True:
        print(" Módulo de Asignación de Programadores a Tareas ")
        print()
        print("1. Ingresar datos manualmente")
        print("2. Cargar datos desde archivo TXT")
        print("3. Salir de programa")
        
        opcion = input("Seleccione una opción (1, 2 o 3): ")
        
        if opcion not in ['1', '2', '3']:
            print()
            print("¡Opción inválida! Por favor ingrese 1, 2 o 3.")
            print()
            continue
        
        if opcion == '1':
            # Ingreso manual
            N = int(input("Ingrese el número de programadores (N): "))
            M = int(input("Ingrese el número de tareas (M): "))
            
            programadores = [] #Aqui definimos una lista para Programador
            for i in range(N):
                max_tareas = int(input(f"Ingrese la capacidad máxima del programador {i}: "))
                programadores.append(Programador(i, max_tareas))
            
            tareas = []
            for j in range(M):
                programadores_requeridos = int(input(f"Ingrese los programadores requeridos para la tarea {j}: "))
                tareas.append(Tarea(j, programadores_requeridos))
            
            print()
            print("Ingrese la matriz de costos combinados (desempeño + transporte):")
            C = []
            for i in range(N):
                fila = list(map(float, input(f"Costos para el programador {i} (separados por espacio): ").split()))
                if len(fila) != M:
                    print(f"Error: Debe ingresar exactamente {M} costos.") #Si el caso que el usuario ingreso mal valor, se muestra este mensaje
                    return
                C.append(fila)
        elif opcion == '2':
            # Lectura desde archivo para los datos
            nombre_archivo = input("Ingrese el nombre del archivo TXT: ")
            datos = leer_datos_desde_archivo(nombre_archivo)
            if not datos:
                continue
            
            # Dando valores a los siguientes variables
            N, M, capacidades, demandas, C = datos
            
            programadores = []
            for i in range(N):
                programadores.append(Programador(i, capacidades[i]))
            
            tareas = []
            for j in range(M):
                tareas.append(Tarea(j, demandas[j]))
        else:
            print("Saliendo el programa......")
            print("¡Hasta Luego!")
            break

        # Verificar factibilidad
        if sum(p.max_tareas for p in programadores) < sum(t.programadores_requeridos for t in tareas):
            print("\n¡Error! La capacidad total es menor que la demanda.")
            continue

        # Dando la Solución Óptima con PuLP
        problema = pulp.LpProblem("Asignacion_Optima", pulp.LpMinimize)
        x = pulp.LpVariable.dicts("Asignacion", ((p.id, t.id) for p in programadores for t in tareas), lowBound=0, cat='Integer')
        problema += pulp.lpSum(C[p.id][t.id] * x[p.id, t.id] for p in programadores for t in tareas)
        
        for p in programadores:
            problema += pulp.lpSum(x[p.id, t.id] for t in tareas) <= p.max_tareas
        
        for t in tareas:
            problema += pulp.lpSum(x[p.id, t.id] for p in programadores) == t.programadores_requeridos
        
        problema.solve()
        
        print(" Solución Óptima en Pulp")
        print()
        if pulp.LpStatus[problema.status] == 'Optimal':
            costo_optimo = 0
            for p in programadores:
                for t in tareas:
                    if x[p.id, t.id].value() > 0:
                        cantidad = int(x[p.id, t.id].value())
                        costo = cantidad * C[p.id][t.id]
                        print(f"  - Programador {p.id} → Tarea {t.id}: {cantidad} unidad(es) | Costo: {costo}")
                        costo_optimo += costo
            print(f"\nCosto total óptimo: {costo_optimo}")
        else:
            print("No se encontró solución óptima.")

        # Preguntar si desea continuar
        continuar = input("\n¿Desea realizar otra asignación? (s/n): ").lower()
        if continuar != 's':
            print("¡Hasta luego!")
            break

# Una vez ha definido el main, llamamos para ejecutarlo
main()