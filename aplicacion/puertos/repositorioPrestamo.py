from abc import ABC, abstractmethod


class RepositorioPrestamo(ABC):
    @abstractmethod
    def obtener_prestremas(self) -> list: ...
