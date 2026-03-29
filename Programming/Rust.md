# Rust Programming Language 🦀
<!--source: Easy rust--> 

# Comments

```rust
//this is a one-line comment in rust 
/* this is a multi-line comment in rust
    this works like charm
    look at this
*/
```
---

# Data types
In rust, Data types can be divided into two types.
1. Scalar Data type 
	- Integer Data type
		Integers are of two types, Signed and Unsigned integer
        | Length | Signed | Unsigned | 
        | --- | --- | --- |
        | 8 bit | i8 | u8 |
        | 16 bit | i16 | u16 | 
        | 32 bit | i32 | u32 |
        | 64 bit | i64 | u64 | 
        | 128 bit | i128 | u128 |
        | arch | isize | usize |
        Integer Literals are of few types
        | Number Literal | Example | 
        | ---- | ----- |
        | Decimal | 98_222 |
        | Hex | 0xff |
        | Octal | Oo77 | 
        | Binary | Ob1111_0000 | 
        | Byte(u8 only) | b'A' |
	- Floating Data type
		 There is a 64 bit float **f64** and  a 32 bit float **f32**
         Default value is 64 bit float for accuracy.
 	- Boolean type
        true and false thats it.
    - Character type
        char in rust can store a Unicode Scalar value. so it can also store unicode character's (emoji,chinese,etc..)(U+0000 to U+D7FF and UE0000 to U10FFFF)
2. Compound Data type
    Compound types can store more than one type into it.In rust there are two Compound data type
	- Tuple 
        Tuple is Heterogenous and they are comma separated list of values inside paranthases.
        
        ```rust
        fn main(){
            let tup: (i32, f64, u8) = (200,20.0,25);
            let test = (200,20.0,25);
            let (x,y,z) = tup; //by which each value of a tuple is stored as x y and z
            let r = tup.1;
            println!("y value is {}", y);
            println!("r value is {}", r);
        }
        ```
	- Array
        The array stores homogenous data and has an immutable size and length. they are stored in the stack rather than the heap.
        ```rust
        fn main(){
            let arr: [i32;5] = [123,144,122,123,100];
            let months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", 
                    "October", "November", "December"];
            let x = arr[0];
            let y = arr[1];
        }
        ```
        Rust provides a safety feature of not letting the program to even access the memory region if the accessed element is out of bound while running. so it still
        compiles but it doesn't let it access, hence preventing from invalid memory access.

3. User Defined types
    - Struct
        The struct is a curstom data type that lets you package together and name mutiple related values. It's like an object's data attributes.
        ```rust
            #[derive(Debug)]
            struct Rectangle{
                width: i32,
                height: i32,
            }

            impl Rectangle{
                fn area(&self) -> i32{
                    self.width * self.height
                }
            }


            #[derive(Debug)]
            struct Player{
                username: String,
                email: String, 
                active: bool,
            }

            struct Color(u8,u8,u8);

            fn build(email: String, username: String) -> Player{
                Player{
                    username,
                    email,
                    active: true,
                }
            }

            fn area(dimensions: (u8,u8)) -> u8{
                dimensions.0 * dimensions.1
            }

            fn main(){
                let mut user1: Player =  Player{username: String::from("Alex22"), email: String::from("alex@hotmale.com"), active: true};
                let id = user1.username;
                user1.username = String::from("SAlex22");
                let user2: Player = Player{username: String::from("Alex22"), ..user1}
                let rect: (u8,u8) = (20,30);
                println!("{:?}",rect );
                let rectangle1: Rectangle = Rectangle{width: 20, height: 30};
                println!("{}",rectangle1.area());
            }
        ```
    - Enum
        The Enum allows you to say a value is one of a possible set of values. Rust enums are particularly powerful because they can hold data directly.
        ```rust
        enum IpAddr{
            V4,
            V6,
        }

        fn main(){
            let four: IpAddr = IpAddr::V4;
            let six: IpAddr = IpAddr::V6;
            let lhost: IpAddr = Ip{kind: IpAddr::V4,address: String::from("127.0.0.1") };
        }

        struct Ip(){
            kind: IpAddr,
            address: String,
        }
        ```
    - Unions
        Used mainly for interfacing with c code(FFI). A union shares the same memory location for all its fields, so only one field can be used at a time.
        It's unsafe to use in most standard Rust code.

---

# Type-inference
This is where the compiler takes care of the data type for the variables. Basically all integers are i32 and all floats are f64. 
But there are some times you should specify the data type for the variable. 

1. During complex variable intialisation.
2. when you want a specific type that you prefer.

- To specify data type add a colon after the variable name specified.
``let x: i32 = 255;``

- You can also specify the data type behind the given value.
``let x = 255u32``
- For better readability, use _ as comma like for big numeric values. you can use it however you want and how much ever you wish and it isn't seen in output.
``let x = 25_000_000``
``let x = 2_50_00_000``

- In Floats, you can just add a '.' in the end of a number to make it a float.
``let x = 5. //this is just 5.0``

> [!NOTE]  NOTE
> float needs to be in same type for arithmetic operations. you can't add a f32 and f64 float. (mismated types error)
> To use different types for arithmetic operations, you need to cast it.

- also if one variable is in f32 and another one is not specified, the compiler will automatically assign the unassigned one too as f32.

---

# Variables and Mutability
- A variable is used to store data in the memory. In rust variables are immutable by default.
```rust
fn main(){
    let x = 20; //immutable by default
    //x = 40;  //not possible, throws error at compile time.
}
```

- To allow a variable value to change, you must declare it mutable using the keyword `mut`.

```rust 
fn main(){
    let mut x = 20;
    x = 40; //now this is possible
}
```

This is done by default for the following reasons.
- Prevent accidental changes.
- Improve Program safety. 
- Helps with safe Concurrency.

---
# Shadowing(Mutable reference)
Shadowing is the act of redeclaring the variable with same name.
```rust
fn main(){
    let x = 20;
    {
        let x = 40;
        println!("{}",x);
    }
    println!("{}",x);

    let y = 5;
    let y = y + 1;
    let y = y * 2;

    println!("y = {}", y);
}
```

---
# Const and Static
## Constants(Const)
They are used to create values that exist for the entire lifetime of the program.
```rust
fn main(){
    const PI: f64 = 3.14159;
}
```

characteristics of const
- Always specify the data type in const(the code won't compile if the type is not specified).
- Const is always immutable.
- They are evaluated at compile time.
- Can be declared anywhere(any scope).
- The value must be computed at compile time, so no expressions are allowed while creating a constant.
- A new copy is created whenever a const is modified in various scopes.
    ``const VALUE: i64 = x + 20`` //not allowed 

## Static
statics on the other hand is a global variable stored in a fixed memory location for the entire duration of the 
program.

```rust
static PI: f32 = 3.14159;
```

characteristics of static
- only one copy of it exists in the memory.
- exists for the entire lifetime of the static.(static lifetime)
- usually immutable.
- if the value is changed, since it has one copy, that will be changed.

You can also do mutable static using 'static mut' but it is discouraged because.
- they are unsafe
- mutiple threads could modify them simultaneously(thread safety issue)
- Data races
This can be fixed and used properly with the help of a few Concurrency tools like mutex, atomic types etc..

---
# stack, Heap, Pointers
Stack: is a region of the memory that stores the temporary data used by functions
- It is very fast.
- Stores fixed size data.
- Automatically managed.
- LIFO(Last in, First out)
- when a function ends the stack frame is automatically removed.

Heap: is a region of the memory that stores the data whose size may change at the runtime.
- It is Slower than stack.
- Stores dynamic data.
- requires memory allocation.
- accessed through pointers.
- The variable name is stored on the stack and the value is stored on the heap.

Pointers:  A pointer is the vairable that stores the memory address of another value.
- Reference Pointers: They refer to something.
- Mutable References: They allow the pointed variable to be mutable.
- Smart Pointers: They are advanced pointers which 
- Raw Pointers: they are unsafe pointers.
```rust
use std::rc::Rc;

fn main(){
    // Reference pointers
    let x = 30;
    let y = &x;
    println!("{}", y); //prints 30 
    println!("{}", &y); //& is optional here (auto-deref)

    //mutable reference
    let mut a = 20;
    let b = &mut a;

    *b = 40;   //must add *, can't deref automatically
    println!("{}", &b); //can auto-deref so optional &

    //smart pointers
    let d = Rc::new(10);
    let e = Rc::clone(&d);

    //raw pointer(unsafe, a const * in cpp/c)

    let ax = 5;
    let bx = &ax as *const i32;
    unsafe{
        println!("{}", *bx)//requires unsafe block to use it.
    }
}
```

---
# Functions
- functions are a better way to write a functionality combined into a block for future executions and reduce   
  repetitiveness
- Functions are written with the keyword `fn`
- The main function says the main flow of code in rust.
- Functions are written in snake case.
- In rust you don't need to care about where you define the function, the compiler takes care of it.
- Function parameters requires defenition of the datatype clearly.
- The value for functions provided in doesn't require you to specify the specific name of the parameter provided,
  (only order based).
- for returns you need to provide -> after the paranthesis with the return value

```rust
fn main(){
    let x = addition(5,6);
    println!("{}", x);
}

fn addition(x: i32,y: i32) -> i32{
    x + y
}
```

---
# Control Flow
Control flow is the basic idea of implementing various desirable actions to be done required incase of the outcome being fluctuating and unpredictabe.
There are Parts of Control Flow
- Conditions: Conditions are provided to check for a predicted outcome and do certain action.
- Iteration: Conditions are provided to check for certain predicted outcome and iterate for a specified time and do 
             certain opperation as provided.

## Conditions
if statement can be applied in various methods. this is the primary condition provided in order for checking.
```rust
//if statement
let number = 3;
if number < 5 {
    println!("condition was true");
} else if number == 5 {
    println!("condition was true"); //else if statement
}else {
    println!("condition was false");
} //else statement

//let-if statement
let condition = true;
let number = if condition {
    5
} else {
    6
};
```
> [!NOTE] NOTE
> data type retured in both cases should be same(no different data types)

## Iterators
```rust
fn main(){
    //iterator 1: using loop keyword
    loop{
        println!("loops again & again");
    }

    let i = 0;
    loop{
        println!("loops again & again");
        if i == 10{
            break;
        }
    }
    //iterator 2: using while loop
    let mut x = 0;
    while x != 10{
        println!("im printing rn");
        x += 1;
    }

    //iterator 3: using for loop
    for x in 1..10{
        println!("printing 10 times?");
    }
}
```

---
# Ownership and Borrowing
- Ownership is the new idea provided by the rust programming language. Rust reinvents the wheel of managing memory in a new way.
- Each variable has it value and the variable is the owner of it.
- There can be one owner at a time.
- When the owner goes out of the scope the value will also be dropped.
- When some other variable requires it(in a different scope) we need to borrow it from the owner to use it.
- Borrowing can be done in 4 ways(Mutable Reference,Reference,Smart Pointers,raw pointers)

---
# References
Reference is the idea of providing the address of a specific variable to another variable to let it access and modify or view it.

- Reference Pointers: They refer to something.
- Mutable References: They allow the pointed variable to be mutable.
```rust
// Reference pointers
let x = 30;
let y = &x;
println!("{}", y); //prints 30 
println!("{}", &y); //& is optional here (auto-deref)

//mutable reference
let mut a = 20;
let b = &mut a;

*b = 40;   //must add *, can't deref automatically
println!("{}", &b); //can auto-deref so optional &
```

---
# Operators
Operators are the symbols and types which are used for doing a specific operation.
## Arithmetic Operators
| Operator | Name |
|--- | --- |
| + | Addition | 
| - | Subtraction | 
| * | Multiplication | 
| / | Division | 
| % | Modulus |

```rust
let x = 10 + 20;
let y = 20 - 10;
let z = 10 * 10;
let a = z / x;
let b = a % 2;
```

## Comparison/Relational Operators

| Operator | Name |
|--- | --- |
| == | Equal | 
| != | Not Equal | 
| < | Lesser Than | 
| > | Greater Than | 
| >= | Greater than Equal to | 
| <= | Lesser than Equal to | 


## Logical Operators

| Operator | Name |
|--- | --- |
| && | logical and | 
| \|\| | logical or | 
| ! | Logical not | 

```rust 
if x > 0 && x < 100 { }   // both must be true
if x == 0 || x == 255 { } // at least one true
if !is_empty { }
```

## Bitwise Operator


| Operator | Name |
|--- | --- |
| & | Bitwise and | 
| \| | Bitwise or | 
| ^ | Bitwise xor | 
| ! | Bitwise not | 
| << | Leftward shift | 
| >> | Rightward shift| 


## Assignment operator 

| Operator | Name |
|--- | --- |
| = | Assign | 
| += | Add-asign | 
| -= | Subract-assign |
| *= | multiply-assign | 
| /= | divide-assign | 
| %= | remainder-assign | 
| &= | bitwise and-assign | 
| \|= | bitwise or-assign | 
| ^= | bitwise xor-assign | 
| >>= | rightward shift assign | 
| <<= | leftward shift assign |


## Reference and Dereference Operator

| Operator | Name |
|--- | --- |
| &x | Immutable Borrow | 
| &mut x | Mutable Borrow | 
| *x | Dereference | 

```rust
let x = 10;
let r = &x;        // immutable ref
println!("{}", *r); // dereference → 10

let mut y = 20;
let m = &mut y;
*m += 5;           // mutate through reference → y is now 25
```

## Range Operators(also used as slicing operators accordingly)

| Operator | Name |
|--- | --- |
| a..b | exclusive range | 
| a..=b | inclusive range | 
| a.. | range from | 
| ..b | range to | 
| ..=b | range to inclusive | 
| .. | full range | 

```rust
for i in 1..5  { }  // 1,2,3,4
for i in 1..=5 { }  // 1,2,3,4,5

let v = vec![10,20,30,40,50];
let s = &v[1..4];   // [20, 30, 40]
let s = &v[..];     // entire vec as slice
```

## Error Propagation Operators
`?` is used for error Propagationin Result and Option
```rust
fn parse_and_double(s: &str) -> Result<i32, std::num::ParseIntError> {
    let n = s.trim().parse::<i32>()?;  // returns Err early if parse fails
    Ok(n * 2)
}
```

## Type cast Operators 
`as` is used for type casting
```rust
let f = 3.99_f64;
let i = f as i32;       // 3 — truncates (does NOT round)
let b = 300_u32 as u8;  // 44 — wraps on overflow
let c = 65_u8 as char;  // 'A'
```

## Closure Operators 
`|` is used for defining an anonymous function that can capture its environment
```rust
let add    = |a, b| a + b;
let double = |x: i32| x * 2;
let greet  = |name: &str| format!("Hello, {}!", name);

// Capturing environment
let offset = 10;
let shift  = |x| x + offset;  // captures `offset` by reference
```

## Pattern Matching Operators 

| Operator | Name |
|--- | --- |
| \| | or-pattern |  
| @ | Bind-and-test | 
| _ | wildcard | 
| .. | rest/ignore | 
| if guard | condition | 
```rust
match value {
    0           => println!("zero"),
    1 | 2       => println!("one or two"),
    n @ 3..=9   => println!("small: {n}"),
    x if x < 0  => println!("negative: {x}"),
    _           => println!("large"),
}
```

## Path and scope Operators 

| Operator | Name |
|--- | --- |
| :: | path separator | 
| . | Field/method access | 
| -> | Return type(fn) | 
| => | match arm | 


## Pointers Operators(Unsafe)

| Operator | Name |
|--- | --- |
| *const T | Raw immutable pointer | 
| *mut T | raw mutable pointer | 
| *ptr | Dereference pointer |

```rust
let x = 42;
let p: *const i32 = &x;
unsafe {
    println!("{}", *p); // dereference raw pointer
}
```

---
# Slices

Slicing is the act of cutting up data and taking it away and either storing it or accessing it.
In rust it is just a fat pointer.

```rust
// Array / Vec slicing
let arr = [1, 2, 3, 4, 5];
let mid  = &arr[1..4];  // [2, 3, 4]
let tail = &arr[2..];   // [3, 4, 5]
let head = &arr[..3];   // [1, 2, 3]
let all  = &arr[..];    // [1, 2, 3, 4, 5]

// String slicing
let s = "hello world";
let hello = &s[0..5];  // "hello"
let world = &s[6..];   // "world"

let s = "héllo";       // 'é' is 2 bytes (bytes 1 and 2)

let ok  = &s[0..1];    // "h"  — valid boundary
let bad = &s[0..2];    // PANIC — cuts 'é' in half
let ok2 = &s[0..3];    // "hé" — 'é' ends at byte 3

let mut v = vec![1, 2, 3, 4, 5];

let slice = &mut v[1..4];  // mutable slice: [2, 3, 4]
slice[0] = 99;             // modifies v[1]
slice[2] = 77;             // modifies v[3]

println!("{:?}", v);       // [1, 99, 3, 77, 5]

// Accepts &[i32] — works with arrays, Vecs, or any slice
fn sum(numbers: &[i32]) -> i32 {
    numbers.iter().sum()
}

let arr = [1, 2, 3, 4, 5];
let vec = vec![10, 20, 30];

println!("{}", sum(&arr));       // pass array slice
println!("{}", sum(&vec));       // pass vec slice
println!("{}", sum(&vec[1..]));  // pass partial slice
```

---
# Structs
The struct is a curstom data type that lets you package together and name mutiple related values. It's like an object's data attributes.
```rust
[derive(Debug)]
struct Rectangle{
    width: i32,
    height: i32,
}

impl Rectangle{
    fn area(&self) -> i32{
        self.width * self.height
    }
}


#[derive(Debug)]
struct Player{
    username: String,
    email: String, 
    active: bool,
}

struct Color(u8,u8,u8);

fn build(email: String, username: String) -> Player{
    Player{
        username,
        email,
        active: true,
    }
}

fn area(dimensions: (u8,u8)) -> u8{
    dimensions.0 * dimensions.1
}

fn main(){
    let mut user1: Player =  Player{username: String::from("Alex22"), email: String::from("alex@hotmale.com"), active: true};
    let id = user1.username;
    user1.username = String::from("SAlex22");
    let user2: Player = Player{username: String::from("Alex22"), ..user1}
    let rect: (u8,u8) = (20,30);
    println!("{:?}",rect );
    let rectangle1: Rectangle = Rectangle{width: 20, height: 30};
    println!("{}",rectangle1.area());
}
```

---
# Enums
```rust
enum IpAddr{
    V4(String),
    V6(String),
    V8(u8,u8,u8,u8),
    Secret{name: String, message: String, size: u8},
}


enum State{
    Bliss,
    Tx,
    Rx,
}

enum Coin{
    Small,
    Medium,
    Large(State),
}

impl IpAddr{
    fn check(&mut self) {
        match self{
            IpAddr::Secret{name: n, message: m, size: s} => {
                if n.len() != *s as usize {
                    *s = m.len() as u8;
                }
            }
            _ => {}
        }
    }
}

enum Country{
    Position,
    Gdp,
}

struct Ctry{
    gdp: Country,
    name: String,
    position: Country,
}

fn main(){
    let localhost: IpAddr = IpAddr::V4(String::from("127.0.0.1"));
    let us: Ctry = Ctry{gdp: Country::Gdp,name: String::from("USA") ,position: Country::Position};
    let ip: IpAddr = IpAddr::V8(127,0,0,1);
    let mut sec: IpAddr = IpAddr::Secret{name: String::from("Alex"),message: String::from("Testing enums"), size: 8 };
    sec.check();
    match sec {
        IpAddr::Secret {size, ..} => { println!("{}", size)},
        _ => {}
    }

    let coin: Coin = Coin::Large(State::Bliss);

    match coin{
        Coin::Large(s) => {
            match s{
                State::Bliss => println!("state of bliss"),
                State::Tx => println!("State of text"),
                State::Rx => println!("State of Regret"),
                _ => {},
            }
        },
        _ => {},
    }
}

```

## Option Enum
```rust
//looks like this
enum Option<T>{
        Some(T),
        None,
}

//implementation
fn main(){
    let some_number: Option<u8> = Some(5);
    let some_string: option<String> = Some(String::from("something"));
    let absent_number: Option<i32> = None;

    let x: i8 = 4;
    let y: Option<i8> = Some(6);

    //let sum: i8 = x + y; //not possible 
    let sum: i8 = x + y.unwrap_or();//default 0
}

```

---
# Match

---
# Destructuring
# if-let
# Common-Collections
# Other-Collections
## vectors
## strings
## hashmaps (BTreeMap)
## vecDeque
## BinaryHeap
## HashSet (BTreeSet)
# Methods(impl)
# Generics
# Interior-Mutability
# Type-Aliases
# Lifetime
# Trait
# Closures
# Common-Macros
# Macros
# Iterators
# Attributes
# Arc
# Box
# Channels
# Deref and DerefMut
# Drop
# rc
# Standard libraries
# async-await
# Concurrency
# Threads
# Future
# Streams
# oop
# Trait-objects
# External-Crates(rand,rayon,serde,chrono,regex)
# oo
# oo-Design-Paterns
# Paterns
# Refutability
# Unsafe-Rust
