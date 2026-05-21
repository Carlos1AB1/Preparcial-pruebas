"""
Módulo de gestión de notas académicas.

Responsabilidades:
- Validación de notas (rango, tipo de dato)
- Registro de notas por materia y semestre
- Prevención de duplicados
- Cálculo de promedios
- Evaluación de aprobación/reprobación
"""

from src.exceptions import InvalidGradeError, DuplicateGradeError, NoGradesError

PASSING_GRADE = 3.0
MIN_GRADE = 0.0
MAX_GRADE = 5.0


class GradeManager:
    """
    Gestor central de notas académicas.
    
    Encapsula toda la lógica de validación, almacenamiento y cálculo
    de notas para un estudiante individual.
    """
    
    def __init__(self):
        """Inicializa el gestor de notas."""
        self.grades = {}  # {(materia, semestre): nota}
    
    def _validate_grade_type(self, grade: float) -> None:
        """Valida que el tipo de dato sea numérico."""
        if not isinstance(grade, (int, float)):
            raise TypeError(f"La nota debe ser numérica, recibido: {type(grade).__name__}")
    
    def _validate_grade_range(self, grade: float) -> None:
        """Valida que la nota esté en el rango [0.0, 5.0]."""
        if grade < MIN_GRADE or grade > MAX_GRADE:
            raise InvalidGradeError(
                f"La nota {grade} está fuera del rango válido [{MIN_GRADE}, {MAX_GRADE}]"
            )
    
    def _validate_no_duplicate(self, subject: str, semester: int) -> None:
        """Valida que no exista una nota previa para esa materia/semestre."""
        key = (subject, semester)
        if key in self.grades:
            raise DuplicateGradeError(
                f"Ya existe una nota registrada para {subject} en semestre {semester}"
            )
    
    def register_grade(self, subject: str, grade: float, semester: int) -> bool:
        """
        Registra una nota para una materia en un semestre específico.
        
        Args:
            subject: Nombre de la materia
            grade: Nota entre 0.0 y 5.0
            semester: Número de semestre
            
        Returns:
            True si la nota se registró correctamente
            
        Raises:
            InvalidGradeError: Si la nota está fuera del rango [0.0, 5.0]
            DuplicateGradeError: Si ya existe nota para esa materia en ese semestre
            TypeError: Si grade no es numérico
        """
        self._validate_grade_type(grade)
        self._validate_grade_range(grade)
        self._validate_no_duplicate(subject, semester)
        
        key = (subject, semester)
        self.grades[key] = grade
        return True
    
    def get_grade(self, subject: str, semester: int) -> float:
        """Obtiene la nota de una materia en un semestre."""
        key = (subject, semester)
        return self.grades.get(key)
    
    def is_passing(self, subject: str, semester: int) -> bool:
        """
        Determina si el estudiante aprobó una materia.
        
        Se considera aprobada una materia con nota >= 3.0.
        
        Args:
            subject: Nombre de la materia
            semester: Número de semestre
            
        Returns:
            True si la nota es >= 3.0, False en caso contrario
            
        Raises:
            NoGradesError: Si no hay nota registrada para esa materia
        """
        grade = self.get_grade(subject, semester)
        if grade is None:
            raise NoGradesError(f"No hay nota registrada para {subject}")
        return grade >= PASSING_GRADE
    
    def calculate_average(self) -> float:
        """
        Calcula el promedio de todas las notas registradas.
        
        Returns:
            Promedio de todas las notas
            
        Raises:
            NoGradesError: Si no hay notas registradas
        """
        if not self.grades:
            raise NoGradesError("No hay notas registradas para calcular promedio")
        
        total = sum(self.grades.values())
        count = len(self.grades)
        return total / count
    
    def get_all_grades(self) -> dict:
        """Retorna todas las notas registradas."""
        return self.grades.copy()
