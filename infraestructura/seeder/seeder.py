from datetime import date

from dominio.camara import Camara
from dominio.estado_dispositivo import EstadoDispositivo
from dominio.estado_multa import EstadoMulta
from dominio.estado_prestamo import EstadoPrestamo
from dominio.estudiante import Estudiante
from dominio.kit_robot import KitRobot
from dominio.multa import Multa
from dominio.portatil import Portatil
from dominio.prestamo import Prestamo
from infraestructura.repositorio_dispositivos_sqlite import (
    RepositorioDispositivosSQLite,
)
from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite
from infraestructura.repositorio_multa_sqlite import RepositorioMultaSQLite
from infraestructura.repositorio_prestamo_sqlite import RepositorioPrestamoSQLite


class Seeder:
    def __init__(
        self,
        repo_estudiantes: RepositorioEstudiantesSQLite,
        repo_dispositivos: RepositorioDispositivosSQLite,
        repo_prestamos: RepositorioPrestamoSQLite,
        repo_multas: RepositorioMultaSQLite,
    ) -> None:
        self.repo_estudiantes = repo_estudiantes
        self.repo_dispositivos = repo_dispositivos
        self.repo_prestamos = repo_prestamos
        self.repo_multas = repo_multas

    def poblar_datos_iniciales(self) -> None:
        # 1. Crear Estudiantes
        ana = Estudiante(id="1", codigo="1001", nombre="Ana")
        luis = Estudiante(id="2", codigo="1002", nombre="Luis")
        carlos = Estudiante(id="3", codigo="1003", nombre="Carlos")

        self.repo_estudiantes.agregar_estudiante(ana)
        self.repo_estudiantes.agregar_estudiante(luis)
        self.repo_estudiantes.agregar_estudiante(carlos)

        # 2. Crear Dispositivos
        portatil1 = Portatil(id="P1", codigo="PORTATIL-01", estado=EstadoDispositivo.DISPONIBLE)
        portatil2 = Portatil(id="P2", codigo="PORTATIL-02", estado=EstadoDispositivo.EN_USO)
        portatil3 = Portatil(id="P3", codigo="PORTATIL-03", estado=EstadoDispositivo.EN_USO)
        
        camara1 = Camara(id="C1", codigo="CAMARA-01", estado=EstadoDispositivo.DISPONIBLE)
        camara2 = Camara(id="C2", codigo="CAMARA-02", estado=EstadoDispositivo.EN_USO)
        
        kit1 = KitRobot(id="K1", codigo="KIT-01", estado=EstadoDispositivo.DISPONIBLE)

        self.repo_dispositivos.guardar_dispositivo([portatil1, portatil2, portatil3, camara1, camara2, kit1])

        # 3. Crear Préstamos Activos para Ana (R1: Máximo 2 activos)
        prestamo_ana_1 = Prestamo(
            id="PRES-ANA-1",
            estudiante=ana,
            dispositivo=portatil2,
            fecha_prestamo=date(2026, 10, 2)
        )
        prestamo_ana_2 = Prestamo(
            id="PRES-ANA-2",
            estudiante=ana,
            dispositivo=portatil3,
            fecha_prestamo=date(2026, 10, 3)
        )

        # 4. Crear Préstamo vencido para Devolución (CA3: prestada el 2026-10-01)
        prestamo_camara = Prestamo(
            id="PRES-CAMARA-2",
            estudiante=carlos,
            dispositivo=camara2,
            fecha_prestamo=date(2026, 10, 1)
        )

        self.repo_prestamos.guardar_prestamo(prestamo_ana_1)
        self.repo_prestamos.guardar_prestamo(prestamo_ana_2)
        self.repo_prestamos.guardar_prestamo(prestamo_camara)

        # 5. Crear Préstamo histórico y Multa pendiente para Luis (CA4)
        prestamo_luis = Prestamo(
            id="PRES-LUIS-1",
            estudiante=luis,
            dispositivo=camara1,
            fecha_prestamo=date(2026, 9, 20),
            fecha_devolucion=date(2026, 9, 28)
        )
        prestamo_luis.estado = EstadoPrestamo.FINALIZADO
        self.repo_prestamos.guardar_prestamo(prestamo_luis)

        multa_luis = Multa(id="MULTA-LUIS-1", prestamo=prestamo_luis, valor=16000)
        self.repo_multas.guardar_multa(multa_luis)
