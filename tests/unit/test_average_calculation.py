"""
Tests unitarios para el Requerimiento 3: Cálculo de promedio.
TC_11, TC_12, TC_13
"""

import pytest
from src.student import Student
from src.exceptions import NoGradesError


class TestRequirement3AverageCalculation:
    """Tests para cálculo del promedio de notas."""
    
    @pytest.fixture
    def student(self):
        """Crea un estudiante para cada test."""
        return Student("S003", "Carlos López")
    
    # CASOS POSITIVOS
    def test_tc_11_calculate_average_of_multiple_grades(self, student):
        """TC_11: Calcular promedio de múltiples notas [3.0, 4.0, 5.0]."""
        student.register_grade("Matemáticas", 3.0, 1)
        student.register_grade("Física", 4.0, 1)
        student.register_grade("Química", 5.0, 1)
        
        average = student.calculate_average()
        assert average == pytest.approx(4.0)
    
    def test_tc_13_calculate_average_with_single_grade(self, student):
        """TC_13: Calcular promedio con una sola nota (3.5)."""
        student.register_grade("Historia", 3.5, 1)
        average = student.calculate_average()
        assert average == 3.5
    
    # CASOS NEGATIVOS
    def test_tc_12_calculate_average_with_no_grades(self, student):
        """TC_12: Calcular promedio sin notas registradas."""
        with pytest.raises(NoGradesError) as exc_info:
            student.calculate_average()
        assert "no hay" in str(exc_info.value).lower()
    
    # CASOS ADICIONALES
    def test_calculate_average_with_two_grades(self, student):
        """Calcular promedio con dos notas."""
        student.register_grade("Inglés", 2.0, 1)
        student.register_grade("Programación", 4.0, 1)
        
        average = student.calculate_average()
        assert average == 3.0
    
    def test_calculate_average_with_decimal_values(self, student):
        """Calcular promedio con valores decimales."""
        student.register_grade("Arte", 2.5, 1)
        student.register_grade("Música", 3.5, 1)
        student.register_grade("Deporte", 4.0, 1)
        
        average = student.calculate_average()
        assert average == pytest.approx(3.333333, rel=1e-5)
    
    def test_calculate_average_with_zero_grades(self, student):
        """Calcular promedio incluyendo nota 0.0."""
        student.register_grade("Física", 0.0, 1)
        student.register_grade("Química", 5.0, 1)
        
        average = student.calculate_average()
        assert average == 2.5
