import uuid

from aplicacion.puertos.proveedor_id import ProveedorId


class ProveedorIdUUID(ProveedorId):
    def generar_id(self) -> str:
        return str(uuid.uuid4())
