
from contextlib import closing

import aion.database as database


SCHEMA_VERSION = 1
SINGLETON_INDEX = "ux_aion_instance_singleton"

REQUIRED_TABLES = {
    "aion_instance",
    "events",
    "memories",
    "memory_sources",
}


def migrate_database() -> int:
    database_path = database.DATABASE_PATH

    # Nunca crear silenciosamente una base nueva.
    if not database_path.is_file():
        raise FileNotFoundError(
            f"No existe la base de datos: {database_path}"
        )

    with closing(database.get_connection()) as connection:
        try:
            # Bloquea escrituras concurrentes durante la migración.
            connection.execute("BEGIN IMMEDIATE")

            version = connection.execute(
                "PRAGMA user_version"
            ).fetchone()[0]

            if version > SCHEMA_VERSION:
                raise RuntimeError(
                    "La base de datos utiliza una versión "
                    "más reciente que este código."
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
                    "Faltan tablas necesarias de AION."
                )

            integrity = connection.execute(
                "PRAGMA integrity_check"
            ).fetchall()

            if integrity != [("ok",)]:
                raise RuntimeError(
                    "La base de datos no supera integrity_check."
                )

            if connection.execute(
                "PRAGMA foreign_key_check"
            ).fetchall():
                raise RuntimeError(
                    "Existen referencias de datos inválidas."
                )

            identities = connection.execute(
                "SELECT agent_id FROM aion_instance LIMIT 2"
            ).fetchall()

            if len(identities) != 1:
                raise RuntimeError(
                    "AION necesita exactamente una identidad."
                )

            if version == 0:
                # Un índice único sobre una constante permite
                # una sola fila en toda la tabla.
                connection.execute(
                    "CREATE UNIQUE INDEX "
                    "ux_aion_instance_singleton "
                    "ON aion_instance ((1))"
                )

                connection.execute(
                    "PRAGMA user_version = 1"
                )

            # Comprobamos que la garantía existe en v1.
            indexes = connection.execute(
                "PRAGMA index_list('aion_instance')"
            ).fetchall()

            singleton_exists = any(
                row[1] == SINGLETON_INDEX and row[2] == 1
                for row in indexes
            )

            if not singleton_exists:
                raise RuntimeError(
                    "Falta el índice único de identidad."
                )

            connection.commit()
            return SCHEMA_VERSION

        except BaseException:
            connection.rollback()
            raise

