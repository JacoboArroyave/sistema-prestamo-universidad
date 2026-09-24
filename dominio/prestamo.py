from estudiante import Estudiante
from dispositivo import Dispositivo

class Prestamo:
    
    def __init__(
        self,
        id,
        estudiante: Estudiante,
        dispositivo: Dispositivo,
        fecha_prestamo,
        fecha_devolucion=None
    ):
        self.id = id
        self.estudiante = estudiante
        self.dispositivo = dispositivo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

