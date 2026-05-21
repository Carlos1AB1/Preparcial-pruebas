"""
Módulo de estudiante con gestión de notas académicas.
"""

from src.grade_manager import GradeManager


class Student:
    """Representa un estudiante con su gestión de notas."""
    
    def __init__(self, student_id: str, name: str):
        """
        Inicializa un estudiante.
        
        Args:
            student_id: ID único del estudiante
            name: Nombre del estudiante
        """
        self.student_id = student_id
        self.name = name
        self.grade_manager = GradeManager()
    
    def register_grade(self, subject: str, grade: float, semester: int) -> bool:
        """
        Registra una nota para una materia.
        
        Args:
            subject: Nombre de la materia
            grade: Nota entre 0.0 y 5.0
            semester: Número de semestre
            
        Returns:
            True si se registró correctamente
        """
        return self.grade_manager.register_grade(subject, grade, semester)
    
    def is_passing(self, subject: str, semester: int) -> bool:
        """
        Verifica si el estudiante aprobó una materia.
        
        Args:
            subject: Nombre de la materia
            semester: Número de semestre
            
        Returns:
            True si aprobó (nota >= 3.0), False en caso contrario
        """
        return self.grade_manager.is_passing(subject, semester)
    
    def calculate_average(self) -> float:
        """
        Calcula el promedio de todas las notas del estudiante.
        
        Returns:
            Promedio de todas las notas
        """
        return self.grade_manager.calculate_average()
    
    def get_grade(self, subject: str, semester: int) -> float:
        """Obtiene la nota de una materia en un semestre."""
        return self.grade_manager.get_grade(subject, semester)
    
    def get_all_grades(self) -> dict:
        """Retorna todas las notas registradas del estudiante."""
        return self.grade_manager.get_all_grades()
