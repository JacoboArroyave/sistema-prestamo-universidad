from dispositivo import Dispositivo

class Portatil(Dispositivo):
    
    @property
    def tarifa_diaria(self):
        return 5000
    
    @property
    def maximo_dias(self):
        return 3