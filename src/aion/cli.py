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

        response = aion.chat(message)

        print(f"AION > {response}")


if __name__ == "__main__":
    main()