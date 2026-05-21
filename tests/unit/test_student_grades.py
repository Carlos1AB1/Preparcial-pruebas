"""
Tests unitarios para el Requerimiento 1: Registro de notas (validación de rango).
TC_01, TC_02, TC_03, TC_04, TC_05, TC_06
"""

import pytest
from src.student import Student
from src.exceptions import InvalidGradeError


class TestRequirement1GradeValidation:
    """Tests para validación de notas en rango [0.0, 5.0]."""
    
    @pytest.fixture
    def student(self):
        """Crea un estudiante para cada test."""
        return Student("S001", "Juan Pérez")
    
    # CASOS POSITIVOS (Particiones válidas)
    def test_tc_01_register_valid_mid_range_grade(self, student):
        """TC_01: Registrar nota válida en rango medio (3.5)."""
        result = student.register_grade("Matemáticas", 3.5, 1)
        assert result is True
        assert student.get_grade("Matemáticas", 1) == 3.5
    
    # CASOS BORDE (Valores límite)
    def test_tc_02_register_valid_lower_boundary_grade(self, student):
        """TC_02: Registrar nota en límite inferior válido (0.0)."""
        result = student.register_grade("Física", 0.0, 1)
        assert result is True
        assert student.get_grade("Física", 1) == 0.0
    
    def test_tc_03_register_valid_upper_boundary_grade(self, student):
        """TC_03: Registrar nota en límite superior válido (5.0)."""
        result = student.register_grade("Química", 5.0, 1)
        assert result is True
        assert student.get_grade("Química", 1) == 5.0
    
    # CASOS NEGATIVOS (Particiones inválidas)
    def test_tc_04_reject_negative_grade(self, student):
        """TC_04: Rechazar nota negativa (-0.5)."""
        with pytest.raises(InvalidGradeError) as exc_info:
            student.register_grade("Historia", -0.5, 1)
        assert "rango válido" in str(exc_info.value).lower()
    
    def test_tc_05_reject_grade_above_maximum(self, student):
        """TC_05: Rechazar nota mayor a 5.0 (5.1)."""
        with pytest.raises(InvalidGradeError) as exc_info:
            student.register_grade("Inglés", 5.1, 1)
        assert "rango válido" in str(exc_info.value).lower()
    
    def test_tc_06_reject_non_numeric_grade(self, student):
        """TC_06: Rechazar tipo de dato no válido ('abc')."""
        with pytest.raises(TypeError) as exc_info:
            student.register_grade("Programación", "abc", 1)
        assert "numérica" in str(exc_info.value).lower()
    
    # CASOS ADICIONALES DE BORDE
    def test_register_grade_just_below_lower_boundary(self, student):
        """Registrar nota justo antes del límite inferior (-0.1)."""
        with pytest.raises(InvalidGradeError):
            student.register_grade("Música", -0.1, 1)
    
    def test_register_grade_just_after_lower_boundary(self, student):
        """Registrar nota justo después del límite inferior (0.1)."""
        result = student.register_grade("Música", 0.1, 1)
        assert result is True
    
    def test_register_grade_just_below_upper_boundary(self, student):
        """Registrar nota justo antes del límite superior (4.9)."""
        result = student.register_grade("Dibujo", 4.9, 1)
        assert result is True
    
    def test_register_grade_just_after_upper_boundary(self, student):
        """Registrar nota justo después del límite superior (5.1)."""
        with pytest.raises(InvalidGradeError):
            student.register_grade("Dibujo", 5.1, 1)
