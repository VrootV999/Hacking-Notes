# 🐚 Bash Scripting — Red Team Edition

## Basics of a Bash Script

```bash
#!/bin/bash
# This is a comment
echo "Hello Red Team"
```

- Shebang (#!/bin/bash): tells system which interpreter to use.
- Comments (#): ignored by Bash; useful for notes or disabling code.
- Commands: exactly as typed in terminal.
--- 

## Running a Script

```bash
chmod +x script.sh    # Make executable
./script.sh           # Run from current directory
bash script.sh        # Run explicitly with bash
```
--- 

## Variables

```bash
name="Operator"
echo "Hello $name"
#No spaces around =.
#Access variables with $variable
```
--- 

## Reading Input
```bash
read -p "Enter target IP: " target
echo "Pinging $target"
```
--- 

## Arguments
```bash
#!/bin/bash
echo "First arg: $1"
echo "Second arg: $2"
echo "All args: $@"
```

- `$1`, `$2` → first and second arguments.
- `$@` → all arguments.
--- 

## Conditionals

```bash
if [ "$user" == "root" ]; then
    echo "We have root privileges!"
else
    echo "Standard user detected."
fi
```

- String operators: ==, !=, -z (empty)
- Number operators: -eq, -ne, -gt, -lt
- File operators: -f (file exists), -d (directory), -x (executable)
--- 

## Loops

### For-Loop
```bash 
for ip in {1..5}; do
    echo "Pinging 192.168.1.$ip"
done
```

### While-Loop
```bash 
count=1
while [ $count -le 5 ]; do
    echo "Try $count"
    ((count++))
done
```

### do-while loop

```bash
doStuff(){
  // first "iteration" here
}
doStuff
while [condition]; do
  doStuff
done
```
--- 

## Function
```bash
recon() {
    echo "Scanning $1..."
    nmap -sV $1
}
recon 192.168.1.1
```
--- 

## Useful Operators
- Command substitution: output=$(command)
- Redirection:
    - `>` overwrite file
    - `>>` append
    - `2>` errors

- Pipes (|): send output from one command to another
--- 

## Tricks
```bash
bash -x script.sh   # Debug mode
set -e              # Exit on error
set -u              # Exit if using undefined var
set -o pipefail     # Catch errors in pipelines
```
--- 

## Security Consideration
- Always quote variables: "${var}" to prevent word splitting.
- Avoid storing plaintext creds in scripts — use environment variables or prompt for them.
- Use explicit interpreter (#!/bin/bash) for consistency.
- Clean up traces — logs, temp files, history.
--- 

## Array

### Indexed Arrays
```bash
ports=(22 80 443)
echo "First port: ${ports[0]}"
```

### Looping through arrays
```bash
for port in "${ports[@]}"; do
    echo "Scanning port $port"
done
```

### Associative array
```bash 
declare -A targets
targets=( ["web"]="192.168.1.10" ["db"]="192.168.1.20" )
echo "DB IP: ${targets[db]}"
```
--- 

## Pattern Matching & Globbing
- Wildcards:
    `*` → match any length

    `?` → match single char

    `[abc]` → match one char from set

- Extended globbing:
    ```bash 
    shopt -s extglob
    ls !(*.txt)  # list files not ending with .txt
    ```
--- 

## String Manipulation
```bash 
var="192.168.1.1"
echo "${var:0:7}"       # substring
echo "${var//192/10}"   # replace
echo "${var%%.*}"       # remove after first dot
```
--- 

## Exit Codes & Conditional Execution
- `$?` → exit status of last command (0 success, non-zero fail)

- `cmd1 && cmd2` → run cmd2 if cmd1 succeeds

- `cmd1 || cmd2` → run cmd2 if cmd1 fails
--- 

## Here-Document
```bash 
cat <<EOF
Multi-line text
Goes here
EOF
```
--- 

## Here-string
```bash 
cat <<< "Single line input"
```
--- 

## Subshells and Grouping
```bash 
#( ... ) → runs commands in a subshell
#{ ...; } → runs commands in current shell
(cd /tmp && ls)   # directory change only inside subshell
```
--- 

## envp
```bash 
export API_KEY="secret"
```
--- 

## Trap Signals & Cleanup

```bash 
trap 'echo "Cleaning up..."; rm -f /tmp/tmpfile' EXIT
```

--- 
## Command-Line Option Parsing
```bash 
while getopts "u:p:" opt; do
  case $opt in
    u) user=$OPTARG ;;
    p) pass=$OPTARG ;;
  esac
done
```
- Makes scripts behave like professional CLI tools. 

- Process Control
    - & → run in background
    - jobs → list background jobs
    - fg / bg → bring jobs foreground/background
    - wait → wait for background process to finish
--- 
## Shell Options (shopt)
```bash 
shopt -s nullglob   # avoid errors if no matches
shopt -s nocaseglob # case-insensitive globbing
```
--- 

## The Expansion Order
When you type a command, Bash processes it in roughly this order:

1. **Brace expansion**
2. **Tilde expansion**
3. **Parameter & variable expansion**
4. **Command substitution**
5. **Arithmetic expansion**
6. **Word splitting**
7. **Pathname expansion** (globbing)

Then the command is finally executed.

### 1. Brace Expansion
- Happens **first** — before variables are even expanded.
- Generates strings from patterns.
    ```bash
    echo {A,B,C}        # A B C
    echo {1..5}         # 1 2 3 4 5
    ```
- Useful for generating payload variations:
    ```bash 
    scp file{1..10}.txt target:/tmp/
    ```

### 2. Tilde Expansion
- Expands ~ to the home directory.
```bash 
cd ~               # /home/user
cd ~root           # /root
```

### 3. Parameter & Variable Expansion

- `${var}`, `$var`, `${var:-default}`, `${var:=default}`
```bash 
user="root"
echo "User is ${user}"
```
Modifiers:
    `${var#pattern}` → remove shortest match from start
    `${var##pattern}` → remove longest match from start
    `${var%pattern}` → remove shortest match from end
    `${var%%pattern}` → remove longest match from end

### 4. Command Substitution
- Runs a command, replaces it with its output.
```bash 
today=$(date)
echo "Today is $today"
```
- Preferred: $(command) over backticks `command` for nesting. 

### 5. Arithmetic Expansion
- $((expression))
```bash 
x=5
echo $((x + 3))   # 8
```
- Supports bitwise ops — useful for binary manipulation.

### 6. Word Splitting
- After expansions, Bash splits text into words on $IFS (Internal Field Separator).
    ```bash 
    list="one two three"
    for i in $list; do echo "$i"; done
    ```
- To avoid unintended splitting:
    ```bash 
    for i in "$list"; do echo "$i"; done   # single item
    ```

### 7. Pathname Expansion (Globbing)
- Matches files based on wildcards.
    ```bash 
    ls *.txt
    ```
- Wildcards:
    `*` → zero or more chars
    `?` → single char
    `[abc]` → set of chars
- Extended globbing:
    ```bash 
    shopt -s extglob
    ls !(*.txt)
    ```
--- 

## Quoting Rules
Quoting changes how expansions occur:
- Single quotes ' → literal, no expansion at all.
    ```bash 
    echo '$USER'   # $User
    ```
- Double quotes " → expands variables and commands, but disables globbing & splitting (except $@ special behavior).
    ```bash
    echo "$USER"   # expands
    #Backslash \ → escapes a single character.
    #ANSI-C quoting $'string' → supports escape sequences.
    echo $'\x41'   # A
    ```
--- 

## Impact of set -f (Disable Globbing)
```bash 
set -f   # disable pathname expansion
files="*"
echo $files  # prints literal *
```
- Useful when handling user-supplied input safely.

## Special Variables in Parsing
- $* vs $@ inside double quotes:
    - "$*" → all args as one string
    - "$@" → each arg as separate word
```bash 
for arg in "$@"; do echo "$arg"; done
```
