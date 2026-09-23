from abc import ABC, abstractmethod


class PRoveedorFecha(ABC):
    @abstractmethod
    def obtener_fecha_actual(self) -> str: ...
