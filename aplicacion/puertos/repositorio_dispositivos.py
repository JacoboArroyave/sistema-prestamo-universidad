from abc import ABC, abstractmethod

from ...dominio.dispositivo import Dispositivo


class RepositorioDispositivos(ABC):
    @abstractmethod
    def obtener_dispositivos(self) -> list: ...

    @abstractmethod
    def guardar_dispositivo(self, dispositivo: list[Dispositivo]) -> None: ...

    @abstractmethod
    def eliminar_dispositivo(self, dispositivo_id) -> None: ...

    @abstractmethod
    def obtener_dispositivo_por_id(self, dispositivo_id) -> Dispositivo: ...

    @abstractmethod
    def actualizar_dispositivo(self, dispositivo: Dispositivo) -> None: ...
