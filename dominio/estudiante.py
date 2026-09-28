class Estudiante:
    
    def __init__(self, id, codigo, nombre):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
    def __str__(self):
        return f"Estudiante(id={self.id}, codigo={self.codigo}, nombre={self.nombre})"
