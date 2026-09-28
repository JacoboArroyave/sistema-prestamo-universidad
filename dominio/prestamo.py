from dispositivo import Dispositivo
from estudiante import Estudiante

from dominio.estado_dispositivo import EstadoDispositivo
from dominio.estado_prestamo import EstadoPrestamo


class Prestamo:
    
    def __init__(
        self,
        id,
        estudiante: Estudiante,
        dispositivo: Dispositivo,
        fecha_prestamo,
        fecha_devolucion,
    ):
        self.id = id
        self.estudiante = estudiante
        self.dispositivo = dispositivo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.estado= EstadoPrestamo.ACTIVO

    def cambiar_estado(self, nuevo_estado:EstadoPrestamo):
        self.estado = nuevo_estado

    def procesar_devolucion(self, fecha_devolucion,estado_dispositivo:EstadoDispositivo):
        self.fecha_devolucion = fecha_devolucion
        dias_retraso = self.calcular_fecha_retraso()
        self.dispositivo.cambiar_estado(estado_dispositivo)
        costo_multa:int = 0
        if dias_retraso > 0:
            costo_multa= self.dispositivo.calcular_multa(dias_retraso)
        return costo_multa



    def calcular_fecha_retraso(self):
        dias_retraso = (self.fecha_devolucion - self.fecha_prestamo).days - self.dispositivo.maximo_dias
        return max(0,dias_retraso)
