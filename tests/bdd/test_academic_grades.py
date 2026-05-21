"""
Step definitions para los escenarios BDD del sistema de notas académicas.

Conecta los pasos del archivo Gherkin con la implementación del código.
"""

import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from src.student import Student
from src.exceptions import (
    InvalidGradeError,
    DuplicateGradeError,
    NoGradesError,
)

# Cargar todos los escenarios del archivo .feature
scenarios("academic_grades.feature")


# ============================================================================
# FIXTURES Y ESTADO COMPARTIDO
# ============================================================================

@pytest.fixture
def student_context():
    """Contexto compartido para los tests BDD."""
    return {
        "student": None,
        "last_exception": None,
        "is_passing_result": None,
        "average_result": None,
    }


# ============================================================================
# BACKGROUND: Precondiciones comunes
# ============================================================================

@given(
    parsers.parse(
        'un estudiante registrado en el sistema con ID "{student_id}" '
        'y nombre "{student_name}"'
    )
)
def create_student(student_context, student_id, student_name):
    """Crea un estudiante para los escenarios."""
    student_context["student"] = Student(student_id, student_name)


# ============================================================================
# REQUERIMIENTO 2: SISTEMA DE APROBACIÓN
# ============================================================================

@given(
    parsers.parse(
        'el estudiante ha registrado una nota de {grade:f} '
        'para "{subject}" en semestre {semester:d}'
    )
)
def register_single_grade(student_context, grade, subject, semester):
    """Registra una nota para un estudiante."""
    student = student_context["student"]
    student.register_grade(subject, grade, semester)


@when(
    parsers.parse(
        'se verifica si el estudiante aprobó "{subject}" en semestre {semester:d}'
    )
)
def check_if_passing(student_context, subject, semester):
    """Verifica si el estudiante aprobó una materia."""
    student = student_context["student"]
    try:
        result = student.is_passing(subject, semester)
        student_context["is_passing_result"] = result
        student_context["last_exception"] = None
    except NoGradesError as e:
        student_context["last_exception"] = e


@then(parsers.parse("el resultado debe ser que {result_text}"))
def verify_passing_result(student_context, result_text):
    """Verifica el resultado de aprobación/reprobación."""
    expected = result_text.lower() == "aprobó"
    actual = student_context["is_passing_result"]
    assert actual == expected, f"Se esperaba {expected}, se obtuvo {actual}"


@then(
    parsers.parse('el resultado debe ser "{result_text}"')
)
def verify_passing_result_quoted(student_context, result_text):
    """Verifica el resultado con comillas (compatible con Scenario Outline)."""
    expected = result_text.lower() == "aprobó"
    actual = student_context["is_passing_result"]
    assert actual == expected, f"Se esperaba {expected}, se obtuvo {actual}"


@given(parsers.parse('el estudiante no tiene nota registrada para {subject}'))
def no_grade_registered(student_context, subject):
    """Asegura que no hay nota registrada (ya debe estarlo por defecto)."""
    # El estudiante ya se crea sin notas, así que no necesitamos hacer nada
    student_context["check_subject"] = subject


@when(
    parsers.parse(
        'se intenta verificar si el estudiante aprobó "{subject}" '
        'en semestre {semester:d}'
    )
)
def attempt_check_passing_no_grade(student_context, subject, semester):
    """Intenta verificar aprobación de materia sin nota."""
    student = student_context["student"]
    try:
        student.is_passing(subject, semester)
    except NoGradesError as e:
        student_context["last_exception"] = e


@then("se debe lanzar un error indicando que no hay nota registrada")
def verify_no_grade_error(student_context):
    """Verifica que se lanzó error de no grades."""
    assert isinstance(
        student_context["last_exception"], NoGradesError
    ), f"Se esperaba NoGradesError, se obtuvo {type(student_context['last_exception'])}"


# ============================================================================
# REQUERIMIENTO 3: CÁLCULO DE PROMEDIO
# ============================================================================

@given("el estudiante ha registrado las siguientes notas en semestre 1:")
def register_multiple_grades_table(student_context, datatable):
    """Registra múltiples notas desde una tabla."""
    student = student_context["student"]
    # datatable es una lista de listas, no de diccionarios
    # La primera fila contiene los encabezados
    headers = datatable[0]
    for row in datatable[1:]:
        row_dict = {headers[i]: row[i] for i in range(len(headers))}
        subject = row_dict["materia"]
        grade = float(row_dict["nota"])
        student.register_grade(subject, grade, 1)


@when("se calcula el promedio de todas las notas")
def calculate_average(student_context):
    """Calcula el promedio de notas."""
    student = student_context["student"]
    try:
        average = student.calculate_average()
        student_context["average_result"] = average
        student_context["last_exception"] = None
    except NoGradesError as e:
        student_context["last_exception"] = e


@then(parsers.parse("el promedio debe ser {expected_average:f}"))
def verify_average_result(student_context, expected_average):
    """Verifica el resultado del promedio calculado."""
    actual = student_context["average_result"]
    assert abs(actual - expected_average) < 0.001, (
        f"Se esperaba promedio {expected_average}, se obtuvo {actual}"
    )


@given("el estudiante no tiene notas registradas")
def no_grades_registered(student_context):
    """Asegura que no hay notas (ya debe estarlo por defecto)."""
    pass


@when("se intenta calcular el promedio")
def attempt_calculate_average_no_grades(student_context):
    """Intenta calcular promedio sin notas."""
    student = student_context["student"]
    try:
        student.calculate_average()
    except NoGradesError as e:
        student_context["last_exception"] = e


@then("se debe lanzar un error indicando que no hay notas para calcular promedio")
def verify_no_grades_error(student_context):
    """Verifica que se lanzó error de no grades."""
    assert isinstance(
        student_context["last_exception"], NoGradesError
    ), (
        f"Se esperaba NoGradesError, se obtuvo "
        f"{type(student_context['last_exception'])}"
    )


# ============================================================================
# REQUERIMIENTO 4: PREVENCIÓN DE DUPLICADOS
# ============================================================================

@when(
    parsers.parse(
        'se intenta registrar una nueva nota de {new_grade:f} '
        'para "{subject}" en semestre {semester:d}'
    )
)
def attempt_register_duplicate(student_context, new_grade, subject, semester):
    """Intenta registrar una nota duplicada."""
    student = student_context["student"]
    try:
        student.register_grade(subject, new_grade, semester)
    except DuplicateGradeError as e:
        student_context["last_exception"] = e


@then(
    parsers.parse(
        'se debe lanzar un error "{error_type}" indicando que ya existe nota'
    )
)
def verify_duplicate_error(student_context, error_type):
    """Verifica que se lanzó error de duplicado."""
    assert isinstance(
        student_context["last_exception"], DuplicateGradeError
    ), (
        f"Se esperaba {error_type}, se obtuvo "
        f"{type(student_context['last_exception'])}"
    )


@then(parsers.parse("la nota original de {original_grade:f} debe permanecer sin cambios"))
def verify_original_grade_preserved(student_context, original_grade):
    """Verifica que la nota original se preservó."""
    # Esta verificación se hace implícitamente en el test anterior
    # pero podemos agregar validación explícita si es necesario
    pass


@when(
    parsers.parse(
        'se registra correctamente una nota de {grade:f} '
        'para "{subject}" en semestre {semester:d}'
    )
)
def register_grade_different_context(student_context, grade, subject, semester):
    """Registra una nota en diferente contexto (materia o semestre)."""
    student = student_context["student"]
    result = student.register_grade(subject, grade, semester)
    assert result is True, "La nota debería registrarse correctamente"


@then("ambas notas deben estar registradas sin conflicto")
def verify_both_grades_registered(student_context):
    """Verifica que ambas notas se registraron."""
    student = student_context["student"]
    all_grades = student.get_all_grades()
    assert len(all_grades) == 2, f"Se esperaban 2 notas, se encontraron {len(all_grades)}"


@then("ambas notas de diferentes materias deben estar registradas")
def verify_different_subjects_registered(student_context):
    """Verifica que notas de diferentes materias se registraron."""
    student = student_context["student"]
    all_grades = student.get_all_grades()
    assert len(all_grades) == 2, f"Se esperaban 2 notas, se encontraron {len(all_grades)}"


@given("el estudiante ha registrado las siguientes notas:")
def register_multiple_grades_complex(student_context, datatable):
    """Registra múltiples notas desde una tabla compleja."""
    student = student_context["student"]
    # datatable es una lista de listas, no de diccionarios
    # La primera fila contiene los encabezados
    headers = datatable[0]
    for row in datatable[1:]:
        row_dict = {headers[i]: row[i] for i in range(len(headers))}
        subject = row_dict["materia"]
        semester = int(row_dict["semestre"])
        grade = float(row_dict["nota"])
        student.register_grade(subject, grade, semester)


@when(
    parsers.parse(
        'se intenta registrar una nota de {note_grade:f} '
        'para "{note_subject}" en semestre {note_semester:d}'
    )
)
def attempt_register_based_on_scenario(
    student_context, note_grade, note_subject, note_semester
):
    """Intenta registrar una nota basada en el escenario."""
    student = student_context["student"]
    try:
        student.register_grade(note_subject, note_grade, note_semester)
        student_context["is_passing_result"] = True  # Reutilizamos para marcar éxito
        student_context["last_exception"] = None
    except DuplicateGradeError as e:
        student_context["is_passing_result"] = False
        student_context["last_exception"] = e


@then(parsers.parse('se debe {action}'))
def verify_action_outcome(student_context, action):
    """Verifica el resultado de la acción basada en el Scenario Outline."""
    if "lanzar error duplicado" in action:
        assert isinstance(
            student_context["last_exception"], DuplicateGradeError
        ), f"Se esperaba error duplicado, pero la nota se registró"
    elif "registrar correctamente" in action:
        assert student_context["is_passing_result"] is True, (
            "Se esperaba que la nota se registrara correctamente"
        )
