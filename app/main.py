import sys
import os
import subprocess
import readline

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

def executeProgram(fullPath, args, output_file=None, target_stream="stdout", append=False):
    try:
        if output_file:
            if append:
                with open(output_file, "a") as file:
                    if target_stream == "stderr":
                        subprocess.run([fullPath] + args, stderr=file, text=True)
                    else:
                        subprocess.run([fullPath] + args, stdout=file, text=True) 
            else:    
                with open(output_file, "w") as file:
                    if target_stream == "stderr":
                        subprocess.run([fullPath] + args, stderr=file, text=True)
                    else:
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

def handleRedirect(func, args):
    target_stream = "stdout"
    append = False
    if ">" in args:
        index = args.index(">")
    elif "1>" in args:
        index = args.index("1>")
    elif ">>" in args:
        index = args.index(">>")
        append = True
    elif "1>>" in args:
        index = args.index("1>>")
        append = True
    elif "2>" in args:
        index = args.index("2>")
        target_stream = "stderr"
    elif "2>>" in args:
        index = args.index("2>>")
        target_stream = "stderr"
        append=True
    else:
        index = None
    output_path = args[index + 1]
    actual_args = args[:index]

    if append:
        executeProgram(func, actual_args, output_file=output_path, target_stream=target_stream, append=append)
    else:
        executeProgram(func, actual_args, output_file=output_path, target_stream=target_stream)

def isRedirectionOrAppend(args):
    return ">" in args or "1>" in args or ">>" in args or "1>>" in args or "2>" in args or "2>>" in args

def get_all_executables(BUILTINS):
    execs = set(BUILTINS)
    path_str = os.environ.get('PATH', '')
    
    for directory in path_str.split(os.pathsep):
        if os.path.isdir(directory):
            try:
                for filename in os.listdir(directory):
                    full_path = os.path.join(directory, filename)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        execs.add(filename)
            except PermissionError:
                continue
    return sorted(list(execs))

def completer(text, state):
    options = [i for i in CACHED_COMMANDS if i.startswith(text)]

    if state < len(options):
        return options[state] + " "
    else:
        return None

# Globals
BUILTINS = ["exit", "echo", "type", "pwd", "cd"]
CACHED_COMMANDS = get_all_executables(BUILTINS)
# Register the tab-completion function
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def main():
    #builtIns = ["exit", "echo", "type", "pwd", "cd"]
    while (True):
        command = input("$ ").strip()
        func = parseCommand(command)[0]
        args = parseCommand(command)[1:]
        match(func):
            case "exit":
                sys.exit()
                continue
            case "echo":
                if isRedirectionOrAppend(args):
                    handleRedirect(func, args)
                else:
                    print(" ".join(args))
                continue
            case "type":
                args = command[4:].strip()
                if args in BUILTINS:
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
                    if isRedirectionOrAppend(args):
                        handleRedirect(func,args)
                    else:
                        executeProgram(func, args)
                else:
                    print(f"{command}: not found")
                continue


if __name__ == "__main__":
    main()
