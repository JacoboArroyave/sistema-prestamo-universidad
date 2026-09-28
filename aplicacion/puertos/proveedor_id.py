
from abc import ABC, abstractmethod


class ProveedorId(ABC):
    @abstractmethod
    def generar_id(self) -> str:...
       

