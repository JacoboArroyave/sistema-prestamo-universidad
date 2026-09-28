
from aplicacion.puertos.notificador import Notificador
from aplicacion.puertos.proveedor_fecha import ProveedorFecha
from aplicacion.puertos.proveedor_id import ProveedorId
from aplicacion.puertos.repositorio_dispositivos import RepositorioDispositivos
from aplicacion.puertos.repositorio_estudiantes import RepositorioEstudiantes
from aplicacion.puertos.repositorio_multa import RepositorioMulta
from aplicacion.puertos.repositorio_prestamo import RepositorioPrestamo
from dominio.dispositivo import Dispositivo
from dominio.estudiante import Estudiante
from dominio.prestamo import Prestamo


class RegistrarPrestamo:
    def __init__(self,notificador:Notificador,proveedor_fecha:ProveedorFecha,proveedor_id:ProveedorId,repositorio_prestamo:RepositorioPrestamo,repositorio_dispositivo:RepositorioDispositivos,repositorio_multa:RepositorioMulta,repositorio_estudiante:RepositorioEstudiantes):
        self.repositorio_prestamo:RepositorioPrestamo = repositorio_prestamo
        self.reprositorio_dispositivo :RepositorioDispositivos= repositorio_dispositivo
        self.reprositorio_multa:RepositorioMulta = repositorio_multa
        self.repositoorio_estudiante:RepositorioEstudiantes = repositorio_estudiante
        self.proveedor_fecha:ProveedorFecha = proveedor_fecha
        self.proveedor_id:ProveedorId = proveedor_id
        self.notificador: Notificador = notificador

    
    def registrar_prestamo(self,id_estudiante,id_dispositivo):
        estudiante:Estudiante =self.repositoorio_estudiante.obtener_estudiante_por_id(id_estudiante)
        dispositivo:Dispositivo = self.reprositorio_dispositivo.obtener_dispositivo_por_id(id_dispositivo)
        if estudiante is None or dispositivo is None:
            raise ValueError("No se encontró el estudiante o el dispositivo")
        
        if not dispositivo.es_disponible(): 
            raise ValueError("El dispositivo no está disponible para préstamo")
        
        cantidad_prestamos_activos = self.repositorio_prestamo.obtener_cantidad_prestamos_activos_por_estudiante(id_estudiante)  
        cantidad_deudas = self.reprositorio_multa.obtener_cantidad_multas_por_estudiante(id_estudiante)

        if cantidad_prestamos_activos >= 2 or cantidad_deudas > 0:
            raise ValueError("El estudiante no puede realizar más préstamos debido a restricciones")
        
        prestamo = Prestamo(self.proveedor_id.generar_id(), estudiante, dispositivo, self.proveedor_fecha.obtener_fecha_actual())
        dispositivo.cambiar_estado_en_uso()
        self.reprositorio_dispositivo.actualizar_dispositivo(dispositivo)
        self.repositorio_prestamo.guardar_prestamo(prestamo)
        self.notificador.enviar_mensaje("Prueba mensaje de caso de uso registrar prestamo cambiar este mensaje por uno mas elaborado con una funcion ")
 
