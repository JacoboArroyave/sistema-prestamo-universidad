import sqlite3
from aplicacion.casos_uso.registrarPrestamo import RegistrarPrestamo
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

    portatil1 = Portatil(id="P1", codigo="PORTATIL-01", estado=EstadoDispositivo.EN_USO)
    repo_dispositivos.guardar_dispositivo(portatil1)

    camara1 = Camara(id="C1", codigo="CAMARA-01", estado=EstadoDispositivo.EN_USO)
    repo_dispositivos.guardar_dispositivo(camara1)

    kit_robot1 = KitRobot(id="K1", codigo="KIT-ROBOT-01", estado=EstadoDispositivo.DISPONIBLE)
    repo_dispositivos.guardar_dispositivo(kit_robot1)

    proveedor_fecha = ProveedorFechaFija()
    proveedor_id = ProveedorIdUUID()
    notificador = NotificadorSimulado()

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
        id="PRES-ANA-1",
        estudiante=ana,
        dispositivo=portatil1,
        fecha_prestamo=date(2026, 10, 2),
    )
    repo_prestamos.guardar_prestamo(prestamo_1)

    prestamo_2 = Prestamo(
        id="PRES-ANA-2",
        estudiante=ana,
        dispositivo=camara1,
        fecha_prestamo=date(2026, 10, 3),
    )
    repo_prestamos.guardar_prestamo(prestamo_2)

    print("--- CA2: Ana (con 2 préstamos activos) pide un tercer equipo ---")
    try:
        caso_prestamo.registrar_prestamo(id_estudiante="1", id_dispositivo="K1")
        print("❌ CA2 falló: el préstamo se registró pero debía ser rechazado.")
    except LimiteDePrestamosExcedido as e:
        print(f"✅ CA2 exitoso (rechazado correctamente): {e}")

if __name__ == "__main__":
    ejecutar()