Feature: Sistema de Registro de Notas Académicas
  Como estudiante de la Universidad Regional del Sur
  Quiero registrar mis notas académicas por materia y semestre
  Para poder conocer mi desempeño y calcular mis promedios

  Background:
    Given un estudiante registrado en el sistema con ID "EST001" y nombre "Carlos Sánchez"

  # Requerimiento 2: Sistema de Aprobación/Reprobación
  @smoke @critical
  Scenario: Estudiante aprueba una materia con nota igual al mínimo aprobatorio
    Given el estudiante ha registrado una nota de 3.0 para "Matemáticas" en semestre 1
    When se verifica si el estudiante aprobó "Matemáticas" en semestre 1
    Then el resultado debe ser que aprobó

  @critical
  Scenario: Estudiante reprueba una materia con nota justo debajo del mínimo aprobatorio
    Given el estudiante ha registrado una nota de 2.99 para "Física" en semestre 1
    When se verifica si el estudiante aprobó "Física" en semestre 1
    Then el resultado debe ser que reprobó

  @smoke
  Scenario Outline: Verificar aprobación con diferentes notas
    Given el estudiante ha registrado una nota de <nota> para "<materia>" en semestre 1
    When se verifica si el estudiante aprobó "<materia>" en semestre 1
    Then el resultado debe ser "<resultado>"

    Examples: Notas y resultados
      | nota | materia      | resultado |
      | 5.0  | Inglés       | aprobó    |
      | 4.5  | Química      | aprobó    |
      | 3.0  | Historia     | aprobó    |
      | 2.99 | Biología     | reprobó   |
      | 1.5  | Geografía    | reprobó   |
      | 0.0  | Educación    | reprobó   |

  @regression
  Scenario: Intento de verificar aprobación sin nota registrada genera error
    Given el estudiante no tiene nota registrada para Educación Física
    When se intenta verificar si el estudiante aprobó "Educación Física" en semestre 1
    Then se debe lanzar un error indicando que no hay nota registrada

  # Requerimiento 3: Cálculo de Promedio
  @smoke @critical
  Scenario: Calcular promedio con múltiples notas registradas
    Given el estudiante ha registrado las siguientes notas en semestre 1:
      | materia      | nota |
      | Matemáticas  | 3.0  |
      | Física       | 4.0  |
      | Química      | 5.0  |
    When se calcula el promedio de todas las notas
    Then el promedio debe ser 4.0

  @critical
  Scenario: Calcular promedio con una sola nota registrada
    Given el estudiante ha registrado una nota de 3.5 para "Historia" en semestre 1
    When se calcula el promedio de todas las notas
    Then el promedio debe ser 3.5

  @regression
  Scenario: Intento de calcular promedio sin notas registradas genera error
    Given el estudiante no tiene notas registradas
    When se intenta calcular el promedio
    Then se debe lanzar un error indicando que no hay notas para calcular promedio

  # Requerimiento 4: Prevención de Duplicados
  @smoke @critical
  Scenario: Rechazar intento de registrar nota duplicada en misma materia y semestre
    Given el estudiante ha registrado una nota de 3.0 para "Matemáticas" en semestre 1
    When se intenta registrar una nueva nota de 2.5 para "Matemáticas" en semestre 1
    Then se debe lanzar un error "DuplicateGradeError" indicando que ya existe nota
    And la nota original de 3.0 debe permanecer sin cambios

  @smoke
  Scenario: Permitir registrar nota en misma materia pero diferente semestre
    Given el estudiante ha registrado una nota de 3.0 para "Matemáticas" en semestre 1
    When se registra correctamente una nota de 3.5 para "Matemáticas" en semestre 2
    Then ambas notas deben estar registradas sin conflicto

  @smoke
  Scenario: Permitir registrar nota en diferente materia pero mismo semestre
    Given el estudiante ha registrado una nota de 4.0 para "Matemáticas" en semestre 1
    When se registra correctamente una nota de 3.5 para "Física" en semestre 1
    Then ambas notas de diferentes materias deben estar registradas

  @regression
  Scenario Outline: Validar prevención de duplicados con múltiples combinaciones
    Given el estudiante ha registrado las siguientes notas:
      | materia     | semestre | nota |
      | Matemáticas | 1        | 4.0  |
      | Física      | 1        | 3.5  |
      | Matemáticas | 2        | 3.8  |
    When se intenta registrar una nota de <nota> para "<materia>" en semestre <semestre>
    Then se debe <resultado>

    Examples: Combinaciones de materias y semestres
      | materia     | semestre | nota | resultado              |
      | Matemáticas | 1        | 2.5  | lanzar error duplicado |
      | Física      | 1        | 4.0  | lanzar error duplicado |
      | Química     | 1        | 3.0  | registrar correctamente |
      | Matemáticas | 3        | 3.9  | registrar correctamente |
