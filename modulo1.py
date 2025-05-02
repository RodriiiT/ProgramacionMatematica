def leer_matriz_consola(n, m):
    print(f"Ingrese la matriz de costos {n}x{m} separada por espacios y luego de finalizar la fila presione enter para seguir a la siguinete fila:")
    matriz = []
    for i in range(n):
        fila = list(map(int, input().split()))
        if len(fila) != m:
            raise ValueError("Número incorrecto de elementos en la fila.")
        matriz.append(fila)
    return matriz

def leer_vectores_consola(n, m):
    print("\nIngrese el vector S (capacidad de programadores):")
    S = list(map(int, input(f"{n} valores separados por espacios: ").split()))
    if len(S) != n:
        raise ValueError("Longitud de S incorrecta")
    
    print("\nIngrese el vector D (requerimientos de tareas):")
    D = list(map(int, input(f"{m} valores separados por espacios: ").split()))
    if len(D) != m:
        raise ValueError("Longitud de D incorrecta")
    
    return S, D

def leer_datos_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        lineas = [linea.strip() for linea in f.readlines() if linea.strip()]
    
    #Leer matriz
    matriz = []
    i = 0
    while i < len(lineas) and lineas[i] != 'S':
        matriz.append(list(map(int, lineas[i].split())))
        i += 1
    
    #Leer vector S
    i += 1
    S = list(map(int, lineas[i].split()))
    
    #Leer vector D
    i += 1
    D = list(map(int, lineas[i].split()))
    
    return matriz, S, D

def asignacion_optima(matriz_costos, S, D):
    n = len(matriz_costos)
    m = len(matriz_costos[0]) if n > 0 else 0
    
    if sum(S) < sum(D):
        raise ValueError("No hay suficiente capacidad total de programadores")
    
    asignaciones = [[] for _ in range(n)]  #Lista de tuplas (tarea, cantidad)
    programadores_usados = [0] * n
    
    #Ordenar tareas por requerimiento descendente
    tareas_ordenadas = sorted(enumerate(D), key=lambda x: -x[1])
    
    for tarea_idx, requerimiento in tareas_ordenadas:
        #Obtener programadores disponibles ordenados por costo ascendente
        candidatos = sorted(
            [(prog, matriz_costos[prog][tarea_idx]) 
             for prog in range(n) 
             if programadores_usados[prog] < S[prog]],
            key=lambda x: x[1]
        )
        
        asignados = 0
        for prog, costo_unitario in candidatos:
            disponible = S[prog] - programadores_usados[prog]
            asignar = min(requerimiento - asignados, disponible)
            
            if asignar > 0:
                asignaciones[prog].append((tarea_idx, asignar))
                programadores_usados[prog] += asignar
                asignados += asignar
            
            if asignados >= requerimiento:
                break
        
        if asignados < requerimiento:
            raise ValueError(f"No se puede cumplir la tarea {tarea_idx}")
    
    #Calcular costo total correctamente
    costo_total = sum(
        matriz_costos[prog][tarea] * cantidad 
        for prog in range(n) 
        for (tarea, cantidad) in asignaciones[prog]
    )
    
    return asignaciones, costo_total
    
def main():
     while True:
        cent = input("¿Desea continuar (s/n): ").lower()
        while cent not in ("s", "n"):
            print("Por favor ingrese un cáracter válido")
            cent = input("¿Desea continuar (s/n): ").lower()
            
        if cent == "n":
            print("Saliendo...")
            break
        else:
            #Entrada
            entrada = input("¿Desea ingresar datos por consola o archivo? (c/a): ").strip().lower()
            while entrada not in ("c", "a"):
                print("Entrada inválida, por favor ingrese un carácter válido")
                entrada = input("¿Desea ingresar datos por consola o archivo? (c/a): ").strip().lower()
            
            if entrada == "a":
                try: 
                    nombre_archivo = input("Ingrese el nombre del archivo: ")
                    matriz, S, D = leer_datos_archivo(nombre_archivo)
                except FileNotFoundError:
                    print("El archivo no fue encontrado")
                    continue
            else:
                try:
                    n = int(input("Número de programadores: "))
                    m = int(input("Número de tareas: "))
                    matriz = leer_matriz_consola(n, m)
                    S, D = leer_vectores_consola(n, m)
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
                
            try:
                asignaciones, total = asignacion_optima(matriz, S, D)
                
                print("\nAsignación óptima:")
                for prog in range(len(asignaciones)):
                    for tarea, cantidad in asignaciones[prog]:
                        print(f"Programador {prog} -> Tarea {tarea} (x{cantidad}, Costo: {matriz[prog][tarea] * cantidad})")
                print(f"\nCosto total: {total}")
                
            except ValueError as e:
                print(f"\nError: {e}")

if __name__ == "__main__":
    main() 