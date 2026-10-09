import sqlite3
from pathlib import Path


# Raíz del proyecto AION.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Base de datos persistente.
DATABASE_PATH = PROJECT_ROOT / "data" / "aion.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection
