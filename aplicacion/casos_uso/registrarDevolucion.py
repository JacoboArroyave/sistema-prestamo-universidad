
from aplicacion.puertos.notificador import Notificador
from aplicacion.puertos.proveedor_fecha import ProveedorFecha
from aplicacion.puertos.proveedor_id import ProveedorId
from aplicacion.puertos.repositorio_dispositivos import RepositorioDispositivos
from aplicacion.puertos.repositorio_estudiantes import RepositorioEstudiantes
from aplicacion.puertos.repositorio_multa import RepositorioMulta
from aplicacion.puertos.repositorio_prestamo import RepositorioPrestamo
from dominio.estado_dispositivo import EstadoDispositivo
from dominio.multa import Multa
from dominio.prestamo import Prestamo


class RegistrarDevolucion:
    def __init__( self,notificador:Notificador,proveedor_id:ProveedorId,repositorioPrestamo:RepositorioPrestamo, repositorio_estudiantes: RepositorioEstudiantes, repositorio_dispositivos: RepositorioDispositivos, proveedor_fecha: ProveedorFecha, proveedor_multa: RepositorioMulta):
        self.repositorio_estudiantes: RepositorioEstudiantes = repositorio_estudiantes
        self.repositorio_dispositivos: RepositorioDispositivos =  repositorio_dispositivos
        self.proveedor_fecha: ProveedorFecha = proveedor_fecha
        self.repositorio_multa: RepositorioMulta= proveedor_multa
        self.repositorio_prestamos:RepositorioPrestamo=repositorioPrestamo
        self.proveedor_id:ProveedorId=proveedor_id
        self.notificador:Notificador =notificador

    def registrar_devolucion(self, id_estudiante: str, id_dispositivo: str,estado_dispositivo:EstadoDispositivo | None= None):
        prestamo:Prestamo= self.repositorio_prestamos.obtener_prestamo_por_estudiante_y_dispositivo(id_estudiante, id_dispositivo)
        if prestamo is None:
            raise ValueError("No se encontró un préstamo activo para este estudiante y dispositivo")
        valor_multa = prestamo.procesar_devolucion(self.proveedor_fecha.obtener_fecha_actual(),estado_dispositivo)
        if valor_multa > 0 :
            multa: Multa = Multa(id=self.proveedor_id.generar_id(), prestamo=prestamo, valor=valor_multa)
            self.repositorio_multa.guardar_multa(multa)
            self.notificador.enviar_mensaje("Prueba mensaje de caso de uso devolver prestamo cambiar este mensaje por uno mas elaborado con una funcion ")
        self.repositorio_prestamos.actualizar_prestamo(prestamo)
        self.repositorio_dispositivos.actualizar_dispositivo(prestamo.dispositivo)


