"""
Excepciones personalizadas para el sistema de registro de notas.
"""


class InvalidGradeError(ValueError):
    """Se lanza cuando se intenta registrar una nota fuera del rango [0.0, 5.0]."""
    pass


class DuplicateGradeError(ValueError):
    """Se lanza cuando se intenta registrar dos notas para la misma materia en el mismo semestre."""
    pass


class NoGradesError(ValueError):
    """Se lanza cuando se intenta calcular promedio sin notas registradas."""
    pass
