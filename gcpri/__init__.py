"""GCP Resource Inventory (GCPRI).

Utilities for collecting a cross-project inventory of Google Cloud Platform
resources using the Cloud Asset API.
"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # pragma: no cover - Python <3.8
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

try:
    __version__ = version("gcpri")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.1.0"

