import inspect
import os
from sys import path
from typing import Any, Dict, List

anyscale_dir = os.path.dirname(os.path.abspath(__file__))
path.append(os.path.join(anyscale_dir, "client"))
path.append(os.path.join(anyscale_dir, "sdk"))
ANYSCALE_RAY_DIR = os.path.join(anyscale_dir, "anyscale_ray")

from anyscale.connect import SessionBuilder  # noqa: E402

# Auto-add all Anyscale connect builder functions to the top-level.
for attr, _ in inspect.getmembers(SessionBuilder, inspect.isfunction):
    if attr.startswith("_"):
        continue

    def _new_builder(attr: str) -> Any:
        def new_session_builder(*a: List[Any], **kw: Dict[str, Any]) -> Any:
            """Start building an Anyscale session.

            See ``anyscale.SessionBuilder`` for documentation of this
            experimental feature.
            """

            builder = SessionBuilder()
            return getattr(SessionBuilder, attr)(builder, *a, **kw)

        return new_session_builder

    globals()[attr] = _new_builder(attr)

__version__ = "0.3.34"

ANYSCALE_ENV = os.environ.copy()
ANYSCALE_ENV["PYTHONPATH"] = ANYSCALE_RAY_DIR + ":" + ANYSCALE_ENV.get("PYTHONPATH", "")
