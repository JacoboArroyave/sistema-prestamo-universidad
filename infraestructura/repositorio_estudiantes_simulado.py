from typing import override

from aplicacion.puertos.repositorio_estudiantes import RepositorioEstudiantes
from dominio.estudiante import Estudiante


class RepositorioEstudiantesSimulado(RepositorioEstudiantes):
    def __init__(self):
        self.estudiantes:list[Estudiante] = []
    @override
    def obtener_estudiantes(self)->list[Estudiante]:
        # # for estudiante in self.estudiantes: 
        # #     print(estudiante.__str__())
        return self.estudiantes
    @override
    def agregar_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    @override
    def obtener_estudiante_por_id(self,estudiante_id)->Estudiante | None :
        for estudiante in self.estudiantes:
            if estudiante.id == estudiante_id:
                return estudiante
        return None 
