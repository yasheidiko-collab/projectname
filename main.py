#!/usr/bin/env python3
"""Run the chatbot API from the workspace root."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "chatbot-api"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the chatbot API from the workspace root.")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", default=8000, type=int, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable hot reload")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        import uvicorn
    except ImportError as exc:
        raise ImportError(
            "Missing dependencies. Run the script with the virtual environment: `.venv/bin/python main.py`"
        ) from exc

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)