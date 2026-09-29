from datetime import date, timedelta
from dominio.dispositivo import Dispositivo
from dominio.estado_dispositivo import EstadoDispositivo
from dominio.estado_prestamo import EstadoPrestamo
from dominio.estudiante import Estudiante

class Prestamo:

    def __init__(
        self,
        id,
        estudiante: Estudiante,
        dispositivo: Dispositivo,
        fecha_prestamo: date,
        fecha_devolucion: date | None = None,
    ):
        self.id = id
        self.estudiante = estudiante
        self.dispositivo = dispositivo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_maxima_devolucion = fecha_prestamo + timedelta(
            days=dispositivo.maximo_dias
        )

        self.fecha_devolucion = fecha_devolucion
        self.estado = EstadoPrestamo.ACTIVO

    def cambiar_estado(self, nuevo_estado: EstadoPrestamo):
        self.estado = nuevo_estado

    def procesar_devolucion(
        self, fecha_devolucion: date, estado_dispositivo: EstadoDispositivo | None
    ) -> int:
        self.fecha_devolucion = fecha_devolucion
        dias_retraso = self.calcular_fecha_retraso()
        self.dispositivo.actualizar_estado_por_devolucion(estado_dispositivo)
        
        costo_multa: int = 0
        if dias_retraso > 0:
            costo_multa = self.dispositivo.calcular_multa(dias_retraso)
        return costo_multa

    def calcular_fecha_retraso(self) -> int:
        if self.fecha_devolucion is None:
            raise ValueError(
                "La fecha de devolución no puede ser None al calcular el retraso."
            )

        dias_retraso = (self.fecha_devolucion - self.fecha_maxima_devolucion).days
        return max(0, dias_retraso)
    @property
    def validar_prestamo_activo(self)->bool:
        return self.estado == EstadoPrestamo.ACTIVO
