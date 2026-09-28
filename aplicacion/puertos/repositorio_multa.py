from abc import ABC, abstractmethod


class RepositorioMulta(ABC):
    @abstractmethod
    def obtener_multa(self) -> list: ...
    @abstractmethod
    def guardar_multa(self, deuda): ...
    @abstractmethod
    def obtener_cantidad_multas_por_estudiante(self, id_estudiante) -> int: ...
