"""
Tests unitarios para el Requerimiento 2: Sistema de aprobación.
TC_07, TC_08, TC_09, TC_10
"""

import pytest
from src.student import Student
from src.exceptions import NoGradesError


class TestRequirement2ApprovalSystem:
    """Tests para determinación de aprobación/reprobación (nota >= 3.0)."""
    
    @pytest.fixture
    def student(self):
        """Crea un estudiante para cada test."""
        return Student("S002", "María García")
    
    # CASOS BORDE (Límite de aprobación)
    def test_tc_07_student_passes_with_exact_minimum_grade(self, student):
        """TC_07: Estudiante aprueba con nota = 3.0."""
        student.register_grade("Matemáticas", 3.0, 1)
        assert student.is_passing("Matemáticas", 1) is True
    
    def test_tc_08_student_fails_with_just_below_minimum_grade(self, student):
        """TC_08: Estudiante reprueba con nota = 2.99."""
        student.register_grade("Matemáticas", 2.99, 1)
        assert student.is_passing("Matemáticas", 1) is False
    
    # CASOS POSITIVOS
    def test_tc_09_student_passes_with_grade_above_minimum(self, student):
        """TC_09: Estudiante aprueba con nota > 3.0 (4.5)."""
        student.register_grade("Matemáticas", 4.5, 1)
        assert student.is_passing("Matemáticas", 1) is True
    
    # CASOS NEGATIVOS
    def test_tc_10_student_fails_with_grade_below_minimum(self, student):
        """TC_10: Estudiante reprueba con nota < 3.0 (1.5)."""
        student.register_grade("Física", 1.5, 1)
        assert student.is_passing("Física", 1) is False
    
    # CASOS ADICIONALES
    def test_passing_with_maximum_grade(self, student):
        """Estudiante aprueba con nota máxima (5.0)."""
        student.register_grade("Química", 5.0, 1)
        assert student.is_passing("Química", 1) is True
    
    def test_failing_with_minimum_grade(self, student):
        """Estudiante reprueba con nota mínima (0.0)."""
        student.register_grade("Inglés", 0.0, 1)
        assert student.is_passing("Inglés", 1) is False
    
    def test_is_passing_raises_error_for_non_registered_subject(self, student):
        """Lanza error si se intenta verificar aprobación de materia sin nota."""
        with pytest.raises(NoGradesError):
            student.is_passing("SinNota", 1)
