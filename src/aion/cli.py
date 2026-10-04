from aion.core import AionCore


def main():
    aion = AionCore()

    print("AION")
    print(f"Identity: {aion.identity.agent_id}")
    print("Escribe 'exit' para salir.\n")

    while True:
        message = input("You > ")

        if message.lower() == "exit":
            print("AION > Hasta luego.")
            break

        try:
            response = aion.chat(message)
            print(f"AION > {response}")

        except Exception as error:
            print()
            print("AION > No he podido obtener una respuesta del proveedor.")
            print(f"ERROR > {error}")
            print()


if __name__ == "__main__":
    main()