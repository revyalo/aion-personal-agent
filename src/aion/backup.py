
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

import aion.database as database


REQUIRED_TABLES = {
    "aion_instance",
    "events",
    "memories",
    "memory_sources",
}


def verify_backup(path: Path) -> dict:
    path = Path(path).resolve()

    # Abrimos la copia en modo solo lectura.
    with closing(
        sqlite3.connect(
            f"{path.as_uri()}?mode=ro",
            uri=True,
        )
    ) as connection:
        integrity = connection.execute(
            "PRAGMA integrity_check"
        ).fetchall()

        if integrity != [("ok",)]:
            raise RuntimeError(
                "La copia no supera integrity_check."
            )

        violations = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if violations:
            raise RuntimeError(
                "La copia contiene referencias rotas."
            )

        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table'"
            )
        }

        if not REQUIRED_TABLES.issubset(tables):
            raise RuntimeError(
                "La copia no tiene el esquema esperado de AION."
            )

        identities = connection.execute(
            "SELECT agent_id FROM aion_instance"
        ).fetchall()

        if len(identities) != 1:
            raise RuntimeError(
                "La copia debe contener una única identidad."
            )

        counts = {}

        for table in ("events", "memories", "memory_sources"):
            counts[table] = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

        return {
            "agent_id": identities[0][0],
            **counts,
        }


def create_backup(destination: Path) -> Path:
    source = database.DATABASE_PATH.resolve()
    destination = Path(destination).expanduser().resolve()

    if source == destination:
        raise ValueError(
            "No puedes sobrescribir la base original."
        )

    if not source.is_file():
        raise FileNotFoundError(
            f"No existe la base de datos: {source}"
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Crea un archivo nuevo con permisos privados.
    # O_EXCL impide sobrescribir uno que ya exista.
    fd = os.open(
        destination,
        os.O_CREAT | os.O_EXCL | os.O_WRONLY,
        0o600,
    )
    os.close(fd)

    try:
        with closing(
            sqlite3.connect(
                f"{source.as_uri()}?mode=ro",
                uri=True,
                timeout=10,
            )
        ) as original:
            with closing(
                sqlite3.connect(destination, timeout=10)
            ) as copy:
                original.backup(copy)

        # Una copia inválida no se considera completada.
        verify_backup(destination)

    except BaseException:
        destination.unlink(missing_ok=True)
        raise

    return destination


def main():
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    destination = (
        database.DATABASE_PATH.parent
        / "backups"
        / f"aion-{timestamp}.db"
    )

    try:
        backup_path = create_backup(destination)
        report = verify_backup(backup_path)

    except (OSError, sqlite3.Error, ValueError, RuntimeError) as error:
        raise SystemExit(
            f"ERROR: No se pudo completar el backup: {error}"
        ) from error

    print(f"Backup verificado: {backup_path}")
    print(f"Identidad: {report['agent_id']}")
    print(f"Eventos: {report['events']}")
    print(f"Memorias: {report['memories']}")
    print(f"Referencias: {report['memory_sources']}")


if __name__ == "__main__":
    main()

