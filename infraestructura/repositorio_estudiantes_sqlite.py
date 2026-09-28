import sqlite3

from aplicacion.puertos.repositorio_estudiantes import RepositorioEstudiantes
from dominio.estudiante import Estudiante
from infraestructura.mappers.estudiante_mapper import EstudianteMapper


class RepositorioEstudiantesSQLite(RepositorioEstudiantes):
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self.conexion = conexion
        self._crear_tabla()

    def _crear_tabla(self) -> None:
        cursor = self.conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id TEXT PRIMARY KEY,
                codigo TEXT NOT NULL,
                nombre TEXT NOT NULL
            )
        """)
        self.conexion.commit()

    def obtener_estudiantes(self) -> list[Estudiante]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, codigo, nombre FROM estudiantes")
        filas = cursor.fetchall()
        return [EstudianteMapper.a_entidad(f) for f in filas]

    def obtener_estudiante_por_id(self, estudiante_id: str) -> Estudiante | None:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, codigo, nombre FROM estudiantes WHERE id = ?", (estudiante_id,))
        fila = cursor.fetchone()
        if fila:
            return EstudianteMapper.a_entidad(fila)
        return None

    def agregar_estudiante(self, estudiante: Estudiante) -> None:
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO estudiantes (id, codigo, nombre) VALUES (?, ?, ?)",
            (estudiante.id, estudiante.codigo, estudiante.nombre)
        )
        self.conexion.commit()
