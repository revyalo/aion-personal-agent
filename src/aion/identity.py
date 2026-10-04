import uuid

from aion.database import get_connection

class Identity:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id


def load_or_create_identity():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS aion_instance (
            agent_id TEXT PRIMARY KEY
        )
    """)

    row = connection.execute(
        "SELECT agent_id FROM aion_instance LIMIT 1"
    ).fetchone()

    if row is not None:
        agent_id = row[0]
    else:
        agent_id = str(uuid.uuid4())

        connection.execute(
            "INSERT INTO aion_instance (agent_id) VALUES (?)",
            (agent_id,)
        )

        connection.commit()

    connection.close()

    return Identity(agent_id)