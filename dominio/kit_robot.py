from dispositivo import Dispositivo

class KitRobot(Dispositivo):
    
    @property
    def tarifa_diaria(self):
        return 12000
    
    @property
    def maximo_dias(self):
        return 1