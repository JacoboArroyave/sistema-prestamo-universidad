from abc import ABC, abstractmethod
from datetime import date


class ProveedorFecha(ABC):
    @abstractmethod
    def obtener_fecha_actual(self) -> date: ...
