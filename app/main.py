import sys

def main():
    builtIns = ["exit", "echo", "type"]
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
            case "type":
                args = command[4:].strip()
                if args in builtIns:
                    print(f"{args} is a shell builtin")
                else:
                    print(f"{args}: not found")
                continue
            case _:
                print(f"{command}: command not found")
                continue


if __name__ == "__main__":
    main()
