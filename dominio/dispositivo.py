from abc import ABC, abstractmethod

from dominio.estado_dispositivo import EstadoDispositivo


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
    def maximo_dias(self)->int:
        pass
    
    def calcular_multa(self, dias_retraso)->int :
        return dias_retraso * self.tarifa_diaria

    def cambiar_estado_en_uso(self):
        self.estado = EstadoDispositivo.EN_USO

    def es_disponible(self):
        return self.estado == EstadoDispositivo.DISPONIBLE

    def actualizar_estado_por_devolucion(self, nuevo_estado:EstadoDispositivo | None ):
        if nuevo_estado is None or nuevo_estado == EstadoDispositivo.EN_USO:
            self.estado = EstadoDispositivo.DISPONIBLE
        else:
            self.estado =EstadoDispositivo.EN_MANTENIMIENTO
