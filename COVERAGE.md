"""
Documentación de Test Coverage

Total: 47 tests (28 unitarios + 19 BDD)

REQUERIMIENTO 1: Validación de notas (Rango 0.0-5.0)
- TC_01: Registrar nota válida en rango medio
- TC_02: Registrar nota en límite inferior (0.0)
- TC_03: Registrar nota en límite superior (5.0)
- TC_04: Rechazar nota negativa (-0.5)
- TC_05: Rechazar nota > 5.0 (5.1)
- TC_06: Rechazar tipo no numérico
+ 4 tests adicionales de bordes
TOTAL: 10 tests
COBERTURA: 100%

REQUERIMIENTO 2: Sistema de Aprobación (nota >= 3.0)
- TC_07: Aprueba con nota = 3.0
- TC_08: Reprueba con nota = 2.99
- TC_09: Aprueba con nota > 3.0 (4.5)
- TC_10: Reprueba con nota < 3.0 (1.5)
+ 3 tests adicionales
+ 8 escenarios BDD
TOTAL: 14 tests
COBERTURA: 100%

REQUERIMIENTO 3: Cálculo de Promedio
- TC_11: Promedio de múltiples notas (3.0, 4.0, 5.0)
- TC_12: Error sin notas registradas
- TC_13: Promedio de una sola nota
+ 3 tests adicionales
+ 3 escenarios BDD
TOTAL: 9 tests
COBERTURA: 100%

REQUERIMIENTO 4: Prevención de Duplicados
- TC_14: Rechazar duplicado (misma materia, mismo semestre)
- TC_15: Permitir misma materia, diferente semestre
- TC_16: Permitir diferente materia, mismo semestre
+ 2 tests adicionales
+ 4 escenarios BDD (incluyendo Scenario Outline)
TOTAL: 9 tests
COBERTURA: 100%

COBERTURA GENERAL:
- src/__init__.py: 100%
- src/exceptions.py: 100% (6 statements)
- src/grade_manager.py: 100% (40 statements, 10 branches)
- src/student.py: 100% (16 statements)
TOTAL: 100% (62 statements)

CICLO TDD APLICADO:
1. RED: Todos los tests se escribieron sin implementación
2. GREEN: Implementación mínima para pasar todos los tests
3. REFACTOR: Extracción de validaciones a métodos privados

VALIDACIÓN BDD:
- 19 escenarios en total
- 6+ escenarios de aprobación/reprobación
- 1+ Scenario Outline con tabla de Examples
- 1+ escenario de manejo de errores
- Tags: @smoke, @critical, @regression
- Lenguaje de negocio comprensible para no-técnicos

PIPELINE CI/CD:
- GitHub Actions configurado
- Ejecuta tests unitarios y BDD
- Reporta cobertura >= 80%
- Workflow en .github/workflows/ci.yml
"""
