def leer_matriz_consola(n, m):
    print(f"Ingrese la matriz de costos {n}x{m} separada por espacios y luego de finalizar la fila presione enter para seguir a la siguinete fila:")
    matriz = []
    for i in range(n):
        fila = list(map(int, input().split()))
        if len(fila) != m:
            raise ValueError("Número incorrecto de elementos en la fila.")
        matriz.append(fila)
    return matriz

def leer_matriz_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        lineas = f.readlines()
    matriz = []
    for linea in lineas:
        fila = list(map(int, linea.strip().split()))
        matriz.append(fila)
    return matriz

def asignacion_optima(matriz_costos):
    n = len(matriz_costos)
    m = len(matriz_costos[0]) if n > 0 else 0
    asignaciones = []
    costos = []
    total = 0

    for tarea in range(m):
        min_costo = float('inf')
        programador_elegido = -1
        for programador in range(n):
            if matriz_costos[programador][tarea] < min_costo:
                min_costo = matriz_costos[programador][tarea]
                programador_elegido = programador
        asignaciones.append((programador_elegido, tarea))
        costos.append(min_costo)
        total += min_costo

    return asignaciones, total

def main():
    entrada = input("¿Desea ingresar datos por consola o archivo? (c/a): ").strip().lower()
    if entrada == 'a':
        nombre_archivo = input("Ingrese el nombre del archivo: ")
        matriz = leer_matriz_archivo(nombre_archivo)
    else:
        n = int(input("Número de programadores: "))
        m = int(input("Número de tareas: "))
        matriz = leer_matriz_consola(n, m)
        n = len(matriz)
        m = len(matriz[0]) if n > 0 else 0

    asignaciones, total = asignacion_optima(matriz)

    print("\nAsignación óptima:")
    for prog, tarea in asignaciones:
        print(f"Tarea {tarea} -> Programador {prog} (Costo: {matriz[prog][tarea]})")
    print(f"\nCosto total: {total}")

if __name__ == "__main__":
    main()