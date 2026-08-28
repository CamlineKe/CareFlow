"""Load shared fixtures for package tests under ``app/*/tests/``.

pytest 8+ forbids ``pytest_plugins`` in nested conftest files. Declare it
once at the backend rootdir so ``tests/conftest.py`` is not registered twice.
"""

pytest_plugins = ["tests.conftest"]
