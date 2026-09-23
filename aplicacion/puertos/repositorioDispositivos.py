from abc import ABC, abstractmethod


class RepositorioDispositivos(ABC):
    @abstractmethod
    def obtener_dispositivos(self) -> list: ...
