from dominio.prestamo import Prestamo
from estado_multa import EstadoMulta

class Multa():    
    def __init__(self, id, prestamo:Prestamo, id_prestamo, valor):
        self.id = id
        self.prestamo = Prestamo
        self.valor = valor
        self.estado = EstadoMulta.MORA
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
