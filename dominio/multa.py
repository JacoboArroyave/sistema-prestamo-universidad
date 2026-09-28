
from dominio.estado_multa import EstadoMulta
from dominio.prestamo import Prestamo


class Multa:    
    def __init__(self, id, prestamo:Prestamo, valor):
        self.id = id
        self.prestamo = prestamo
        self.valor = valor
        self.estado = EstadoMulta.MORA
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
