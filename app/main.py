import sys

def main():
    while (True):
        command = input("$ ").strip()
        func = command.split(" ")[0].strip()
        args = command.split(" ")[1:]
        match(func):
            case "exit":
                sys.exit()
                continue
            case "echo":
                print(command[5:])
                continue
            case _:
                print(f"{command}: command not found")
                continue


if __name__ == "__main__":
    main()
