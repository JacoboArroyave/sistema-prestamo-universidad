import sqlite3

from aplicacion.puertos.repositorio_multa import RepositorioMulta
from dominio.estado_multa import EstadoMulta
from dominio.multa import Multa


class RepositorioMultaSQLite(RepositorioMulta):
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self.conexion = conexion
        self._crear_tabla()

    def _crear_tabla(self) -> None:
        cursor = self.conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multas (
                id TEXT PRIMARY KEY,
                id_prestamo TEXT NOT NULL,
                valor REAL NOT NULL,
                estado TEXT NOT NULL,
                FOREIGN KEY (id_prestamo) REFERENCES prestamos(id)
            )
        """)
        self.conexion.commit()

    def guardar_multa(self, deuda: Multa) -> None:
        cursor = self.conexion.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO multas (id, id_prestamo, valor, estado) VALUES (?, ?, ?, ?)",
            (deuda.id, deuda.prestamo.id, deuda.valor, deuda.estado.value)
        )
        self.conexion.commit()

    def obtener_multa(self) -> list:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, id_prestamo, valor, estado FROM multas")
        return cursor.fetchall()

    def obtener_cantidad_multas_por_estudiante(self, id_estudiante: str) -> int:
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT COUNT(m.id) as cantidad 
            FROM multas m
            JOIN prestamos p ON m.id_prestamo = p.id
            WHERE p.id_estudiante = ? AND m.estado = ?
            """,
            (id_estudiante, EstadoMulta.MORA.value)
        )
        fila = cursor.fetchone()
        return fila["cantidad"] if fila else 0
