from aion.core import AionCore
from aion.instance_lock import (
    InstanceAlreadyRunningError,
    single_instance_lock,
)


def run_cli():
    aion = AionCore()

    print("AION")
    print(f"Identity: {aion.identity.agent_id}")
    print("Escribe 'exit' para salir.\n")

    while True:
        try:
            message = input("You > ")
        except (EOFError, KeyboardInterrupt):
            print("\nAION > Hasta luego.")
            break

        if message.lower() == "exit":
            print("AION > Hasta luego.")
            break

        try:
            response = aion.chat(message)
            print(f"AION > {response}")

        except Exception as error:
            print()
            print(
                "AION > No he podido obtener "
                "una respuesta del proveedor."
            )
            print(f"ERROR > {error}")
            print()


def main():
    try:
        # Primero adquirimos el bloqueo.
        # Después iniciamos el Core.
        with single_instance_lock():
            run_cli()

    except InstanceAlreadyRunningError as error:
        print(f"AION > {error}")


if __name__ == "__main__":
    main()
