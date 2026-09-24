from abc import ABC, abstractmethod
from estado_dispositivo import EstadoDispositivo

class Dispositivo(ABC):
    
    def __init__(self, id, codigo, estado=EstadoDispositivo.DISPONIBLE):
        self.id = id
        self.codigo = codigo
        self.estado = estado
    
    @property
    @abstractmethod
    def tarifa_diaria(self):
        pass
    
    @property
    @abstractmethod
    def maximo_dias(self):
        pass
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado