
# Main 
- Main is where you can make shit and run shit inside it.
- basically a place where everything happens kinda like a hall in a house.
```
int main(){
	return 0;
};
// this is where we run stuff.
```
# Return 0?
- return zero is to ensure that the code works otherwise the code will return value of 1.
# Input and Output
- Input and output in C++ can be taken only with this module
  `# include <iostream>`
# Operators
## Arithmetic
Just like python no diffrence
## Comparison
just like python no difference

## Logical
- && and
- || or
- !  not
# String
-  `#include <string>`
```
//without using
std::string test = "test string";

// with using
using std::string;
//with typedef
typedef std::string string;
```
## Concatination 
```
# include <string>
typedef std::string string;
int main(){
	string firstName = "John ";  
	string lastName = "Doe";  
	string fullName = firstName + lastName;  
	cout << fullName;
}

int main(){
	string firstName = "John";  
	string lastName = "Doe";  
	string fullName = firstName + " " + lastName;  
	cout << fullName;
}

```

## String Length
- length 
- `string name = "test" 
   `cout << test.length()`
   `cout << test.size()`
## String Access 
- Access Character
- `string test = "test";`
  `cout << test.at(3)`    output t
  
  `cout << test[3]`          output t
## String Size
- sizeof()
- string.sizeof(); 
# Math 
```
cout << min(5, 10);
cout << max(5, 10);


//with math
# include <cmath>
cout << sqrt(64);  
cout << round(2.6);  
cout << log(2);
```
# Booleans 
- true = 1
- false = 0
```
bool isCodingFun = true;  
bool isFishTasty = false;  
cout << isCodingFun;  // Outputs 1 (true)  
cout << isFishTasty;  // Outputs 0 (false)


test booleans

int x = 10;  
int y = 9;  
cout << (x > y);

cout << (10 > 9);
```

# If, else, else if 
- Just like JS 
```
int main(){
	int n1;
	int n2;
	cout << "Enter your 1st number" << '\n';
	cin >> n1;
	cout << "Enter your 2nd number" << '\n';
	cin >> n2;
	if(n1 > n2){
		cout << "n1 is greater than n2" << '\n';
		}
	else if (n1 == n2){
		cout << "n1 and n2 are same";
	}
	else {
		cout << "n2 is greate than n1" << '\n';
	};
	return 0;
};
 
```

# Switch 
- Just like js
```
# include <iostream>
# include <string>
typedef std:string string
using std:cout
using std:cin

int main(){
	int day_of_the_week = 7;
	switch(day_of_the_week){
		case 1:
			cout << "Monday";
			break;
		case 2:
			cout << "Tuesday";
			break;
		case 3:
			cout << "Wednesday";
			break;
		case 4:
			cout << "Thurday";
			break;
		case 5:
			cout << "Friday";
			break;
		case 6:
			cout << "Saturday";
			break;
		case 7:
			cout << "Sunday";
			break;
		default:
			cout << "Not a Day!!!";
	}
}
```

# Enums
- Note for strings you can't use switch case.
- instead you need enums
```
# include <iostream>
# include <string>
typedef std:string string
using std:cout
using std:cin

//we create a enum which can correspond a string to a integer
enum Day = {Monday = 1, Tuesday = 2, Wednesday = 3, Thursday = 4, Friday = 5, Saturday = 6, Sunday = 7, }

int main(){
	Day today = "Sunday"   // The day enum we created becomes its own data type
	switch(today){
		case Monday:
			cout << "Monday";
			break;
		case Tuesday:
			cout << "Tuesday";
			break;
		case Wednesday:
			cout << "Wednesday";
			break;
		case Thursday:
			cout << "Thurday";
			break;
		case Friday:
			cout << "Friday";
			break;
		case Saturday:
			cout << "Saturday";
			break;
		case Sunday:
			cout << "Sunday";
			break;
		default:
			cout << "Not a Day!!!";
	}
}
```

# While loop 
- just like JS
```
int main(){
    while (true){
        string first_name;
    	cout << "Enter your name: " << endl;
    	getline(std::cin, first_name);
    	string second_name;
    	cout << "Enter your next name: " << endl;
    	getline(std::cin, second_name);
    	string full_name = first_name + " " + second_name;
    	cout << "Your Full name is: " << full_name << endl;
    	string Confir;
    	cout << "Are you Sure[y/n]: ";
    	getline(cin, Confir);
    	if(Confir == "YES" || Confir == "Yes" || Confir == "y" || Confir == "Y"){
        	cout << "Welcome " << full_name;
        	break;    
    	}
    	else{
        	cout << "Lets Try that Again." << endl;
        	cout << "\n";
    	}
}
```
# For Loop 
- Just like JS
- for(condition1; condition2; condition3){ code }
- condition1       do it at the start of the loop
- condition2      condition which when satisfies starts a loop
- condition3      done after every time that loop occurs/satisfies
```
int main(){
    for (int i = 1; i <= 5; i++){
        for (int j = 1 ; j <= i; j++) {
           cout << "* ";
        }
        cout << "\n";
    } 
    return 0;
}
```
# Loop Control 
- Controls the loop
- Continue      continues the loop  by skiping it,
- break           breaks the loop
# Arrays 
 - array test[value] = {"only", "the", "the", "given", "Value", "Is", "The", "Limit"}
 - array test[] = {"unlimited", "Values", "Can", "Be", "Given"}
## Array Loop 
```
string cars[5] = {"Volvo", "BMW", "Ford", "Mazda", "Tesla"};  
for (int i = 0; i < 5; i++) {  
  cout << i << " = " << cars[i] << "\n";  
}


// for each loop

int myNumbers[5] = {10, 20, 30, 40, 50};  
  
// Loop through integers  
for (int i : myNumbers) {  
  cout << i << "\n";  
}
```
## Declaration 
```
string cars[5];  
cars[0] = "Volvo";  
cars[1] = "BMW";  
cars[2] = "Ford";  
cars[3] = "Mazda";  
cars[4] = "Tesla";
```
## Vector 
```
// A vector with 3 elements  
vector<string> cars = {"Volvo", "BMW", "Ford"};  
  
// Adding another element to the vector  
cars.push_back("Tesla");
```

## Multi-dimensional Array 
```
string letters[2][4] = {  
  { "A", "B", "C", "D" },  
  { "E", "F", "G", "H" }  
};


string letters[2][2][2] = {  
  {  
    { "A", "B" },  
    { "C", "D" }  
  },  
  {  
    { "E", "F" },  
    { "G", "H" }  
  }  
};
```
# Struct (structure)
- It is a class being reusable
```
struct students{
	string name;
	int age;
	bool enrolled;
};

students student1;
student1.name = "Alex";
studen1.age = 10;
student1.enrolled = true;

//can also make things default using predefined struct

struct students{
	string name;
	int age;
	bool enrolled = true;    /predefined
};
```
# References 
- Refer to smth
  string food = "Pizza";  // food variable  
  string &meal = food;    // reference to food
  cout << meal;
# Memory Address 
- The location of the particular thing in the memory
- string food = "Pizza";  
   cout << &food;
# Pointers 
- a pointer is a Variable that stores a memory address
```
string food = "Pizza";  // A food variable of type string  
string* ptr = &food;    // A pointer variable, with the name ptr, that stores                               the address of food
//ptr is a name or the pointer which has the name ptr
// u can name it anything
// * means a pointer
// so printing ptr would show the ptr directly
//the below both would be same
cout << ptr;
cout << &food;
```
## Change pointer value 
```
string food = "Pizza";  
string* ptr = &food;  

cout << food << "\n";  

cout << &food << "\n";  
  
cout << *ptr << "\n";  
  
*ptr = "Hamburger";          //change in the pointer

cout << *ptr << "\n";  

cout << food << "\n";
```

# Function 
- datatype function_name(parameter){   code  }
- void is something which is known as unknown data type
```
void myFunction() {  
  cout << "I just got executed!";  
}  
  
int main() {  
  myFunction();  
  return 0;  
}

//you can declare it later
void myFunction();  
  
// The main method  
int main() {  
  myFunction();  // **call** the function  
  return 0;  
}  
  
void myFunction() {  
  cout << "I just got executed!";  
}
```
## Patameters and Arguments
- just like a normal function you can give in parameters
```
void sum(int num1, int num2){
	return num1 + num2;
}

int main(){
	sum(5,10);
	return 0;
}
```
## Default 
- default a value in a funciton
```
void sum(int num1, int num2 = 10){
	return num1 + num2;
}

int main(){
	sum(5);
	return 0;
}
```
## Pass by Value  vs Pass by reference 
### Pass by Value 
 - when we provide a value in a main and then pass it by value to a function the function takes a copy of the value so it is not the same value taken as it is to the function. so there is a copy of the value in the function and there is no change in the original values of the variables.
 - to check it you can pass a function and cout within the function then cout the variable in the main. 
 - the cout from the main shows the value not being changed
 - whereas the value in the function is changed bu the original value isn't affected
```
 void swapNums(int x, int y) {
  int z = x;
  x = y;
  y = z;
  cout << x << y;
}

int main() {
  int firstNum = 10;
  int secondNum = 20;

  cout << "Before swap: " << "\n";
  cout << firstNum << secondNum << "\n";

  cout << "After swap: " << "\n"; 
  swapNums(firstNum, secondNum);
  cout << "Main swap worked?" << firstNum << secondNum << "\n"

  return 0;
}

```

### Pass by reference 
- when we provide a reference we are saying the function to use it so there is no duplicate one as the original variable. 
- so when we try to use pass by reference the original value is change completely
- you can try to cout from the main and from the function and still the change made in the function can be seen in the main.
```
void swapNums(int &x, int &y) {
  int z = x;
  x = y;
  y = z;
  cout << x << y;
}

int main() {
  int firstNum = 10;
  int secondNum = 20;

  cout << "Before swap: " << "\n";
  cout << firstNum << secondNum << "\n";

  cout << "After swap: " << "\n"; 
  swapNums(firstNum, secondNum);
  cout << "Main swap worked?" << firstNum << secondNum << "\n"

  return 0;
}

```
## You can put anything in a fucking function 

## Function overload 
- same function with different names but have some shit in common
```
int plusFuncInt(int x, int y) {  
  return x + y;  
}  
  
double plusFuncDouble(double x, double y) {  
  return x + y;  
}  
  
int main() {  
  int myNum1 = plusFuncInt(8, 5);  
  double myNum2 = plusFuncDouble(4.3, 6.26);  
  cout << "Int: " << myNum1 << "\n";  
  cout << "Double: " << myNum2;  
  return 0;  
}
```

## Scope 
### Local Variable
- created inside a function
```
void myFunction() {  
  int x = 5;        //local
  cout << x;  
}  
  
int main() {  
  myFunction();  
  return 0;  
}
```
### Global Variable 
- created outside the function
```
int x = 5;                //global variable
  
void myFunction() {  
  cout << x << "\n";      //can be used inside the function
}  
  
int main() {  
  myFunction();  
  cout << x;              //can be used inside the function
  return 0;  
}
```

## Recursion 
- Calling a function in a variable or use a function as something that you want.
```
int sum(int k) {  
  if (k > 0) {  
    return k + sum(k - 1);  
  } else {  
    return 0;  
  }  
}  
  
int main() {  
  int result = sum(10);    //you used sum to add the number and save it in result
  cout << result;  
  return 0;  
}
```
# OOP 
Class and then objects inside a class.
ykyk
## Class & Objects 
- you create a class with the keyword class
- you create a object by using the class outside and making bunch of it.
```
class MyClass {       // The class  
  public:             // Access specifier  
    int myNum;        // Attribute (int variable)  
    string myString;  // Attribute (string variable)  
};  
  
int main() {  
  MyClass myObj;      // Create an object of MyClass  
  
  // Access attributes and set values  
  myObj.myNum = 15;   
  myObj.myString = "Some text";  
  
  // Print attribute values  
  cout << myObj.myNum << "\n";  
  cout << myObj.myString;  
  return 0;  
}
```
- EX:
```
// Create a Car class with some attributes  
class Car {  
  public:  
    string brand;     
    string model;  
    int year;  
};  
  
int main() {  
  // Create an object of Car  
  Car carObj1;  
  carObj1.brand = "BMW";  
  carObj1.model = "X5";  
  carObj1.year = 1999;  
  
  // Create another object of Car  
  Car carObj2;  
  carObj2.brand = "Ford";  
  carObj2.model = "Mustang";  
  carObj2.year = 1969;  
  
  // Print attribute values  
  cout << carObj1.brand << " " << carObj1.model << " " << carObj1.year << "\n";  
  cout << carObj2.brand << " " << carObj2.model << " " << carObj2.year << "\n";  
  return 0;
```
## Methods 
- functions used in a classes are known as Methods
- There are two ways to define functions that belongs to a class:
	- Inside class definition
	- Outside class definition
### Inside Class 
```
class MyClass {        // The class  
  public:              // Access specifier  
    void myMethod() {  // Method/function defined inside the class  
      cout << "Hello World!";  
    }  
};  
  
int main() {  
  MyClass myObj;     // Create an object of MyClass  
  myObj.myMethod();  // Call the method  
  return 0;  
}
```
### Outside Class 
```
class MyClass {        // The class  
  public:              // Access specifier  
    void myMethod();   // Method/function declaration  
};  

void MyClass::myMethod() {  
  cout << "Hello World!";  
}                      // Method/function definition outside the class  


int main() {  
  MyClass myObj;       // Create an object of MyClass  
  myObj.myMethod();    // Call the method  
  return 0;  
}
```
## Constructor 
- Auto called when object of a class is created
```
class Car {                           // The class  
  public:                             // Access specifier  
    string brand;                     // Attribute  
    string model;                     // Attribute  
    int year;                         // Attribute  
    Car(string x, string y, int z) {  // Constructor with parameters  
      brand = x;  
      model = y;  
      year = z;  
    }  
};  
  
int main() {  
                                      // Create Car objects and call the                                                  constructor with different values  
  Car carObj1("BMW", "X5", 1999);  
  Car carObj2("Ford", "Mustang", 1969);  
  
  // Print values  
  cout << carObj1.brand << " " << carObj1.model << " " << carObj1.year << "\n";  
  cout << carObj2.brand << " " << carObj2.model << " " << carObj2.year << "\n";  
  return 0;  
}
```
- Ex:
```
class Car {        // The class  
  public:          // Access specifier  
    string brand;  // Attribute  
    string model;  // Attribute  
    int year;      // Attribute  
    Car(string x, string y, int z) { // Constructor with parameters  
      brand = x;  
      model = y;  
      year = z;  
    }  
};  
  
int main() {  
  // Create Car objects and call the constructor with different values  
  Car carObj1("BMW", "X5", 1999);  
  Car carObj2("Ford", "Mustang", 1969);  
  
  // Print values  
  cout << carObj1.brand << " " << carObj1.model << " " << carObj1.year << "\n";  
  cout << carObj2.brand << " " << carObj2.model << " " << carObj2.year << "\n";  
  return 0;  
}
```

## Access Specifier 
- `public` - members are accessible from outside the class
- `private` - members cannot be accessed (or viewed) from outside the class
- `protected` - members cannot be accessed from outside the class, however, they can be accessed in inherited classes. You will learn more about Inheritance later.
```
class MyClass {  
  **public:**    // Public access specifier  
    int x;   // Public attribute  
  **private:**   // Private access specifier  
    int y;   // Private attribute  
};  
  
int main() {  
  MyClass myObj;  
  myObj.x = 25;  // Allowed (public)  
  myObj.y = 50;  // Not allowed (private)  
  return 0;  
}
```
## Encapsulation 
- Hiding data "within" so that no one could access it.
```
#include <iostream>  
using namespace std;  
  
class Employee {  
  private:  
    // Private attribute  
    int salary;  
  
  public:  
    // Setter  
    void setSalary(int s) {  
      salary = s;  
    }  
    // Getter  
    int getSalary() {  
      return salary;  
    }  
};  
  
int main() {  
  Employee myObj;  
  myObj.setSalary(50000);  
  cout << myObj.getSalary();  
  return 0;  
}
```
## Inheritance 
- derived class (child) - the class that inherits from another class
- **base class** (parent) - the class being inherited from
- types:
	- single inheritance
	  `class vehicle{                                                            public:                                                                           void move() { cout << "moving\n";                                          }                                                                   };                                                                    class Car : public vehicle {};`
	- multilevel inheritance
	  `class vehicle {......};                                                    class car : public vehicle{....};                                          class sportscar : public car{....};`
	- multiple inheritance
	  `class Engine{....};                                                        class Wheels{....};                                                        class car : public Engine, public Wheels {....};`
## Polymorphism 
- many forms of same function
	- compile time polymorphism
		`void print(int x) {count << x; }                                          void print(string x) {count << x; }`
	- runtime polymorphism
	  `class Vehicle{                                                                            virtual void horn() {                                                               cout << "Vehicle horn\n"                                                   }                                                 };                                                                         class Car : public Vehicle {                                                           void horn() override{ cout << "car horn\n";                                }                                                              };`
## Files 
- use file to open file
```
ofstream file("example.txt");
file = "Hello, file";
file.close();
```
# Exception 
- try 
- catch
```
try {
	throw "An error occurred";
}
carch (const char* msg){
	cout << msg;
}
```

# Date
