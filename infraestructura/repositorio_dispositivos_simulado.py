from typing import override

from aplicacion.puertos.repositorio_dispositivos import RepositorioDispositivos
from dominio.dispositivo import Dispositivo


class RepositorioDispositivosSimulado(RepositorioDispositivos):
    def __init__(self):
        self.dispositivos:list[Dispositivo] = []

    @override
    def obtener_dispositivos(self) -> list[Dispositivo]:
        return self.dispositivos
    
    @override
    def guardar_dispositivo(self, dispositivo: Dispositivo) -> None:
        self.dispositivos.append(dispositivo)
    
    @override
    def eliminar_dispositivo(self, dispositivo_id) -> None:
        self.dispositivos = [dispositivo for dispositivo in self.dispositivos if dispositivo.id != dispositivo_id]
    
    @override
    def obtener_dispositivo_por_id(self, dispositivo_id) -> Dispositivo | None:
        for dispositivo in self.dispositivos:
            if dispositivo.id == dispositivo_id:
                return dispositivo
        return None

    @override
    def actualizar_dispositivo(self, dispositivo: Dispositivo) -> None:
        for i, d in enumerate(self.dispositivos):
            if d.id == dispositivo.id:
                self.dispositivos[i] = dispositivo
                return


