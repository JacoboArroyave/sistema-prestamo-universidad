import sqlite3
from datetime import date
from dominio.estado_prestamo import EstadoPrestamo
from dominio.dispositivo import Dispositivo
from dominio.estudiante import Estudiante
from dominio.prestamo import Prestamo


class PrestamoMapper:
    @staticmethod
    def a_entidad(
        fila: sqlite3.Row, 
        estudiante: Estudiante, 
        dispositivo: Dispositivo
    ) -> Prestamo:
        fecha_p = date.fromisoformat(fila["fecha_prestamo"])
        fecha_d = date.fromisoformat(fila["fecha_devolucion"]) if fila["fecha_devolucion"] else None

        prestamo = Prestamo(
            id=fila["id"],
            estudiante=estudiante,
            dispositivo=dispositivo,
            fecha_prestamo=fecha_p,
            fecha_devolucion=fecha_d
        )
        prestamo.estado = EstadoPrestamo(fila["estado"])
        return prestamo
