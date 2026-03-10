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

def getAllDirectoryExecutables(path_input):
    execs = set()
    
    # Handle the special "PATH" case or a specific directory
    search_paths = []
    if path_input == "PATH":
        search_paths = os.environ.get('PATH', '').split(os.pathsep)
    else:
        search_paths = [path_input]

    for directory in search_paths:
        if not os.path.isdir(directory):
            continue
        try:
            for filename in os.listdir(directory):
                full_path = os.path.join(directory, filename)
                # Ensure it's a file and we have execute permissions
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    execs.add(filename)
        except (PermissionError, FileNotFoundError):
            continue

    return list(execs)

def getAllCompleterFileOptions():

    path_execs = set(getAllDirectoryExecutables("PATH"))
    cwd_execs = set(getAllDirectoryExecutables(os.getcwd()))
    
    # Merging all sets into one
    combined = path_execs | cwd_execs
    return sorted(list(combined))

def get_path_commands():
    """Helper to find all executable names in the system PATH."""
    commands = set()
    path_str = os.environ.get('PATH', '')
    for directory in path_str.split(os.pathsep):
        if not os.path.isdir(directory):
            continue
        try:
            for filename in os.listdir(directory):
                full_path = os.path.join(directory, filename)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    commands.add(filename)
        except (PermissionError, FileNotFoundError):
            continue
    return commands

def completer(text, state):
    buffer = readline.get_line_buffer()
    
    # 1. COMMAND COMPLETION (First word)
    if " " not in buffer.lstrip():
        path_cmds = get_path_commands()
        all_options = sorted(list(set(BUILTINS) | path_cmds))
        options = [cmd for cmd in all_options if cmd.startswith(text)]
        # Commands always get a trailing space
        suffix = " "
    
    # 2. FILENAME & DIRECTORY COMPLETION
    else:
        options = []
        try:
            # Handle Nested Paths
            if "/" in text:
                dirname = os.path.dirname(text)
                prefix = os.path.basename(text)
                search_dir = dirname if dirname else "/"
                
                if os.path.isdir(search_dir):
                    for f in os.listdir(search_dir):
                        if f.startswith(prefix):
                            options.append(os.path.join(dirname, f))
            else:
                # Current Directory
                cwd = os.getcwd()
                options = [f for f in os.listdir(cwd) if f.startswith(text)]
            
            options.sort()
        except Exception:
            return None

    # 3. SELECT MATCH AND APPLY SUFFIX
    if state < len(options):
        match = options[state]
        
        # If we are in the 'arguments' section (not a command)
        if " " in buffer.lstrip():
            # Check if the match is a directory
            if os.path.isdir(match):
                return match + "/"  # Brief: "Append a trailing / with no space"
            else:
                return match + " "  # Brief: "Complete it and add a trailing space"
        
        return match + " " # Default for commands
        
    return None

# Globals
BUILTINS = ["exit", "echo", "type", "pwd", "cd"]
# Register the tab-completion function
readline.set_completer(completer)
readline.set_completer_delims(' \t\n;')
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
