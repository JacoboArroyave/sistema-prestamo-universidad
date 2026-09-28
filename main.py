import sqlite3
# CASOS DE USO
from aplicacion.casos_uso.registrarDevolucion import RegistrarDevolucion
from aplicacion.casos_uso.registrarPrestamo import RegistrarPrestamo

# CONCRETOS INFRAESTRUCTURA SQL
from infraestructura.notificador_simulado import NotificadorSimulado
from infraestructura.proveedor_fecha_fija import ProveedorFechaFija
from infraestructura.proveedor_id_uuid import ProveedorIdUUID
from infraestructura.repositorio_dispositivos_sqlite import (
    RepositorioDispositivosSQLite,
)
from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite
from infraestructura.repositorio_multa_sqlite import RepositorioMultaSQLite
from infraestructura.repositorio_prestamo_sqlite import RepositorioPrestamoSQLite

# SEEDER 
from infraestructura.seeder.seeder import Seeder

# Crear conexión SQLite
conexion = sqlite3.connect("sistema.db")
conexion.row_factory = sqlite3.Row  # Necesario para acceder a campos por nombre

# Instanciar repositorios
repo_estudiantes = RepositorioEstudiantesSQLite(conexion)
repo_dispositivos = RepositorioDispositivosSQLite(conexion)
repo_prestamos = RepositorioPrestamoSQLite(conexion, repo_estudiantes, repo_dispositivos)
repo_multas = RepositorioMultaSQLite(conexion)
proveedor_id =ProveedorIdUUID()
proveedor_fecha_fija=ProveedorFechaFija()
notificador = NotificadorSimulado()

# --- Instanciación de Casos de Uso ---

caso_prestamo = RegistrarPrestamo(
    notificador=notificador,
    proveedor_fecha=proveedor_fecha_fija,
    proveedor_id=proveedor_id,
    repositorio_prestamo=repo_prestamos,
    repositorio_dispositivo=repo_dispositivos,
    repositorio_multa=repo_multas,
    repositorio_estudiante=repo_estudiantes,
)

# 2. Caso de Uso: Registrar Devolución
caso_devolucion = RegistrarDevolucion(
    notificador=notificador,
    proveedor_id=proveedor_id,
    repositorioPrestamo=repo_prestamos,
    repositorio_estudiantes=repo_estudiantes,
    repositorio_dispositivos=repo_dispositivos,
    proveedor_fecha=proveedor_fecha_fija,
    proveedor_multa=repo_multas,
)
# Ejecutar el seeder de prueba
seeder = Seeder(repo_estudiantes, repo_dispositivos, repo_prestamos, repo_multas)
seeder.poblar_datos_iniciales()

# print("¡Base de datos inicializada y poblada correctamente para los Casos de Aceptación!")

# --- Prueba de Caso de Aceptación (CA4): Intento de préstamo a estudiante con multa ---
print("\n--- Probando Préstamo para Luis (ID: '2') ---")

try:
    # Intentamos prestarle un dispositivo disponible (ej: PORTATIL-01 con ID 'P1')
    caso_prestamo.registrar_prestamo(
        id_estudiante="2",     # Luis
        id_dispositivo="P1"    # PORTATIL-01
    )
    print("❌ ERROR: El préstamo se registró pero debió ser rechazado por multa.")
except ValueError as e:
    print(f" CA4 Exitoso (Rechazado correctamente): {e}")

# --- Prueba de Caso de Aceptación (CA1): Préstamo Exitoso para Carlos ---
print("\n--- Probando Préstamo Exitoso para Carlos (ID: '3') ---")

try:
    caso_prestamo.registrar_prestamo(
        id_estudiante="3",     # Carlos (sin multas ni préstamos previos)
        id_dispositivo="P1"    # PORTATIL-01 (DISPONIBLE)
    )
    print(" CA1 Exitoso: El préstamo se registró correctamente y se notificó la fecha límite.")
except ValueError as e:
    print(f"❌ Error insospechado: {e}")


repo_prestamos.obtener_todos() # por ahora no hay nada.