import sqlite3

from dominio.estudiante import Estudiante


class EstudianteMapper:
    @staticmethod
    def a_entidad(fila: sqlite3.Row) -> Estudiante:
        return Estudiante(
            id=fila["id"],
            codigo=fila["codigo"],
            nombre=fila["nombre"]
        )
