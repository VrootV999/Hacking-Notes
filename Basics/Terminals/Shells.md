> You'll learn everything to do in linux

  

> [!important]  
> We will learn zsh and bash together We'll only focus on main and common commands  

  

Linux has a command line know as a shell where all the magic happens and in this shell we can do whatever you want and you have the full control of the device in your terminal.

  

This can be used in Mac-os or in Linux and Unix

  

# <span style="color:rgb(22, 177, 208)">Basics</span>

  

### <span style="color:rgb(146, 208, 80)">Get to a directory</span>

  

Go to a specific directory

```Shell
cd /path/to/your/directory
```

  

Go back

```Shell
cd ..
```

Go way back

```Shell
cd ../.. \#how much ever you want
```

## <span style="color:rgb(151, 71, 17)">List files</span>

```Shell
ls 
# -l for long
# -a for hiden file
```

  

## <span style="color:rgb(237, 7, 7)">Where am I?</span>

```Shell
pwd
```

  

## <span style="color:rgb(0, 176, 80)">Who am I?</span>

```Shell
whoami
```

  

## <span style="color:rgb(255, 255, 0)">Help i’m stuck!!</span>

```Shell
<application> --help
         or 
<application> -h
         or 
<application> -?

#replace application with yours
```

## <span style="color:rgb(112, 48, 160)">Read the Manuel</span>

```Shell
man <application>

#replace application with yours
```

  

## <span style="color:rgb(241, 156, 9)">Find what you want</span>

```Shell
locate <smth> #evth but late update of the directorys
whereis <smth> #finds binary file with binary on its location
which <smth>   #finds binary file and only returns the path

find <directory> <options> <expression>
options 
       -type file type
expression
       -name 
```

  

## <span style="color:rgb(15, 53, 204)">What is happening?</span>

```Shell
ps #processes

# a for all users
# u for detailed information 
# x for process without control terminal
```

  

## <span style="color:rgb(196, 18, 163)">Filter</span>

```Shell
| grep <smth>

# <smth> could be a process or file anything
```

  

## <span style="color:rgb(22, 177, 208)">MEOW</span>

```Shell
cat file.txt
cat > file.txt
cat >> file.txt

> interactive mode
```

  

## <span style="color:rgb(146, 208, 80)">I wanna touch you….. not that way</span>

```Shell
touch file.txt 

makes that file
```

  

## <span style="color:rgb(151, 71, 17)">Make directory</span>

```Shell
mkdir test_folder
```

## <span style="color:rgb(237, 7, 7)">Copy</span>

```Shell
cp file.txt /where/to
cp * /where/to
cp file.txt file2.txt /where/to
```

  

## <span style="color:rgb(0, 176, 80)">Move</span>

```Shell
mv file.txt /where/to
mv * /where/to
mv file.txt file2.txt /where/to
```

  

## <span style="color:rgb(255, 255, 0)">Remove</span>

```Shell
rm file.txt
rm -rf folder
rm file.txt file2.txt
rm -rf folder folder2
```

