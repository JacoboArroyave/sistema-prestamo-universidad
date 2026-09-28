from datetime import date

from aplicacion.puertos.proveedor_fecha import ProveedorFecha


class ProveedorFechaFija(ProveedorFecha):
    def __init__(self, fecha_fija: date = date(2026, 10, 5)) -> None:
        self._fecha_fija = fecha_fija

    def obtener_fecha_actual(self) -> date:
        return self._fecha_fija
