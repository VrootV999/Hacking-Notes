
# Basics

### Operators
- Arithmetic
	1.  Addition               +
	2. Subtraction           -
	3. Multiplication        *
	4. Division                 //
	5. Floor Division       %
	6. power                    **
-  Comparison
     1. compare and equal              ==
     2. not equal                               !=
     3. greater than                           >
     4. lesser than                             <
     5. greater than or equal to       >=
     6. lesser than or equal to         <=
- Logical
      1. and
      2. or 
      3. not
- Assignment
      1.  equal to                        =
      2. add with                     +=
      3. subtract with              -= 
      4. multiply with               * =
      5. divide with                  /=
      6. modulus with              %=                    (get last digit)
      7. Divide with                  //=                     (remove last digit)
- Bitwise
     1. and                  &
     2. or                     |
     3. XOR                 ^
     4. not                   ~
     5. left shit           <<
     6. right shift        >>
- Membership
     1. in 
     2. not in
- Identity
     1. is
     2. not is   


### Control Structure
- condition 
     1. if
     2. elif
     3. else
     4. 
- Loop
     1. for
     2. while
- Loop control
     1. break
     2. continue
     3. pass



### Variable
- integer                     int()
- floating-point          float()
- boolean                   True   False
- string                       []
- dictionary                {"key":"value"}
- set                           {}
- tuple                        ()



### Extras
- Exception handling        try,except,else,finally
-  Input                              input
- output                             output
- Comment                        #    ''' '''

# Functions to use
### FOR STRING

- **capitalize()**          Converts the first character to upper case
- **casefold()**            Converts string into lower case
- **center()**                Returns a centered string
- **count()**                  Returns the number of times a specified value occurs in a string
- **encode()**               Returns an encoded version of the string
- **endswith()**            Returns true if the string ends with the specified value
- **expandtabs()**        Sets the tab size of the string
- **find()**                      Searches the string for a specified value and returns the position of 
                - where it was found
- **format()**                   Formats specified values in a string
- **format_map()**         Formats specified values in a string
- **index()**                    Searches the string for a specified value and returns the position of 
                - where it was found
- **isalnum()**                Returns True if all characters in the string are alphanumeric
- **isalpha()**                 Returns True if all characters in the string are in the alphabet
- **isascii()**                   Returns True if all characters in the string are ASCII characters
- **isdecimal()**             Returns True if all characters in the string are decimals
- **isdigit()**                   Returns True if all characters in the string are digits
- **isidentifier()**           Returns True if the string is an identifier
- **islower()**                 Returns True if all characters in the string are lower case
- **isnumeric()**            Returns True if all characters in the string are numeric
- **isprintable()**           Returns True if all characters in the string are printable
- **isspace()**                Returns True if all characters in the string are whitespaces
- **istitle()**                    Returns True if the string follows the rules of a title
- **isupper()**                Returns True if all characters in the string are upper case
- **join()**                       Converts the elements of an iterable into a string
- **ljust()**                       Returns a left justified version of the string
- **lower()**                    Converts a string into lower case
- **lstrip()**                     Returns a left trim version of the string
- **maketrans()**            Returns a translation table to be used in translations
- **partition()**                Returns a tuple where the string is parted into three parts
- **replace()**                 Returns a string where a specified value is replaced with a specified                                    value
- **rfind()**                       Searches the string for a specified value and returns the last                                                position of where it was found
- **rindex()**                    Searches the string for a specified value and returns the last                                                position of where it was found
- **rjust()**                         Returns a right justified version of the string
- **rpartition()**                 Returns a tuple where the string is parted into three parts
- **rsplit()**                        Splits the string at the specified separator, and returns a list
- **rstrip()**                        Returns a right trim version of the string
- **split()**                          Splits the string at the specified separator, and returns a list
- **splitlines()**                  Splits the string at line breaks and returns a list
- **startswith()**                Returns true if the string starts with the specified value
- **strip()**                          Returns a trimmed version of the string
- **swapcase()**                Swaps cases, lower case becomes upper case and vice versa
- **title()**                           Converts the first character of each word to upper case
- **translate()**                   Returns a translated string
- **upper()**                        Converts a string into upper case
- **zfill()**                            Fills the string with a specified number of 0 values at the beginning
## FOR DICTIONARY
- **clear()**                         Removes all the elements from the dictionary  
- **copy()**                         Returns a copy of the dictionary  
- **fromkeys()**                 Returns a dictionary with the specified keys and value  
- **get()**                           Returns the value of the specified key  
- **items()**                       Returns a list containing a tuple for each key-value pair  
- **keys()**                        Returns a list containing the dictionary's keys  
- **pop()**                         Removes the element with the specified key  
- **popitem()**                 Removes the last inserted key-value pair  
- **setdefault()**              Returns the value of the specified key. If the key does not                                                    exist,inserts the key with the specified value  
- **update()**                   Updates the dictionary with the specified key-value pairs  
- **values()**                    Returns a list of all the values in the dictionary
## Built In Function
- **abs()**                        Returns the absolute value of a number  
- **all()**                          Returns True if all items in an iterable object are true  
- **any()**                        Returns True if any item in an iterable object is true  
- **ascii()**                      Returns a readable version of an object. Replaces non-ASCII                                               characters with escape characters  
- **bin()**                        Returns the binary version of a number  
- **bool()**                      Returns the boolean value of the specified object  
- **bytearray()**             Returns an array of bytes  
- **bytes()**                    Returns a bytes object  
- **callable()**                Returns True if the specified object is callable, otherwise False  
- **chr()**                       Returns a character from the specified Unicode code  
- **classmethod()**       Converts a method into a class method  
- **compile()**               Returns the specified source as an object, ready to be executed  
- **complex()**              Returns a complex number  
- **delattr()**                 Deletes the specified attribute (property or method) from the                                              specified object  
- **dict()**                      Returns a dictionary (Array)  
- **dir()**                        Returns a list of the specified object's properties and methods  
- **divmod()**               Returns the quotient and the remainder when argument1 is divided by                               argument2  
- **enumerate()**         Takes a collection (e.g., a tuple) and returns it as an enumerate object  
- **eval()**                     Evaluates and executes an expression  
- **exec()**                    Executes the specified code (or object)  
- **filter()**                    Use a filter function to exclude items in an iterable object  
- **float()**                    Returns a floating-point number  
- **format()**                 Formats a specified value  
- **frozenset()**            Returns a frozenset object  
- **getattr()**                Returns the value of the specified attribute (property or method)  
- **globals()**                Returns the current global symbol table as a dictionary  
- **hasattr()**                Returns True if the specified object has the specified attribute                                             (property/method)  
- **hash()**                    Returns the hash value of a specified object  
- **help()**                     Executes the built-in help system  
- **hex()**                      Converts a number into a hexadecimal value  
- **id()**                         Returns the id of an object  
- **input()**                   Allows user input  
- **int()**                       Returns an integer number  
- **isinstance()**          Returns True if a specified object is an instance of a specified object  
- **issubclass()**          Returns True if a specified class is a subclass of a specified object  
- **iter()**                      Returns an iterator object  
- **len()**                      Returns the length of an object  
- **list()**                      Returns a list  
- **locals()**                 Returns an updated dictionary of the current local symbol table  
- **map()**                    Returns the specified iterator with the specified function applied to                                     each item  
- **max()**                    Returns the largest item in an iterable  
- **memoryview()**     Returns a memory view object  
- **min()**                     Returns the smallest item in an iterable  
- **next()**                   Returns the next item in an iterable  
- **object()**                Returns a new object  
- **oct()**                     Converts a number into an octal  
- **open()**                  Opens a file and returns a file object  
- **ord()**                     Converts an integer representing the Unicode of the specified                                             Character  
- **pow()**                   Returns the value of x to the power of y  
- **print()**                   Prints to the standard output device  
- **property()**            Gets, sets, deletes a property  
- **range()**                 Returns a sequence of numbers, starting from 0 and increments by 1                                  (by default)  
- **repr()**                    Returns a readable version of an object  
- **reversed()**           Returns a reversed iterator  
- **round()**                Rounds a number  
- **set()**                     Returns a new set object  
- **setattr()**              Sets an attribute (property/method) of an object  
- **slice()**                  Returns a slice object  
- **sorted()**               Returns a sorted list  
- **staticmethod()**    Converts a method into a static method  
- **str()**                       Returns a string object  
- **sum()**                    Sums the items of an iterator  
- **super()**                 Returns an object that represents the parent class  
- **tuple()**                  Returns a tuple  
- **type()**                   Returns the type of an object  
- **vars()**                    Returns the `__dict__` property of an object  
- **zip()**                       Returns an iterator, from two or more iterators

## For Tuple
- **count()**      Returns the number of times a specified value occurs in a tuple
- **index()**      Searches the tuple for a specified value and returns the position of where it                       was found
## For Set
- **add()**                                            Adds an element to the set
- **clear()**                                           Removes all the elements from the set
- **copy()**                                           Returns a copy of the set
- **difference()**                                  Returns a set containing the difference between two or                                                        more sets
- **difference_update()**                    Removes the items in this set that are also included in                                                           another, specified set
- **discard**                                          Removes the specified item
- **intersection()**                                Returns a set, that is the intersection of two other sets
- **intersection_update()**                  Removes the items in this set that are not present in                                                             other, specified set(s)
- **isdisjoint()**                                    Returns whether two sets have an intersection or not
- **issubset()**                                     Returns whether another set contains this set or not
- **issuperset()**                                  Returns whether this set contains another set or not
- **pop()**                                             Removes an element from the set
- **remove()**                                       Removes the specified element
- **symmetric_difference()**                Returns a set with the symmetric differences of two                                                              sets
- **symmetric_difference_update()**   Inserts the symmetric differences from this set and                                                               another
- **union()**                                            Returns a set containing the union of sets
- **update()**                                         Updates the set with the union of this set and others

## For File
- **close()**                        Closes the file
- **detach()**                     Returns the separated raw stream from the buffer
- **fileno()**                        Returns a number that represents the stream, from the operating                                        system's perspective
- **flush()**                         Flushes the internal buffer
- **isatty()**                        Returns whether the file stream is interactive or not
- **read()**                          Returns the file content
- **readable()**                   Returns whether the file stream can be read or not
- **readline()**                    Returns one line from the file
- **readlines()**                  Returns a list of lines from the file
- **seek()**                         Changes the file position
- **seekable()**                 Returns whether the file allows us to change the file position
- **tell()**                           Returns the current file position
- **truncate()**                  Resizes the file to a specified size
- **writable()**                   Returns whether the file can be written to or not
- **write()**                        Writes the specified string to the file
- **writelines()**                 Writes a list of strings to the file

## For Array
- **append()**             Adds an element at the end of the list
- **clear()**                  Removes all the elements from the list
- **copy()**                  Returns a copy of the list
- **count()**                Returns the number of elements with the specified value
- **extend()**              Adds the elements of a list (or any iterable) to the end of the current                                   list
- **index()**                Returns the index of the first element with the specified value
- **insert()**                Adds an element at the specified position
- **pop()**                   Removes the element at the specified position
- **remove()**             Removes the first item with the specified value
- **reverse()**             Reverses the order of the list
- **sort()**                   Sorts the list

## Maths
- abs(10.23024)
- max(10,240,425,1000)
- min(1023,1421024,124,1)
- round(10.4124015)

## Import Math
- math.ceil(130.1424)
- math.pow(x,y)
- math.floor(2139.1203)
- math.sqrt(100)


## Import Keyword
- keyword.iskeyword()
- keyword.kwlist

# For Loop
`for variable in iterable

remember for loop you already have a identifier variable (pointer variable)

ex:
```python
for i in range(1,10):
	for j in range(1,10):
		print(i "*" j "=" "i*J")
	print('/n')
```

this show the multiplaction tables like that

lets see how For loop works in making patterns for better understanding

```python
r = int(input("Enter the number of rows: "))
c = int(input("Enter the number of columns: "))
for i in range(1,r+1):     (if r = 5, 1,2,3,4,5)
	for j in range(1,i+1):     (from outer loop one number enters ex: 1 so range(1,2))
		print(j)        (so 1 is printed and next outer loop executed and onemore cycle)
	print('/n')


''' output'''

Enter the number of rows: 5
Enter the number of columns: 5

1
12
123
1234
12345
```


But what if i just change the print(j) to print(i)

output
1
22
333
4444
55555


outer for loop:
	inner for loop:     
one time outer loop then inner one the outer until outer gets over.



# While loop

while loop requires a outside indicator due to the fact that it works with conditions

WHILE (CONDITION)

```python
i = 0              (pointer variable)
n = 5
while i < 5:
	j = 1
	while j < i:
		print(i "*" j "=" i*j)
	print('/n')
```

the above for loop multiplication is written in while loop 

next we'll see how nested loop works

```python
i = 0
r = int(input("Enter the number of rows: "))
c = int(input("Enter the number of columns: "))

while i <= r:
	j = i
	while j <= c:
		print(j)
		j += 1
	print('/n')
	i += 1
```

since we are assigning the pointer variable we need to exit from it manually so we need to do appropriate action such as increment, decrement , removal of digits in places or whatever is good for that scenario.
Otherwise you are going to fuck up your code with a infinite loop.

// = 10      (removes last digit in the given number of yours)
a %10 =    (get the last digit as a variable)


# Exception Handling

this is one way to handle errors in python and can be used to make the program run smoothly without errors which is good for looking better.
#### try 
- used to try a block of code as for a certain error capturing
#### except 
- this thing takes the error mentioned in the except syntax and if it catches a error mentioned by the programmer then it executes certain thing said by the programer
#### finally 
- this is used to wrap up something as like closing the opened/used file or simply to execute something in the end.
#### else
- if anything none of the error is found or didn't catch any such error this false statement will be executed after that.

```python
try:
	n = int(input("Enter your first number for division: "))
	d = int(input("Enter your second number for division"))
	div = n // d
	print("Your answer: /n/n/n", div)
except ZeroDivisionError:
	print("Are u f'king retard, huh??)
except ValueError:
	print("Well it can be seen that you can't f'king read")
except Exceptions:
	print("Well Well we have a retard who can't read and understand")
else:
	print("this is the second soultion")
finally:
	print("This is printed in the end")
```

or with a while loop to get users input again instead of exiting:

```python
while True:
	try:
		n = int(input("Enter your first number for division: "))
		d = int(input("Enter your second number for division"))
		div = n // d
		print("Your answer: /n/n/n", div)
	except ZeroDivisionError:
		print("Are u f'king retard, huh??)
	except ValueError:
		print("Well it can be seen that you can't f'king read")
	except Exceptions:
		print("Well Well we have a retard who can't read and understand")
	else:
		print("this is the second soultion")
	finally:
		print("This is printed in the end")
```

if any file is opened we can do this.......

# File Management

#### Open a File
```python
file = open('filename.txt', 'r')      # Read mode
file = open('filename.txt', 'w')      # Write mode
file = open('filename.txt', 'a')      # Append mode
file = open('filename.txt', 'rb')     # Read binary mode
file = open('filename.txt', 'wb')     # Write binary mode
```
#### File Modes
- `'r'` : Read (default mode, file must exist)
- `'w'` : Write (creates a new file or truncates an existing file)
- `'a'` : Append (creates a new file or appends to an existing one)
- `'rb'` : Read in binary mode
- `'wb'` : Write in binary mode
- `'r+'` : Read and write
- `'w+'` : Write and read (creates a new file or truncates)
- `'a+'` : Append and read (creates a new file or appends)
#### Reading Files
- content = file.read()            READS ENTIRE FILE
- line = file.readline()             READS ONE LINE FROM THE FILE
- lines = file.readlines()          READS ALL THE LINES IN A LIST
- if file.readable():
     content = file.read()    CHECKING READABILITY

#### Writing Files
- file.write("Hello, world!")     WRITES A LINE IN A FILE
- lines = ["Line 1", "Line 2"]
  file.writelines(lines)             WRITES A LIST OF STRINGS TO A FILE
- if file.writable():
    file.write("This will be written to the file.")   CHECKS IF A FILE IS CAN BE WRITTEN TO

#### File Position and Size
- file.seek(0)                          Moves to the beginning of the file
- position = file.tell()             Returns the current file pointer position.
- file.seek(0, 2)                     Move to the end of the file                                                         file_size = file.tell()

#### File Close 
- file.close()                         Close a file
- file.flush()                          Ensure data is written to disk
#### File Truncation 
- file.truncate(10)               Reduces the file size to 10 bytes

#### File Handling Content Manager
```python
with open('filename.txt', 'r') as file:
    content = file.read()

Opens the File
```
#### File Attributes and Properties
 
- file_descriptor = file.fileno()                Returns the file descriptor for the file.
- if file.isatty():
    print("This file is interactive.")          Checks if the file is associated with a terminal.
- raw_stream = file.detach()                Separates the raw stream from the buffer (useful for                                                             binary files).
- if file.seekable():
    print("File pointer can be moved.")  Checks if the file supports seeking (i.e., moving the                                                             file pointer).
- difference():                                       Returns a set containing the difference between two                                                             sets (typically used for set operations but can be                                                                   applied to files in cases).
- differnece_update():                        Removes elements from the current set that are also                                                           present in another set.
  
#### File Error Handling 
```python
try:
    with open('nonexistentfile.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except IOError:
    print("An error occurred while handling the file!")
```
