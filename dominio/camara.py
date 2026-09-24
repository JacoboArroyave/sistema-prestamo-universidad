from dispositivo import Dispositivo

class Camara(Dispositivo):
    
    @property
    def tarifa_diaria(self):
        return 8000
    
    @property
    def maximo_dias(self):
        return 2