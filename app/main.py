import sys
import os
import subprocess

def searchForExecutable(fileToFind, printOutput):
    system_path = os.environ.get('PATH')
    directories = system_path.split(os.pathsep)

    for directory in directories:
        fullPath = directory + "/" + fileToFind
        # IF EXISTS AND HAS EXECUTABLE PERMISSIONS
        if os.access(fullPath, os.F_OK) and os.access(fullPath, os.X_OK):
            if printOutput:
                print(f"{fileToFind} is {fullPath}")
            return True
    if printOutput:
        print(f"{fileToFind}: not found")
    return False

def executeProgram(fullPath, args, output_file=None):
    try:
        if output_file:
            with open(output_file, "w") as file:
                subprocess.run([fullPath] + args, stdout=file, text=True) 
        else:       
            subprocess.run([fullPath] + args, text=True)
    except:
        pass

def changeDirectory(path):
    if path[0] == "~":
        home_dir = os.environ.get("HOME", "/")
        os.chdir(home_dir)
        return
    
    if os.access(path, os.F_OK):
        os.chdir(path)
    else:
        print(f"cd: {path}: No such file or directory")

def parseCommand(command):
    args = []
    current_arg = ""
    inSingleQuotes = False
    inDoubleQuotes = False
    
    i = 0
    while i < len(command):
        char = command[i]

        if char == "'" and not inDoubleQuotes:
            inSingleQuotes = not inSingleQuotes
        elif char == '"' and not inSingleQuotes:
            inDoubleQuotes = not inDoubleQuotes
        elif char == " " and not inSingleQuotes and not inDoubleQuotes:
            if current_arg:
                args.append(current_arg)
                current_arg = ""
        elif char == "\\" and not inSingleQuotes:
            if (i+1 < len(command)):
                current_arg+=command[i+1]
            i+=1
        else:
            current_arg += char
        i += 1
        
    if current_arg:
        args.append(current_arg)
        
    return args

def main():
    builtIns = ["exit", "echo", "type", "pwd", "cd"]
    while (True):
        command = input("$ ").strip()
        func = parseCommand(command)[0]
        args = parseCommand(command)[1:]
        match(func):
            case "exit":
                sys.exit()
                continue
            case "echo":
                print(" ".join(args))
                continue
            case "type":
                args = command[4:].strip()
                if args in builtIns:
                    print(f"{args} is a shell builtin")
                else:
                    searchForExecutable(args, True)
                    #print(f"{args}: not found")
                continue
            case "pwd":
                cwd = os.getcwd()
                print(cwd)
                continue
            case "cd":
                args = command[2:].strip()
                changeDirectory(args)
                continue
            case _:
                isExec = searchForExecutable(func, False)
                if isExec:
                    if ">" in args:
                        executeProgram(func, args, output_file=args[3])
                    else:
                        executeProgram(func, args)
                else:
                    print(f"{command}: not found")
                continue


if __name__ == "__main__":
    main()
