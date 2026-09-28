
from abc import ABC, abstractmethod

from dominio.prestamo import Prestamo


class RepositorioPrestamo(ABC):
    @abstractmethod
    def obtener_prestamo_por_estudiante_y_dispositivo(self,id_estudiante,id_prestamo) -> Prestamo: ...

    @abstractmethod
    def guardar_prestamo(self, prestamo:Prestamo) -> None: ...

    @abstractmethod
    def actualizar_prestamo(self, prestamo:Prestamo) -> None: ... 

    @abstractmethod
    def obtener_cantidad_prestamos_activos_por_estudiante(self,id_estudiante) -> int: ... 
