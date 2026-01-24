# About Make
- Make is the earliest and most popular automation tools used for building software.
- Created by Stuart Feldman while he was in the Bell Labs. An early version was completed in 1976.
- make uses a configuration file called as makefile to define what .c files are needed and which dependendcies exist between them
```txt 
my_project/
├─ Makefile
├─ src/
├─ include/
```

---
# Make tutorial
```makefile
#Includes
include config.mk #just the same make syntax(has a lot of variables and compilation stuff, easy to manage)
#platform specific include
ifeq ($(OS),Windows_NT)
  include windows.mk
else
  include unix.mk
endif


#automatic variables 
$@   # target name
$<   # first dependency
$^   # all dependencies

#Conditionals
ifeq ($(OS),Windows_NT)
  CC = cl
else
  CC = gcc
endif

CC = gcc
CFLAGS = -Wall -Wextra
all: name

name: file.c 
    $(CC) $(CFLAGS) gcc file.c -o file

na: test.c 
    $(CC) $(CFLAGS) gcc -c test.c -o test.o

#pattern rule
%.o: %.c
	$(CC) -c $< -o $@
# implicit rule 
%.o: %.c

file: file.c
	$(CC) -o $@ $<


clean: 
    rm file.c test.c

#phony target
.PHONY: all clean

#
=   # lazy
:=  # immediate
?=  # default
+=  # append

#Functions
$(wildcard *.c)
$(patsubst %.c,%.o,$(SRC))

#Recursive Make
cd subdir && $(MAKE)
```

```zsh
make hello    #for the hello alone
make          #does the all: function
make clean    #processes the clean function
make -j4      #parallel build
make CC=clang #environment interaction
```

>[!NOTE]  Note
> Never ship dependencies, document it and let the user downlowd the dependencies.

--- 

# About Cmake
-  Cmake can be used to make Makefiles and as project increase the make file also increases.
-  complexity increase while using make if your trying to ship the project cross platform
- cmake is used for creating cross platform projects and also automate compiling.

- Cmake uses a file called CMakeLists.txt
- you run cmake to make makefile
- you build your project using make
- add fixes and more code then run make, and goes on.

```txt 
my_project/
├─ CMakeLists.txt   ← REQUIRED (root)
├─ src/
├─ include/
├─ tests/
└─ README.md

#cmake after result
my_project/
├─ CMakeLists.txt
├─ src/
├─ build/           ← generated
    └─ Makefile      ← generated
```

---
# CMake Tutorial
```cmake
cmake_minimum_required(VERSION 4.2.1)
project(myproject)               # general project name is myproject
add_executable(myprogram main.cpp) #program name is myprogram & file is main.cpp
find_package(fmt)

set() #set is used for setting variables for compiling or other purposes
set(CMAKE_CXX_STANDARD 23) #set the compiler version
set(CMAKE_CXX_STANDARD_REQUIRED YES)#YES = must be 23 #NO = if 23 isn't present uses previous versions
set(CMAKE_CXX_EXTENSIONS OFF)# use particular extensions of a compiler

add_library(mylib lib.cpp)     # creates a library (static library by default)
add_library(graph STATIC libgraph.cpp) #creates a static library called graph

add_library(calc SHARED libcalc.cpp) #creates a dynamic library called libcalc.(dll/so/dylib)
target_link_libraries(${PROJECT_NAME} calc fmt::fmt) 
# if you don't know the name for calling the library search it in internet for cmake calling it in cmake

#connects the dynamic library to the executable
#note that ${PROJECT_NAME} is the executable name, call your executable name accordingly

#NOTE: to call the dynamic library you should as always call the function normaly in you program 
#      and then create a header file(.hpp/.h) that calls the function you created as a library and call it in the 
#      library you created "header.h" (in both libcalc.cpp & main.cpp in this case) to refer at first place.

add_subdirectory(lib)
#inside lib directory create a CMakeLists.txt and add those above lines you used to creat the library
add_library(calc SHARED libcalc.cpp) 
add_library(graph STATIC libgraph.cpp) 
target_include_directories(graph INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})  #other words are PUBLIC and PRIVATE
# PUBLIC is when other executables require your program but it doesn't no the header file 
# private is when everything is done in the same directory and other programs don't need it.
# interface is only for the programs that knows the headers 

#variables
${PROJECT_NAME} is a variable
add_executable(${PROJECT_NAME} main.cpp) #uses project name as the output
```

```bash
mkdir build
cd build
cmake ..
make
```

---
