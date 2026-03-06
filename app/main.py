import sys

def main():
    while (True):
        command = input("$ ")
        match(command):
            case "exit":
                sys.exit()
                continue
            case _:
                print(f"{command}: command not found")
                continue


if __name__ == "__main__":
    main()
