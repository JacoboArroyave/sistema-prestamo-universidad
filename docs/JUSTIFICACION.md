# 1. Justificacion imports:

## 1.1. Dominio:
    class Prestamo:
        from datetime import date, timedelta
        from dominio.dispositivo import Dispositivo
        from dominio.estado_dispositivo import EstadoDispositivo
        from dominio.estado_prestamo import EstadoPrestamo
        from dominio.estudiante import Estudiante

La clase prestamo obtenida de la relacion de estudiante (n) --- (n) dispositivo, solo importa clases de la misma capa de dominio para relacionar la logica de los pretsamos asociados a los estudiantes y dispositivos, por tanto sera una de las clases de dominio importadas en la siguiente capa.

## 1.2. Aplicacion
    class RegistrarDevolucion:
        from aplicacion.puertos.notificador import Notificador
        from aplicacion.puertos.proveedor_fecha import ProveedorFecha
        from aplicacion.puertos.proveedor_id import ProveedorId
        from aplicacion.puertos.repositorio_dispositivos import RepositorioDispositivos
        from aplicacion.puertos.repositorio_estudiantes import RepositorioEstudiantes
        from aplicacion.puertos.repositorio_multa import RepositorioMulta
        from aplicacion.puertos.repositorio_prestamo import RepositorioPrestamo
        from dominio.estado_dispositivo import EstadoDispositivo
        from dominio.multa import Multa
        from dominio.prestamo import Prestamo

Para el caso de uso de RegistrarDevolucion se importan solo clases de puertos (abstracciones), y las clases de dominio que contienen las clases de entidad en este caso, Multa y Prestamo, aplicando la logica de negocio del caso.

## 1.3. Infraestructura:
    
    class RepositorioPrestamoSQLite(RepositorioPrestamo):
        import sqlite3
        from aplicacion.puertos.repositorio_prestamo import RepositorioPrestamo
        from dominio.prestamo import Prestamo
        from infraestructura.mappers.prestamo_mapper import PrestamoMapper
        from infraestructura.repositorio_dispositivos_sqlite import RepositorioDispositivosSQLite
        from infraestructura.repositorio_estudiantes_sqlite import RepositorioEstudiantesSQLite

Para este caso se implementa la interfaz abstracta RepositorioPrestamo que pertenece a la capa de aplicacion, con sql lite por lo que ya se implementan librerias especificas como sqlite3.

# 2. Tabla criterios:


| Principio                           | Archivo                                      | Decisión Concreta                                                                                                                                                                                                                         | Dónde se Aplica               |
| ----------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **DIP** | `aplicacion/casos_uso/registrar_prestamo.py` | En este caso de uso no acoplamos a clases concretas de infraestructura. En cambio usamos contratos abstractos.                        | `RegistrarPrestamo`           |
| **SRP**     | `aplicacion/casos_uso/registrar_prestamo.py` | La clase solo orquesta el flujo de negocio del préstamo (validar condiciones, actualizar estados y notificar). Delega la generación de ID, la obtención de la fecha y el envío del mensaje a servicios dedicados.                         | `RegistrarPrestamo`           |
| **OCP**           | `dominio/dispositivo.py`                     |La clase abstracta Dispositivo permite extender el sistema agregando nuevas categorías extendiendo de ella, sin necesidad de modificar el código existente. | `Dispositivo` y sus subclases |
| **LSP**     | `aplicacion/puertos/repositorio_prestamo.py` | Cualquier implementación de los repositorios (en este contexto `SQLite` o `Memoria`) se puede pasar al constructor de `RegistrarPrestamo` de forma transparente sin alterar el comportamiento esperado. | `RepositorioPrestamo`         |
| **ISP** | `aplicacion/puertos/proveedor_fecha.py`      | Se definen contratos pequeños y específicos (`ProveedorFecha`, `ProveedorId`, `Notificador`) con solo los métodos necesarios, en lugar de una interfaz monolítica de utilidades.                                                          | `aplicacion/puertos/`         |

# 3. Uso IA.

El uso de la IA se enfoco en la resolucion de dudas teoricas acerca de los principios a utilizar junto con errores sintacticos que se presentaron en la implementacion del proyecto, "Declaramos que el diseño, el código y los diagramas son de nuestra autoría y que no usamos IA generativa para producirlos"

Jacobo Arroyave 

Daniel Cardona

Camilo Niño