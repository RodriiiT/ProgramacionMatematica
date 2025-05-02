
# Primero definimos las clases POO Para los programadores y las tareas:
class Programador:
    def __init__(self, id_programador, max_tareas):
        self.id = id_programador
        self.max_tareas = max_tareas

class Tarea:
    def __init__(self, id_tarea, programadores_requeridos):
        self.id = id_tarea
        self.programadores_requeridos = programadores_requeridos

# Pruba sencillo:
pedro = Programador(12,2)
print(pedro.id)