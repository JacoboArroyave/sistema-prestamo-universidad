import sqlite3

from aplicacion.puertos.repositorio_dispositivos import RepositorioDispositivos
from dominio.dispositivo import Dispositivo
from infraestructura.mappers.dispositivo_mapper import DispositivoMapper


class RepositorioDispositivosSQLite(RepositorioDispositivos):
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self.conexion = conexion
        self._crear_tabla()

    def _crear_tabla(self) -> None:
        cursor = self.conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispositivos (
                id TEXT PRIMARY KEY,
                codigo TEXT NOT NULL,
                estado TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """)
        self.conexion.commit()

    def obtener_dispositivos(self) -> list[Dispositivo]:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, codigo, estado, tipo FROM dispositivos")
        filas = cursor.fetchall()
        return [DispositivoMapper.a_entidad(f) for f in filas]

    def guardar_dispositivo(self, dispositivo: Dispositivo) -> None:
            cursor = self.conexion.cursor()
            tipo_str = DispositivoMapper.obtener_tipo_str(dispositivo)
            cursor.execute(
                "INSERT OR REPLACE INTO dispositivos (id, codigo, estado, tipo) VALUES (?, ?, ?, ?)",
                (dispositivo.id, dispositivo.codigo, dispositivo.estado.value, tipo_str)
            )
            self.conexion.commit()

    def obtener_dispositivo_por_id(self, dispositivo_id: str) -> Dispositivo | None:
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, codigo, estado, tipo FROM dispositivos WHERE id = ?", (dispositivo_id,))
        fila = cursor.fetchone()
        if fila:
            return DispositivoMapper.a_entidad(fila)
        return None

    def actualizar_dispositivo(self, dispositivo: Dispositivo) -> None:
        cursor = self.conexion.cursor()
        cursor.execute(
            "UPDATE dispositivos SET estado = ? WHERE id = ?",
            (dispositivo.estado.value, dispositivo.id)
        )
        self.conexion.commit()

    def eliminar_dispositivo(self, dispositivo_id: str) -> None:
        cursor = self.conexion.cursor()
        cursor.execute("DELETE FROM dispositivos WHERE id = ?", (dispositivo_id,))
        self.conexion.commit()
