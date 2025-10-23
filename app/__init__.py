"""app package initializer - makes the `app` directory a Python package.

Creating this file fixes ModuleNotFoundError when importing `app` as a package.
"""

__all__ = ["models", "services"]
