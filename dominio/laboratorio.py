from dispositivo import Dispositivo


class Laboratorio:

    def __init__(self, dispositivos: list[Dispositivo]):
        self.dispositivos = dispositivos

    def buscar_dispositivo(self, id):
        for dispositivo in self.dispositivos:
            if dispositivo.id == id:
                return dispositivo

        return None

    def calcularMulta(self, id, dias_retraso):
        dispositivo = self.buscar_dispositivo(id)

        if dispositivo is None:
            return 0

        if dias_retraso <= 0:
            return 0

        return dispositivo.tarifa_diaria * dias_retraso

    def validarFechaDevolucion(self, id, dias_prestamo):
        dispositivo = self.buscar_dispositivo(id)

        if dispositivo is None:
            return False

        return dias_prestamo <= dispositivo.maximo_dias