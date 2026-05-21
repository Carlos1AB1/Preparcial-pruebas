# Guía Rápida de Ejecución

## Requisitos Previos
- Python 3.10+
- `uv` (gestor de dependencias moderno)

## Instalación
```bash
uv sync
```

## Ejecutar Tests

### Tests Unitarios (28 + 4 integración = 32 tests)
```bash
uv run pytest tests/unit/ -v
```

### Tests BDD (19 escenarios)
```bash
uv run pytest tests/bdd/ -v
```

### Todos los Tests (51 total)
```bash
uv run pytest tests/ -v
```

### Con Reporte de Cobertura
```bash
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
```

## Resultados Esperados
- ✅ 51 tests pasando
- ✅ 100% de cobertura
- ✅ 0 warnings en la lógica del código
- ✅ Ejecución en < 1 segundo

## Información de Commits

El repositorio contiene 8 commits demonstrando el ciclo completo de TDD:

1. **SETUP**: Estructura inicial y análisis (Parte 1-2)
2. **🔴 RED**: Tests sin implementación
3. **🟢 GREEN**: Implementación mínima
4. **🔵 REFACTOR**: Mejora de código
5. **PART 4**: BDD Gherkin + step definitions
6. **DOCS**: Documentación de cobertura
7. **DOCS**: Actualización de README con resultados
8. **TESTS**: Tests de integración

## Estructura del Proyecto

```
.
├── src/                       # Código de producción
│   ├── exceptions.py         # Excepciones personalizadas
│   ├── grade_manager.py      # Lógica de gestión de notas
│   └── student.py            # Clase estudiante
├── tests/                     # Tests
│   ├── unit/                 # Tests unitarios (32 tests)
│   └── bdd/                  # Tests BDD (19 escenarios)
├── .github/workflows/        # Pipeline CI/CD
├── README.md                 # Documentación completa
└── pyproject.toml            # Configuración de proyecto
```

## Notas Importantes

- La cobertura del 100% indica que cada línea de código está probada
- Los tests BDD están escritos en lenguaje de negocio comprensible
- El ciclo TDD está evidenciado en el historial de commits
- El pipeline está configurado para fallar si la cobertura < 80%
