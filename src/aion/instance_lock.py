import fcntl
from contextlib import contextmanager

import aion.database as database


class InstanceAlreadyRunningError(RuntimeError):
    pass


@contextmanager
def single_instance_lock():
    # Cada base de datos tiene su propio archivo de bloqueo.
    lock_path = database.DATABASE_PATH.with_suffix(".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("a+") as lock_file:
        try:
            # Intentamos obtener un bloqueo exclusivo sin esperar.
            fcntl.flock(
                lock_file.fileno(),
                fcntl.LOCK_EX | fcntl.LOCK_NB,
            )
        except BlockingIOError as error:
            raise InstanceAlreadyRunningError(
                "AION ya está ejecutándose con esta base "
                "de datos. Cierra la otra instancia primero."
            ) from error

        try:
            # Mantenemos el bloqueo durante toda la sesión.
            yield
        finally:
            # Se libera incluso si ocurre una excepción.
            fcntl.flock(
                lock_file.fileno(),
                fcntl.LOCK_UN,
            )

