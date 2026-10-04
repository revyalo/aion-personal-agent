import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/aion.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    return connection