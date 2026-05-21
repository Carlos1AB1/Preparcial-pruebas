"""
Tests unitarios para el Requerimiento 4: Prevención de duplicados.
TC_14, TC_15, TC_16
"""

import pytest
from src.student import Student
from src.exceptions import DuplicateGradeError


class TestRequirement4DuplicatePrevention:
    """Tests para prevención de notas duplicadas en misma materia/semestre."""
    
    @pytest.fixture
    def student(self):
        """Crea un estudiante para cada test."""
        return Student("S004", "Ana Martínez")
    
    # CASOS NEGATIVOS (Detectan duplicados)
    def test_tc_14_reject_duplicate_same_subject_same_semester(self, student):
        """TC_14: Rechazar duplicado - misma materia, mismo semestre."""
        # Primera nota registrada correctamente
        student.register_grade("Matemáticas", 3.0, 1)
        
        # Intento de registrar segunda nota para la misma materia en mismo semestre
        with pytest.raises(DuplicateGradeError) as exc_info:
            student.register_grade("Matemáticas", 2.5, 1)
        
        assert "ya existe" in str(exc_info.value).lower()
        # Verificar que la nota original se mantiene
        assert student.get_grade("Matemáticas", 1) == 3.0
    
    # CASOS POSITIVOS (Permiten registros en diferente contexto)
    def test_tc_15_allow_same_subject_different_semester(self, student):
        """TC_15: Permitir nota en misma materia, diferente semestre."""
        # Registrar nota en semestre 1
        student.register_grade("Matemáticas", 3.0, 1)
        
        # Registrar nota en semestre 2 (debe permitirse)
        result = student.register_grade("Matemáticas", 3.5, 2)
        assert result is True
        
        # Verificar que ambas notas se registraron
        assert student.get_grade("Matemáticas", 1) == 3.0
        assert student.get_grade("Matemáticas", 2) == 3.5
    
    def test_tc_16_allow_different_subject_same_semester(self, student):
        """TC_16: Permitir nota en materia diferente, mismo semestre."""
        # Registrar nota de Matemáticas en semestre 1
        student.register_grade("Matemáticas", 4.0, 1)
        
        # Registrar nota de Física en semestre 1 (debe permitirse)
        result = student.register_grade("Física", 3.5, 1)
        assert result is True
        
        # Verificar que ambas notas se registraron
        assert student.get_grade("Matemáticas", 1) == 4.0
        assert student.get_grade("Física", 1) == 3.5
    
    # CASOS ADICIONALES
    def test_allow_multiple_subjects_multiple_semesters(self, student):
        """Permitir múltiples materias en múltiples semestres."""
        # Semestre 1
        student.register_grade("Matemáticas", 3.0, 1)
        student.register_grade("Física", 4.0, 1)
        
        # Semestre 2
        student.register_grade("Matemáticas", 3.5, 2)
        student.register_grade("Química", 4.5, 2)
        
        all_grades = student.get_all_grades()
        assert len(all_grades) == 4
    
    def test_duplicate_error_preserves_original_grade(self, student):
        """Verificar que error de duplicado preserva la nota original."""
        original_grade = 3.8
        student.register_grade("Historia", original_grade, 1)
        
        try:
            student.register_grade("Historia", 2.0, 1)
        except DuplicateGradeError:
            pass
        
        # La nota original debe permanecer
        assert student.get_grade("Historia", 1) == original_grade
