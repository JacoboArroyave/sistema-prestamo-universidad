import sqlite3
from dominio.camara import Camara
from dominio.dispositivo import Dispositivo
from dominio.estado_dispositivo import EstadoDispositivo
from dominio.kit_robot import KitRobot
from dominio.portatil import Portatil


class DispositivoMapper:
    @staticmethod
    def a_entidad(fila: sqlite3.Row) -> Dispositivo:
        tipo = fila["tipo"]
        estado = EstadoDispositivo(fila["estado"])
        
        if tipo == "PORTATIL":
            return Portatil(id=fila["id"], codigo=fila["codigo"], estado=estado)
        elif tipo == "CAMARA":
            return Camara(id=fila["id"], codigo=fila["codigo"], estado=estado)
        elif tipo == "KIT_ROBOTICA":
            return KitRobot(id=fila["id"], codigo=fila["codigo"], estado=estado)
        else:
            raise ValueError(f"Tipo de dispositivo no soportado: {tipo}")

    @staticmethod
    def obtener_tipo_str(dispositivo: Dispositivo) -> str:
        return dispositivo.__class__.__name__.upper()
