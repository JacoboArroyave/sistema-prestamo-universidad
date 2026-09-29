
import sqlite3
from datetime import date

from aplicacion.casos_uso.registrarDevolucion import RegistrarDevolucion
from aplicacion.casos_uso.registrarPrestamo import RegistrarPrestamo
from dominio.camara import Camara
from dominio.estado_dispositivo import EstadoDispositivo
from dominio.estudiante import Estudiante
from dominio.prestamo import Prestamo
from infraestructura.notificador_simulado import NotificadorSimulado
from infraestructura.proveedor_fecha_fija import ProveedorFechaFija
from infraestructura.proveedor_id_uuid import ProveedorIdUUID
from infraestructura.repositorio_dispositivos_sqlite import (
    RepositorioDispositivosSQLite,
)
from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite
from infraestructura.repositorio_multa_sqlite import RepositorioMultaSQLite
from infraestructura.repositorio_prestamo_sqlite import RepositorioPrestamoSQLite


def ejecutar():
    # conexion = sqlite3.connect("sistema.db")
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
    proveedor_fecha_devolucion = ProveedorFechaFija(date(2026, 10, 2))

    caso_devolucion = RegistrarDevolucion(
        notificador=notificador,
        proveedor_id=proveedor_id,
        repositorioPrestamo=repo_prestamos,
        repositorio_estudiantes=repo_estudiantes,
        repositorio_dispositivos=repo_dispositivos,
        proveedor_fecha=proveedor_fecha_devolucion,
        proveedor_multa=repo_multas,
    ) 
    caso_prestamo = RegistrarPrestamo(
    
        notificador=notificador,
        proveedor_fecha=proveedor_fecha,
        proveedor_id=proveedor_id,
        repositorio_prestamo=repo_prestamos,
        repositorio_dispositivo=repo_dispositivos,
        repositorio_multa=repo_multas,
        repositorio_estudiante=repo_estudiantes,
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
        caso_devolucion.registrar_devolucion(id_estudiante="1", id_dispositivo="C2",estado_dispositivo=EstadoDispositivo.EN_MANTENIMIENTO)
        caso_prestamo.registrar_prestamo(id_estudiante="1", id_dispositivo="C2")
        print("❌ CA5 falló: ")

    except Exception as e:
        print(f"✅ CA5 exitoso: no se permitió registrar un préstamo de un dispositivo en mantenimiento: {e}")


if __name__ == "__main__":
    ejecutar()
