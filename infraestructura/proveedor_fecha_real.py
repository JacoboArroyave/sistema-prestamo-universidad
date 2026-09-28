from datetime import date

from aplicacion.puertos.proveedor_fecha import ProveedorFecha


class ProveedorFechaReal(ProveedorFecha):
    def obtener_fecha_actual(self) -> date:
        return date.today()  # noqa: DTZ011
