from abc import ABC, abstractmethod


class Notificador(ABC):
    @abstractmethod
    def enviar_mensaje(self, mensaje: str): ...
