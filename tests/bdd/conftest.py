"""
Configuración compartida para los tests BDD.
"""

import pytest


def pytest_configure(config):
    """Configura pytest para BDD."""
    config.addinivalue_line(
        "markers",
        "smoke: Marca tests críticos que deben ejecutarse siempre",
    )
    config.addinivalue_line(
        "markers",
        "critical: Marca tests de funcionalidad crítica",
    )
    config.addinivalue_line(
        "markers",
        "regression: Marca tests de regresión",
    )
