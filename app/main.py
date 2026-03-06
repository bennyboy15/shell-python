import sys
import os

def searchForExecutable(fileToFind):
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)

    for directory in directories:
        fullPath = directory + "/" + fileToFind
        # IF EXISTS AND HAS EXECUTABLE PERMISSIONS
        if os.access(fullPath, os.F_OK) and os.access(fullPath, os.X_OK):
            print(f"{fileToFind} is {fullPath}")
            return
    print(f"{fileToFind}: not found")

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
                    searchForExecutable(args)
                    #print(f"{args}: not found")
                continue
            case _:
                print(f"{command}: command not found")
                continue


if __name__ == "__main__":
    main()
