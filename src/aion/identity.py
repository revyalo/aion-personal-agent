
import uuid

from aion.database import get_connection


class Identity:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id


def load_or_create_identity():
    connection = get_connection()

    try:
        # Reservamos la escritura antes de leer la identidad.
        connection.execute("BEGIN IMMEDIATE")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS aion_instance (
                agent_id TEXT PRIMARY KEY
            )
        """)

        # Leemos hasta dos filas para detectar inconsistencias.
        rows = connection.execute(
            "SELECT agent_id FROM aion_instance LIMIT 2"
        ).fetchall()

        if len(rows) > 1:
            raise RuntimeError(
                "La base de datos contiene varias "
                "identidades de AION."
            )

        if rows:
            agent_id = rows[0][0]
        else:
            agent_id = str(uuid.uuid4())

            connection.execute(
                "INSERT INTO aion_instance (agent_id) VALUES (?)",
                (agent_id,),
            )

        connection.commit()
        return Identity(agent_id)

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
