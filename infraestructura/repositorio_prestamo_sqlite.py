import sqlite3

from aplicacion.puertos.repositorio_prestamo import RepositorioPrestamo
from dominio.prestamo import Prestamo
from infraestructura.mappers.prestamo_mapper import PrestamoMapper
from infraestructura.repositorio_dispositivos_sqlite import (
    RepositorioDispositivosSQLite,
)
from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite


class RepositorioPrestamoSQLite(RepositorioPrestamo):
    def __init__(
        self, 
        conexion: sqlite3.Connection,
        repo_estudiantes: RepositorioEstudiantesSQLite,
        repo_dispositivos: RepositorioDispositivosSQLite
    ) -> None:
        self.conexion = conexion
        self.repo_estudiantes = repo_estudiantes
        self.repo_dispositivos = repo_dispositivos
        self._crear_tabla()

    def _crear_tabla(self) -> None:
        cursor = self.conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id TEXT PRIMARY KEY,
                id_estudiante TEXT NOT NULL,
                id_dispositivo TEXT NOT NULL,
                fecha_prestamo TEXT NOT NULL,
                fecha_maxima_devolucion TEXT NOT NULL,
                fecha_devolucion TEXT,
                estado TEXT NOT NULL,
                FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),
                FOREIGN KEY (id_dispositivo) REFERENCES dispositivos(id)
            )
        """)
        self.conexion.commit()

    def guardar_prestamo(self, prestamo: Prestamo) -> None:
        cursor = self.conexion.cursor()
        fecha_dev = prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
        
        cursor.execute(
            """
            INSERT OR REPLACE INTO prestamos 
            (id, id_estudiante, id_dispositivo, fecha_prestamo, fecha_maxima_devolucion, fecha_devolucion, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                prestamo.id,
                prestamo.estudiante.id,
                prestamo.dispositivo.id,
                prestamo.fecha_prestamo.isoformat(),
                prestamo.fecha_maxima_devolucion.isoformat(),  # Se extrae de la propiedad calculada
                fecha_dev,
                prestamo.estado.value
            )
        )
        self.conexion.commit()

    def actualizar_prestamo(self, prestamo: Prestamo) -> None:
        cursor = self.conexion.cursor()
        fecha_dev = prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else None
        cursor.execute(
            "UPDATE prestamos SET fecha_devolucion = ?, estado = ? WHERE id = ?",
            (fecha_dev, prestamo.estado.value, prestamo.id)
        )
        self.conexion.commit()

    def obtener_prestamo_por_estudiante_y_dispositivo(
        self, id_estudiante: str, id_dispositivo: str
    ) -> Prestamo | None:
        cursor = self.conexion.cursor()
        cursor.execute(
            """
            SELECT id, id_estudiante, id_dispositivo, fecha_prestamo, fecha_maxima_devolucion, fecha_devolucion, estado 
            FROM prestamos 
            WHERE id_estudiante = ? AND id_dispositivo = ? AND estado = 'Activo'
            """,
            (id_estudiante, id_dispositivo)  # Cambiado id_prestamo por id_dispositivo
        )
        fila = cursor.fetchone()
        if not fila:
            return None

        estudiante = self.repo_estudiantes.obtener_estudiante_por_id(fila["id_estudiante"])
        dispositivo = self.repo_dispositivos.obtener_dispositivo_por_id(fila["id_dispositivo"])

        if estudiante is None or dispositivo is None:
            return None

        return PrestamoMapper.a_entidad(fila, estudiante, dispositivo)

    def obtener_cantidad_prestamos_activos_por_estudiante(self, id_estudiante: str) -> int:
        cursor = self.conexion.cursor()
        cursor.execute(
            "SELECT COUNT(*) as cantidad FROM prestamos WHERE id_estudiante = ? AND estado = 'Activo'",
            (id_estudiante,)
        )
        fila = cursor.fetchone()
        return fila["cantidad"] if fila else 0