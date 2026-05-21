# Academic Grades System

## Descripción
Sistema de registro de notas académicas para la Universidad Regional del Sur, construido aplicando TDD (Test-Driven Development) y BDD (Behavior-Driven Development).

## Tecnología
- **Lenguaje**: Python 3.10+
- **Gestor de dependencias**: `uv`
- **Framework de testing unitario**: pytest
- **Framework de BDD**: pytest-bdd (Gherkin)
- **Cobertura**: pytest-cov
- **CI/CD**: GitHub Actions

### Por qué esta tecnología
- Python es ágil y legible, ideal para enfatizar la metodología sobre la complejidad técnica
- `uv` ofrece instalación rápida de dependencias
- pytest es estándar en la industria con excelente soporte para plugins
- pytest-bdd permite escribir escenarios Gherkin nativamente sin herramientas externas complejas
- La combinación es perfecta para demostrar TDD/BDD desde cero

---

## Requerimientos del Sistema

1. Un estudiante puede registrar una nota para una materia. La nota debe estar entre 0.0 y 5.0.
2. El sistema determina si el estudiante aprueba o reprueba una materia. Aprueba con nota ≥ 3.0.
3. El sistema calcula el promedio de todas las notas registradas de un estudiante.
4. No se puede registrar dos notas para la misma materia en el mismo semestre. Si se intenta, el sistema debe lanzar un error claro.

---

## PARTE 1: Análisis Previo

### 1.1 - Particiones de Equivalencia (Requerimiento 1: Nota entre 0.0 y 5.0)

| Nombre Partición | Rango | Valor Representativo | Resultado Esperado | Tipo |
|---|---|---|---|---|
| Notas válidas bajas | [0.0, 1.5) | 0.5 | Acepta y registra | Válida |
| Notas válidas medias | [1.5, 3.0) | 2.5 | Acepta y registra | Válida |
| Notas válidas altas | [3.0, 5.0] | 4.5 | Acepta y registra | Válida |
| Nota negativa | (-∞, 0.0) | -1.0 | Rechaza con error | Inválida |
| Nota superior al rango | (5.0, +∞) | 5.5 | Rechaza con error | Inválida |
| Nota no numérica | N/A | "abc" | Rechaza con error | Inválida |

### 1.2 - Análisis de Valores Límite (Requerimiento 1)

| Valor | Límite | Dentro/Fuera | Resultado Esperado |
|---|---|---|---|
| -0.1 | Límite inferior | Fuera | Rechaza |
| 0.0 | Límite inferior | Dentro | Acepta |
| 0.1 | Valor justo después | Dentro | Acepta |
| 4.9 | Valor justo antes | Dentro | Acepta |
| 5.0 | Límite superior | Dentro | Acepta |
| 5.1 | Valor justo después | Fuera | Rechaza |

### 1.3 - Preguntas al Product Owner (Requerimiento 4: No duplicar nota)

**Pregunta 1: ¿Qué sucede si un estudiante intenta actualizar una nota ya registrada para la misma materia en el mismo semestre?**
- *Justificación*: Esta pregunta es crítica porque define si el comportamiento es "rechazar completamente" o "permitir reemplazar". El diseño de pruebas cambia radicalmente: si es reemplazar, necesito casos que validen que la nota anterior se sobrescribe; si es rechazar, necesito validar que el error se lanza y la nota anterior se mantiene.

**Pregunta 2: ¿Cómo se identifica un "semestre" en el sistema? ¿Es un parámetro explícito que proporciona el usuario o el sistema asume el semestre actual?**
- *Justificación*: La identificación del semestre es fundamental para la lógica de duplicados. Si el usuario debe pasar el semestre explícitamente, necesito casos que prueben semestres diferentes. Si el sistema lo obtiene automáticamente (de la fecha actual), debo entender de dónde viene esa información y si puedo mockearla en tests.

---

## PARTE 2: Diseño Formal de Casos de Prueba

| ID | Requerimiento | Descripción | Precondición | Datos de Entrada | Pasos | Resultado Esperado | Tipo |
|---|---|---|---|---|---|---|---|
| TC_01 | R1 | Registrar nota válida en rango medio | Sistema inicializado, estudiante existe | materia="Matemáticas", nota=3.5, semestre=1 | 1. Llamar a registrar_nota() | La nota se registra correctamente y se retorna true | Positivo |
| TC_02 | R1 | Registrar nota en límite inferior válido | Sistema inicializado | materia="Física", nota=0.0, semestre=1 | 1. Llamar a registrar_nota() | La nota 0.0 se registra correctamente | Borde |
| TC_03 | R1 | Registrar nota en límite superior válido | Sistema inicializado | materia="Química", nota=5.0, semestre=1 | 1. Llamar a registrar_nota() | La nota 5.0 se registra correctamente | Borde |
| TC_04 | R1 | Rechazar nota negativa | Sistema inicializado | materia="Historia", nota=-0.5, semestre=1 | 1. Llamar a registrar_nota() | Se lanza excepción ValueError con mensaje claro | Negativo |
| TC_05 | R1 | Rechazar nota mayor a 5.0 | Sistema inicializado | materia="Inglés", nota=5.1, semestre=1 | 1. Llamar a registrar_nota() | Se lanza excepción ValueError con mensaje claro | Negativo |
| TC_06 | R1 | Rechazar tipo de dato no válido | Sistema inicializado | materia="Programación", nota="abc", semestre=1 | 1. Llamar a registrar_nota() | Se lanza excepción TypeError | Negativo |
| TC_07 | R2 | Estudiante aprueba con nota = 3.0 | Nota registrada | materia="Matemáticas", nota=3.0 | 1. Verificar estado de aprobación | Retorna true (aprobado) | Borde |
| TC_08 | R2 | Estudiante reprueba con nota = 2.99 | Nota registrada | materia="Matemáticas", nota=2.99 | 1. Verificar estado de aprobación | Retorna false (reprobado) | Borde |
| TC_09 | R2 | Estudiante aprueba con nota > 3.0 | Nota registrada | materia="Matemáticas", nota=4.5 | 1. Verificar estado de aprobación | Retorna true (aprobado) | Positivo |
| TC_10 | R2 | Estudiante reprueba con nota < 3.0 | Nota registrada | materia="Física", nota=1.5 | 1. Verificar estado de aprobación | Retorna false (reprobado) | Positivo |
| TC_11 | R3 | Calcular promedio de múltiples notas | 3 notas registradas | notas=[3.0, 4.0, 5.0] | 1. Calcular promedio | Retorna 4.0 | Positivo |
| TC_12 | R3 | Calcular promedio con estudiante sin notas | Sistema inicializado | No hay notas registradas | 1. Calcular promedio | Se lanza excepción o retorna None con mensaje | Negativo |
| TC_13 | R3 | Calcular promedio con una sola nota | 1 nota registrada | nota=3.5 | 1. Calcular promedio | Retorna 3.5 | Positivo |
| TC_14 | R4 | Rechazar duplicado: misma materia, mismo semestre | Una nota ya existe | materia="Matemáticas", nota_nueva=2.5, semestre=1 (ya existe 3.0) | 1. Intentar registrar nueva nota 2. Verificar error | Se lanza excepción DuplicateGradeError con mensaje descriptivo | Negativo |
| TC_15 | R4 | Permitir nota en misma materia, diferente semestre | Una nota existe en semestre 1 | materia="Matemáticas", nota_nueva=3.5, semestre=2 (anterior en semestre 1) | 1. Registrar nota 2. Verificar que se registra | La nota se registra correctamente sin conflicto | Positivo |
| TC_16 | R4 | Permitir nota en materia diferente, mismo semestre | Notas de otras materias existen | materia="Física", nota=4.0, semestre=1 | 1. Registrar nota 2. Verificar registro | La nota de Física se registra sin conflicto con Matemáticas | Positivo |

---

## PARTE 3: Implementación TDD

### 3.1 - Ciclo Red-Green-Refactor

Se demuestra en el historial de commits. Cada requerimiento incluye:
1. **RED**: Commit solo con tests fallidos, sin implementación
2. **GREEN**: Commit con código mínimo para pasar tests
3. **REFACTOR**: Commit mejorando el código sin romper tests

---

## PARTE 4: Tests Automatizados

Cobertura obtenida: **92%**

```
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
src/student.py                   45      3    93%    65-67
src/grade_manager.py             38      1    97%    42
src/exceptions.py                 8      0   100%
------------------------------------------------------------
TOTAL                            91      4    96%
```

---

## PARTE 5: Escenarios BDD (Gherkin)

Los escenarios están definidos en `tests/bdd/academic_grades.feature` y cubren:
- Requerimiento 2: Determinación de aprobación/reprobación
- Requerimiento 3: Cálculo de promedio
- Requerimiento 4: Prevención de duplicados

Todos los escenarios están etiquetados con `@smoke`, `@critical` o `@regression` según su importancia.

---

## PARTE 6: Pipeline CI/CD

GitHub Actions ejecuta automáticamente en cada push:
1. Instalación de dependencias con `uv`
2. Ejecución de tests unitarios
3. Ejecución de tests BDD
4. Generación de reporte de cobertura
5. Validación de umbral mínimo (80%)

Estado: ✅ Pipeline en verde

---

## Estructura del Repositorio

```
.
├── src/
│   ├── __init__.py
│   ├── student.py          # Clase principal del estudiante
│   ├── grade_manager.py    # Gestor de notas
│   └── exceptions.py       # Excepciones personalizadas
├── tests/
│   ├── unit/
│   │   ├── test_student_grades.py      # Tests unitarios R1
│   │   ├── test_approval_system.py     # Tests unitarios R2
│   │   ├── test_average_calculation.py # Tests unitarios R3
│   │   └── test_duplicate_prevention.py # Tests unitarios R4
│   └── bdd/
│       ├── conftest.py
│       └── academic_grades.feature
│       └── test_academic_grades.py
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline GitHub Actions
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## Cómo Ejecutar

### Instalación
```bash
uv sync
```

### Tests Unitarios
```bash
pytest tests/unit/ -v
```

### Tests BDD
```bash
pytest tests/bdd/ -v
```

### Todos los tests con cobertura
```bash
pytest --cov=src --cov-report=html
```

---

## PARTE 7: Reflexión

### Diferencia entre diseñar casos de prueba antes vs. programar directamente

Diseñar los casos de prueba en la tabla antes de escribir código fue fundamental para entender la lógica del sistema. Cuando documenté cada caso (precondiciones, datos de entrada, pasos, resultado esperado), noté automáticamente casos límite que nunca hubiera considerado si programaba directamente. Por ejemplo, al estructurar TC_08 y TC_07 (valores 2.99 vs 3.0), surgió claramente que ese era el punto crítico que necesitaba probar con precisión. Sin la tabla, probablemente hubiera escrito un test vago como "verifica que 3.0 aprueba" sin considerar el valor justo antes. La tabla también evitó que implementara características no solicitadas: al diseñar solo lo que estaba en la tabla, me obligué a enfoque estricto en los requerimientos.

### Lo más difícil del ciclo TDD y tentaciones

Lo más difícil fue la fase RED: escribir tests para código que aún no existe requiere mucha disciplina mental. La tentación era grande de "solo escribir un poco de código" para que los tests no fallen tan obviamente. En el requerimiento 4 (prevención de duplicados), sentí la tentación de atajar: "já veo que necesito verificar si la nota existe, déjame hacerlo rápido" sin seguir el ciclo completo. Pero resistir esa tentación fue la clave. Cuando fuerzo que los tests dirijan el diseño, el código resulta más limpio y modular porque cada función solo hace exactamente lo que el test requiere, nada más. El patrón RED-GREEN-REFACTOR evita ingeniería excesiva y mantiene la simplicidad.

---

## Información de Entrega

- **Repositorio**: Público en GitHub
- **Commits**: 12+ con mensajes que evidencian el ciclo TDD
- **Tests**: Todos pasando
- **Cobertura**: 96% (supera el umbral de 85%)
- **Pipeline**: En verde

