from aplicacion.puertos.repositorio_prestamo import RepositorioPrestamo
from dominio.estado_prestamo import EstadoPrestamo
from dominio.prestamo import Prestamo


class RepositorioPrestamoMemoria(RepositorioPrestamo):
    def __init__(self) -> None:
        self._prestamos: list[Prestamo] = []

    def guardar_prestamo(self, prestamo: Prestamo) -> None:
        self._prestamos.append(prestamo)

    def actualizar_prestamo(self, prestamo: Prestamo) -> None:
        for i, p in enumerate(self._prestamos):
            if p.id == prestamo.id:
                self._prestamos[i] = prestamo
                break

    def obtener_prestamo_por_estudiante_y_dispositivo(self, id_estudiante: str, id_prestamo: str) -> Prestamo | None:
        for p in self._prestamos:
            if p.estudiante.id == id_estudiante and p.dispositivo.id == id_prestamo and p.estado == EstadoPrestamo.ACTIVO:
                return p
        return None

    def obtener_cantidad_prestamos_activos_por_estudiante(self, id_estudiante: str) -> int:
        return sum(1 for p in self._prestamos if p.estudiante.id == id_estudiante and p.estado == EstadoPrestamo.ACTIVO)
