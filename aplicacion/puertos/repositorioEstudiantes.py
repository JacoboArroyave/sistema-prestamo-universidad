from abc import ABC, abstractmethod


class RepositorioEstudiantes(ABC):
    @abstractmethod
    def obtener_estudiantes(self) -> list: ...
