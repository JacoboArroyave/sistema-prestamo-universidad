from abc import ABC, abstractmethod

from dominio.estudiante import Estudiante


class RepositorioEstudiantes(ABC):
    @abstractmethod
    def obtener_estudiantes(self) -> list[Estudiante]: ...
    @abstractmethod
    def obtener_estudiante_por_id(self, estudiante_id) -> Estudiante: ...
    @abstractmethod
    def agregar_estudiante(self, estudiante: Estudiante): ...
