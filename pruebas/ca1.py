import sqlite3

from aplicacion.casos_uso.registrarPrestamo import RegistrarPrestamo
from dominio.estudiante import Estudiante
from dominio.portatil import Portatil
from dominio.estado_dispositivo import EstadoDispositivo
from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite
from infraestructura.repositorio_dispositivos_sqlite import RepositorioDispositivosSQLite
from infraestructura.repositorio_prestamo_sqlite import RepositorioPrestamoSQLite
from infraestructura.repositorio_multa_sqlite import RepositorioMultaSQLite
from infraestructura.proveedor_fecha_fija import ProveedorFechaFija
from infraestructura.proveedor_id_uuid import ProveedorIdUUID
from infraestructura.notificador_simulado import NotificadorSimulado

def ejecutar():
    conexion = sqlite3.connect(":memory:")
    conexion.row_factory = sqlite3.Row

    repo_estudiantes = RepositorioEstudiantesSQLite(conexion)
    repo_dispositivos = RepositorioDispositivosSQLite(conexion)
    repo_prestamos = RepositorioPrestamoSQLite(conexion, repo_estudiantes, repo_dispositivos)
    repo_multas = RepositorioMultaSQLite(conexion)

    ana = Estudiante(id="1", codigo="1001", nombre="Ana")
    repo_estudiantes.agregar_estudiante(ana)

    portatil1 = Portatil(id="P1", codigo="PORTATIL-01", estado=EstadoDispositivo.DISPONIBLE)
    repo_dispositivos.guardar_dispositivo(portatil1)

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

    print("--- CA1: Ana (sin préstamos previos) pide PORTATIL-01 ---")
    try:
        caso_prestamo.registrar_prestamo(id_estudiante="1", id_dispositivo="P1")
        print("✅ CA1 exitoso: el préstamo se registró y se notificó la fecha límite.")
    except Exception as e:
        print(f"❌ CA1 falló: {e}")

if __name__ == "__main__":
    ejecutar()