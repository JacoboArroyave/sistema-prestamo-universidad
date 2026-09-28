from aplicacion.puertos.repositorio_multa import RepositorioMulta
from dominio.estado_multa import EstadoMulta
from dominio.multa import Multa


class RepositorioMultaMemoria(RepositorioMulta):
    def __init__(self) -> None:
        self._multas: list[Multa] = []

    def guardar_multa(self, multa: Multa) -> None:
        self._multas.append(multa)

    def obtener_multa(self) -> list[Multa]:
        return self._multas

    def obtener_cantidad_multas_por_estudiante(self, id_estudiante: str) -> int:
        # Cuenta cuántas multas asociadas al estudiante están en estado MORA
        return sum(
            1 for m in self._multas 
            if m.prestamo.estudiante.id == id_estudiante and m.estado == EstadoMulta.MORA
        )