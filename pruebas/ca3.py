import sqlite3
from aplicacion.casos_uso.registrarDevolucion import RegistrarDevolucion

from dominio.estudiante import Estudiante
from dominio.portatil import Portatil
from dominio.camara import Camara
from dominio.kit_robot import KitRobot
from dominio.excepciones import LimiteDePrestamosExcedido
from dominio.estado_dispositivo import EstadoDispositivo
from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite
from infraestructura.repositorio_dispositivos_sqlite import RepositorioDispositivosSQLite
from infraestructura.repositorio_prestamo_sqlite import RepositorioPrestamoSQLite
from infraestructura.repositorio_multa_sqlite import RepositorioMultaSQLite
from infraestructura.proveedor_fecha_fija import ProveedorFechaFija
from infraestructura.proveedor_id_uuid import ProveedorIdUUID
from infraestructura.notificador_simulado import NotificadorSimulado

from datetime import date
from dominio.prestamo import Prestamo

def ejecutar():
    conexion = sqlite3.connect(":memory:")
    conexion.row_factory = sqlite3.Row

    repo_estudiantes = RepositorioEstudiantesSQLite(conexion)
    repo_dispositivos = RepositorioDispositivosSQLite(conexion)
    repo_prestamos = RepositorioPrestamoSQLite(conexion, repo_estudiantes, repo_dispositivos)
    repo_multas = RepositorioMultaSQLite(conexion)

    ana = Estudiante(id="1", codigo="1001", nombre="Ana")
    repo_estudiantes.agregar_estudiante(ana)


    camara2 = Camara(id="C2", codigo="CAMARA-02", estado=EstadoDispositivo.EN_USO)
    repo_dispositivos.guardar_dispositivo(camara2)



    proveedor_fecha = ProveedorFechaFija()
    proveedor_id = ProveedorIdUUID()
    notificador = NotificadorSimulado()
    proveedor_fecha_devolucion = ProveedorFechaFija(date(2026, 10, 6))

    caso_devolucion = RegistrarDevolucion(
        notificador=notificador,
        proveedor_id=proveedor_id,
        repositorioPrestamo=repo_prestamos,
        repositorio_estudiantes=repo_estudiantes,
        repositorio_dispositivos=repo_dispositivos,
        proveedor_fecha=proveedor_fecha_devolucion,
        proveedor_multa=repo_multas,
    )

    prestamo_1 = Prestamo(
        id="PRES-ANA-2",
        estudiante=ana,
        dispositivo=camara2,
        fecha_prestamo=date(2026, 10, 1),
    )
    repo_prestamos.guardar_prestamo(prestamo_1)

    print("--- CA3: devolución tardía de CAMARA-02 ---")
    try:
       caso_devolucion.registrar_devolucion(id_estudiante="1", id_dispositivo="C2")
       print("✅ CA3 exitoso: la devolución se procesó.")
    except Exception as e:
       print(f"❌ CA3 falló: {e}")


if __name__ == "__main__":
    ejecutar()