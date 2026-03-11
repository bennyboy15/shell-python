# Custom Python Shell

A functional command-line interface built from scratch using Python. This project implements core shell mechanics, including process management, command parsing, and I/O redirection.

---

## Motivation

The primary goal of this project was to dive deep into **systems programming** and understand how operating systems bridge the gap between user input and hardware execution. By building this shell, I explored:

* **Process Lifecycle:** Implementing the `fork/exec` model to manage child processes.
* **System Calls:** Interfacing directly with OS-level functions for navigation and file handling.
* **Data Parsing:** Building a robust parser to handle arguments, flags, and special characters.
* **I/O Management:** Learning how file descriptors work by implementing standard output (`>`) and standard error (`2>`) redirection.

---

## Quick Start

## Prerequisites
* **Python 3.8+**
* Made with OS specific differences in mind but created on Windows.

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/bennyboy15/shell-python.git
   cd shell-python
   python app/main.py

## Usage
```
$ pwd
/home/user/projects
$ls -la > manifest.txt$ cat manifest.txt | grep ".py"
```

## Contributing
Contributions are welcome! If you'd like to add features like tab-completion, environment variable support, or background jobs:

Fork the repository.

Create a Feature Branch (```git checkout -b feature/AmazingFeature```).

Commit your Changes (```git commit -m 'Add some AmazingFeature'```).

Push to the Branch (```git push origin feature/AmazingFeature```).

Open a Pull Request.
