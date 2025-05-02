
# Primero definimos las clases POO Para los programadores y las tareas:
class Programador:
    def __init__(self, id_programador, max_tareas):
        self.id = id_programador
        self.max_tareas = max_tareas

class Tarea:
    def __init__(self, id_tarea, programadores_requeridos):
        self.id = id_tarea
        self.programadores_requeridos = programadores_requeridos

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
            print("Opcion 1")
            break
        elif opcion == '2':
            print("Opcion 2")
            break
        else:
            print("Saliendo el programa......")
            print("¡Hasta Luego!")
            break

# Una vez ha definido el main, llamamos para ejecutarlo
main()