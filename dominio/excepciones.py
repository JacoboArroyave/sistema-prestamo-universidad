#Excepción lanzada cuando se excede el límite de préstamos permitidos
class LimiteDePrestamosExcedido(Exception):
    pass

#Excepción lanzada cuando el estudiante tiene una multa pendiente y no puede realizar un nuevo préstamo
class MultaPendiente(Exception):
    pass