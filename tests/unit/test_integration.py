"""
Tests de integración para el sistema completo.
Verifica que los requerimientos funcionen juntos correctamente.
"""

import pytest
from src.student import Student
from src.exceptions import DuplicateGradeError, NoGradesError


class TestSystemIntegration:
    """Tests de integración del sistema completo."""
    
    def test_complete_student_workflow(self):
        """
        Test de integración completa: un estudiante registra notas,
        verifica aprobación, calcula promedio y evita duplicados.
        """
        # Crear estudiante
        student = Student("S001", "Juan Pérez")
        
        # R1: Registrar varias notas válidas
        assert student.register_grade("Matemáticas", 4.5, 1) is True
        assert student.register_grade("Física", 3.0, 1) is True
        assert student.register_grade("Química", 2.8, 1) is True
        
        # R2: Verificar aprobación
        assert student.is_passing("Matemáticas", 1) is True
        assert student.is_passing("Física", 1) is True
        assert student.is_passing("Química", 1) is False
        
        # R3: Calcular promedio
        average = student.calculate_average()
        assert abs(average - 3.433333) < 0.01
        
        # R4: Intentar registrar duplicado
        with pytest.raises(DuplicateGradeError):
            student.register_grade("Matemáticas", 4.0, 1)
        
        # R4: Permitir misma materia en diferente semestre
        assert student.register_grade("Matemáticas", 3.5, 2) is True
        
        # Verificar que se tienen las notas correctas
        all_grades = student.get_all_grades()
        assert len(all_grades) == 4
    
    def test_multiple_students_isolation(self):
        """Verifica que estudiantes diferentes mantengan sus propias notas."""
        student1 = Student("S001", "Ana")
        student2 = Student("S002", "Carlos")
        
        student1.register_grade("Matemáticas", 5.0, 1)
        student2.register_grade("Matemáticas", 1.0, 1)
        
        assert student1.is_passing("Matemáticas", 1) is True
        assert student2.is_passing("Matemáticas", 1) is False
        
        assert student1.calculate_average() == 5.0
        assert student2.calculate_average() == 1.0
    
    def test_semester_isolation(self):
        """Verifica que semestres diferentes no interfieren entre sí."""
        student = Student("S001", "Maria")
        
        # Semestre 1
        student.register_grade("Historia", 2.5, 1)
        assert student.is_passing("Historia", 1) is False
        
        # Semestre 2 - misma materia, nueva nota
        student.register_grade("Historia", 4.0, 2)
        assert student.is_passing("Historia", 2) is True
        
        # Promedio de ambos semestres
        average = student.calculate_average()
        assert abs(average - 3.25) < 0.01
    
    def test_edge_case_boundary_values(self):
        """Test de casos límite en integración."""
        student = Student("S001", "Test")
        
        # Registrar valores en los límites
        student.register_grade("Math", 0.0, 1)  # Mínimo
        student.register_grade("Physics", 5.0, 1)  # Máximo
        student.register_grade("Chemistry", 3.0, 1)  # Punto de corte
        
        # Math: 0.0 < 3.0 (reprueba)
        assert student.is_passing("Math", 1) is False
        # Physics: 5.0 >= 3.0 (aprueba)
        assert student.is_passing("Physics", 1) is True
        # Chemistry: 3.0 >= 3.0 (aprueba)
        assert student.is_passing("Chemistry", 1) is True
        
        # Promedio exacto: (0.0 + 5.0 + 3.0) / 3 = 2.666...
        average = student.calculate_average()
        assert abs(average - 2.6667) < 0.01
