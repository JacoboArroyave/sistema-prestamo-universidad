from aplicacion.puertos.notificador import Notificador


class NotificadorSimulado(Notificador):
    def enviar_mensaje(self, mensaje: str) -> None:
        print(f"[NOTIFICACIÓN]: {mensaje}")
