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

        struct Ip{
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

```rust
// ============================================
// Ownership rules
// ============================================

fn main() {
    // Each value has an owner
    let s1 = String::from("hello");
    let s2 = s1; // ownership moved to s2
    // println!("{}", s1); // ERROR: s1 is no longer valid

    // Clone creates a deep copy (both remain valid)
    let s3 = String::from("world");
    let s4 = s3.clone();
    println!("s3: {}, s4: {}", s3, s4); // both valid

    // Copy types (integers, bools, chars) are copied automatically
    let x = 5;
    let y = x;
    println!("x: {}, y: {}", x, y); // both valid

    // ============================================
    // Ownership and functions
    // ============================================

    let s = String::from("hello");
    takes_ownership(s);
    // s is no longer valid here

    let x = 5;
    makes_copy(x);
    println!("x is still valid: {}", x); // i32 implements Copy

    // ============================================
    // Return values transfer ownership
    // ============================================

    let s5 = gives_ownership();
    let s6 = String::from("hello");
    let s7 = takes_and_gives_back(s6);
    println!("s5: {}, s7: {}", s5, s7);
}

fn takes_ownership(some_string: String) {
    println!("Got: {}", some_string);
} // some_string goes out of scope and is dropped

fn makes_copy(some_integer: i32) {
    println!("Got: {}", some_integer);
}

fn gives_ownership() -> String {
    String::from("yours")
}

fn takes_and_gives_back(a_string: String) -> String {
    a_string
}
```

---
# References
Reference is the idea of providing the address of a specific variable to another variable to let it access and modify or view it.

```rust
// ============================================
// Immutable references (&T)
// ============================================

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1); // borrow s1
    println!("Length of '{}' is {}", s1, len); // s1 still valid

    // Multiple immutable references allowed
    let r1 = &s1;
    let r2 = &s1;
    let r3 = &s1;
    println!("{}, {}, {}", r1, r2, r3);

    // ============================================
    // Mutable references (&mut T)
    // ============================================

    let mut s2 = String::from("hello");
    change(&mut s2);
    println!("After change: {}", s2);

    // Only ONE mutable reference at a time
    let r1 = &mut s2;
    r1.push_str(" world");
    // let r2 = &mut s2; // ERROR: cannot borrow s2 as mutable more than once

    // Mutable and immutable refs cannot coexist
    // let r_immutable = &s2;
    // let r_mutable = &mut s2; // ERROR

    // ============================================
    // Dangling references (prevented by compiler)
    // ============================================

    // fn dangle() -> &String {
    //     let s = String::from("hello");
    //     &s // ERROR: s is dropped at end of function
    // }

    // ============================================
    // Reference rules summary
    // ============================================
    // 1. At any time, you can have EITHER:
    //    - One mutable reference, OR
    //    - Any number of immutable references
    // 2. References must always be valid
}

fn calculate_length(s: &String) -> usize {
    s.len()
} // s goes out of scope but doesn't drop (doesn't own it)

fn change(s: &mut String) {
    s.push_str(", world");
}
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
    let some_string: Option<String> = Some(String::from("something"));
    let absent_number: Option<i32> = None;

    let x: i8 = 4;
    let y: Option<i8> = Some(6);

    //let sum: i8 = x + y; //not possible 
    let sum: i8 = x + y.unwrap_or(0); // default 0
}

```

---
# Match
```rust
fn main(){
    let num = 10;
    match num {
        1 => println!("number is 1"),
        2 | 4 | 6 | 8 | 10 => println!("number is even"),
        13..=19 =>  println!("a teen number"),
        _ => println!("not special"),
    }
    
    let t = true;
    let bin = match t{
        true => 1,
        false => 0,
    }
}

```
---
# Destructuring
a match block can destructure items like `tuple, arrays, enums, pointers, structures`
## Destructuring tuples
```rust
fn main(){
    let values = (10, 20, 30);
    match values {
        (0,x,y) => println!("second and third value {} {}", x, y),
        (1,..) => println!("first value is 1, rest isn't necessary when .. is used"),
        (..,1) => println!("last value is 1, rest doesn't matter"),
        (1,..,0) => println!("the middle value doesn't matter, rest is 1 and 0"),
        _ => println!("the last default case"),
    }
}
```

## Destructuring arrays and slices
```rust
fn main(){
    let array = [10,-2, 2000];
    match array {
        [0,s,t] => println!("the values are {} {}, first value is 0", s, t),
        [0,_,t] => {println!("second value is ignored, first value is 0 and the last value is {}",t)},
        [-2,s ,..] => println!("third value is ignored, second value is {}, first value is -2 ", s),
        [3, _ , tail @ ..] => println!("the other elements after the third value is {:?}", tail), //can't use more than one ..
        [3, name @ ..] => println!("the other elements from the second ones {:?}", name)
    }
}
```

## Destructuring Enums
```rust
enum Color {
    Red,
    Green,
    Blue,
    RGB(u16,u16,u16),
    HSV(u16,u16,u16),
    HSL(u16,u16,u16),
    CMY(u16,u16,u16),
    CMYK(u16,u16,u16,u16),
    RGBA(u16,u16,u16,f32),
}
impl Color{
    fn check_color(&mut self){
        match self{
            Color::RGBA(..,a)=> {
                if *a > 1 || *a < 0 {
                    println!("invalid alpha");
                    *a = 0
                }
            },
            _ => {},
        }
    }
}

fn main() {
    let color = Color::RGB(122, 17, 40);
    // TODO ^ Try different variants for `color`

    println!("What color is it?");
    // An `enum` can be destructured using a `match`.
    match color {
        Color::Red   => println!("The color is Red!"),
        Color::Blue  => println!("The color is Blue!"),
        Color::Green => println!("The color is Green!"),
        Color::RGB(r, g, b) =>
            println!("Red: {}, green: {}, and blue: {}!", r, g, b),
        Color::HSV(h, s, v) =>
            println!("Hue: {}, saturation: {}, value: {}!", h, s, v),
        Color::HSL(h, s, l) =>
            println!("Hue: {}, saturation: {}, lightness: {}!", h, s, l),
        Color::CMY(c, m, y) =>
            println!("Cyan: {}, magenta: {}, yellow: {}!", c, m, y),
        Color::CMYK(c, m, y, k) =>
            println!("Cyan: {}, magenta: {}, yellow: {}, key (black): {}!",
                c, m, y, k),
        Color::RGBA(r,g,b,_) =>
            println!("Red: {}, Green: {}, Blue: {}, Alpha is unecessary for now", r, g, b),
    }
}
```

## Destructuring Pointers
```rust
fn main(){
    let reference = &4;
    let x = 10;
    let ref y = 20;
    let val = 5;
    let mut mut_val = 29;

    match reference {
        &v => println!("the value is {:#?}", v),
        _ => {},
    }
    match *reference {
        v => println!("got this value {:#?}", v),
        _ => {},
    }
    match x {
        ref r => println!("Reference to the value x {:#?}", r),
    }
    match mut_val {
        ref mut m => {
            *m = 20;
            println!("got the value {:#?}", m);
        }
    }

}
```

## Destructuring Structures
```rust
struct Player{
    name: String,
    age: i32,
    alive: bool,
    special_ages: (i32,i32,i32)
}
fn main(){
    let player1: Player = Player{name: String::from("Alex"), age: 32, alive: true, special_ages: (23,32,0)};
    match player1 {
        Player{name,age,alive,special_ages: (a,..)} => println!("name: {}, age: {}, alive: {}, special_age.1: {}", name, age, alive, a),
        Player{special_ages: r, ..} => println!("the last tuple is {:#?}", r),
        Player{age: a, name: n, ..} => println!("the age is {}, name is {}", a, n),
        //the order doesn't matter in a struct, rename using :, skip using .. and _
    }
}
```

---
# if-let
```rust
// ---------------------------
//  Basic if let with Option
let maybe_number = Some(10);
if let Some(x) = maybe_number {
    println!("Got a value: {}", x);
}

// ---------------------------
//  With else
let maybe_number: Option<i32> = None;
if let Some(x) = maybe_number {
    println!("Got: {}", x);
} else {
    println!("No value");
}

// ---------------------------
//  With Result
let result: Result<i32, &str> = Ok(42);
if let Ok(x) = result {
    println!("Success: {}", x);
} else {
    println!("Error occurred");
}

// ---------------------------
//  Destructuring a struct
struct Player { name: String, age: i32, alive: bool }
let player = Player { name: "Alex".to_string(), age: 32, alive: true };

if let Player { name, age, .. } = player {
    println!("{} is {} years old", name, age);
}

// ---------------------------
//  Destructuring a tuple
let point = (0, 5);
if let (x, 0) = point {
    println!("x-axis: {}", x);
}

// ---------------------------
//  Nested enum patterns
enum Color { RGBA(u8,u8,u8,f32), RGB(u8,u8,u8) }
let color = Color::RGBA(255, 0, 0, 0.5);
if let Color::RGBA(_, _, _, a) = color {
    if a < 1.0 { println!("Semi-transparent"); }
}

// ---------------------------
//  if let with a guard condition
let number = Some(8);
if let Some(x) = number if x > 5 {
    println!("Big number: {}", x);
}

// ---------------------------
//  Ignoring unused parts with _
let color = Color::RGBA(0, 255, 0, 1.0);
if let Color::RGBA(_, _, _, a) = color {
    println!("Alpha: {}", a);
}

// ---------------------------
//  Boolean check alternative with matches!
let num = Some(7);
if matches!(num, Some(x) if x > 5) {
    println!("Matches condition >5");
}

```
---
# Collections
Collections are basically
- They are Dynamic
- Heap allocated
- Resizable at runtime
Never consider array tuples and all those into these. They don't have any of these characteristics.
---
## Common-Collections
There are few common types of collection `String Vector HashMap`
### vectors
```rust
fn main() {
    // 1. Creating vectors
    let mut v: Vec<i32> = Vec::new(); // empty vector
    v.push(10);
    v.push(20);
    v.push(30);

    // Another way (macro)
    let mut v2 = vec![1, 2, 3, 4];

    // 2. Accessing elements
    let first = v[0]; // direct indexing (can panic if out of bounds)
    println!("First element: {}", first);

    // Safe access using get()
    match v.get(1) {
        Some(value) => println!("Second element: {}", value),
        None => println!("No element found"),
    }

    // 3. Iterating over vector (immutable)
    for i in &v {
        println!("Value: {}", i);
    }

    // 4. Mutable iteration (modify values)
    for i in &mut v {
        *i += 5; // dereference and update
    }
    println!("After mutation: {:?}", v);

    // 5. Removing elements
    v.pop(); // removes last element
    println!("After pop: {:?}", v);

    v.remove(0); // removes element at index 0
    println!("After remove index 0: {:?}", v);

    // 6. Length vs Capacity
    let mut v3 = Vec::new();
    println!("Initial capacity: {}", v3.capacity());

    v3.push(1);
    v3.push(2);
    v3.push(3);

    println!("Length: {}", v3.len());         // number of elements
    println!("Capacity: {}", v3.capacity());  // allocated space

    // 7. Ownership example
    let v4 = vec![100, 200, 300];

    for val in v4 {
        println!("Owned value: {}", val);
    }
    // v4 is no longer usable here (moved in loop)

    // 8. Storing different types using enum
    enum Data {
        Int(i32),
        Float(f64),
        Text(String),
    }

    let mixed = vec![
        Data::Int(10),
        Data::Float(3.14),
        Data::Text(String::from("hello")),
    ];

    println!("Mixed vector created!");
}
```

---
### strings
```rust
fn main() {
    // 1. Creating Strings
    let mut s1 = String::new(); // empty string
    s1.push('H');                // add a single character
    s1.push_str("ello");         // append a &str
    println!("s1: {}", s1);      // s1: Hello

    // Another way: from literal
    let s2 = String::from("Rust Programming");
    println!("s2: {}", s2);

    // 2. Concatenation
    let s3 = s1 + " World"; // Note: s1 is moved here
    println!("s3: {}", s3);

    // Using format! macro (does not take ownership)
    let s4 = format!("{} - {}", s2, s3);
    println!("s4: {}", s4);

    // 3. Accessing characters (careful: Strings are UTF-8)
    // let ch = s2[0]; // ❌ Not allowed, panics
    for c in s2.chars() {      // iterate over characters
        print!("{} ", c);
    }
    println!();

    for b in s2.bytes() {      // iterate over bytes
        print!("{} ", b);
    }
    println!();

    // 4. Slicing strings safely
    let slice = &s2[0..4]; // first 4 bytes (valid UTF-8)
    println!("Slice: {}", slice);

    // 5. Modifying string
    let mut s5 = String::from("Rust");
    s5.push_str("Lang"); // append string
    println!("s5: {}", s5);

    s5.insert(4, ' ');   // insert at index
    println!("s5 after insert: {}", s5);

    s5.remove(4);        // remove character at index
    println!("s5 after remove: {}", s5);

    // 6. Conversion between &str and String
    let s6: &str = "Hello &str";
    let s7: String = s6.to_string();
    println!("s7: {}", s7);

    // 7. Ownership and cloning
    let s8 = s7.clone(); // deep copy
    println!("s8 (clone): {}", s8);
}
```

---
### hashmaps 
```rust
use std::collections::HashMap;

fn main() {
    // 1. Creating HashMaps

    // Empty HashMap (key: &str, value: i32)
    let mut scores: HashMap<&str, i32> = HashMap::new();

    // Creating with initial values using collect
    let teams = vec![("Alice", 50), ("Bob", 30), ("Charlie", 70)];
    let mut scores2: HashMap<_, _> = teams.into_iter().collect();

    println!("Empty HashMap: {:?}", scores);
    println!("HashMap from vector: {:?}", scores2);

    // 2. Inserting key-value pairs
    scores.insert("Alice", 100);
    scores.insert("Bob", 80);
    scores.insert("Charlie", 90);
    println!("After insertions: {:?}", scores);

    // 3. Accessing values

    // a) Using get (safe, returns Option)
    match scores.get("Alice") {
        Some(score) => println!("Alice's score: {}", score),
        None => println!("No score found"),
    }

    // b) Using entry API (conditional insertion)
    scores.entry("Dave").or_insert(60); // insert if key doesn't exist
    println!("After entry insert: {:?}", scores);

    // 4. Updating values

    // Overwrite existing key
    scores.insert("Alice", 120);

    // Modify value conditionally
    scores.entry("Bob").and_modify(|v| *v += 10);
    println!("After updates: {:?}", scores);

    // 5. Iterating over HashMap

    // a) Immutable iteration
    for (name, score) in &scores {
        println!("{} => {}", name, score);
    }

    // b) Mutable iteration
    for (_, score) in &mut scores {
        *score += 5; // increase all scores by 5
    }
    println!("After mutable iteration: {:?}", scores);

    // 6. Removing entries
    scores.remove("Charlie"); // remove key "Charlie"
    println!("After removal: {:?}", scores);

    // 7. Checking key existence
    if scores.contains_key("Alice") {
        println!("Alice is in the map");
    }

    if !scores.contains_key("Charlie") {
        println!("Charlie was removed");
    }

    // 8. Ownership rules

    let name = String::from("Eve");
    let value = 70;
    scores.insert(&name, value); // reference as key
    println!("After inserting reference key: {:?}", scores);
    // name can still be used since we inserted a reference, not moved

    let name2 = String::from("Frank");
    let value2 = 85;
    scores.insert(&name2, value2); // ownership can vary depending on key type

    // 9. Using complex types as values
    #[derive(Debug)]
    struct Player {
        level: u32,
        health: u32,
    }

    let mut player_map: HashMap<&str, Player> = HashMap::new();
    player_map.insert("Alice", Player { level: 5, health: 100 });
    player_map.insert("Bob", Player { level: 7, health: 80 });

    println!("Player map: {:?}", player_map);

    // 10. Iterating over keys or values
    for key in scores.keys() {
        println!("Key: {}", key);
    }

    for value in scores.values() {
        println!("Value: {}", value);
    }

    // 11. HashMap ordering
    // Note: HashMap is unordered; iterating may not return keys in insertion order
    println!("Final HashMap: {:?}", scores);
}

```

---
# Other-Collections
There are few uncommon types of collection like `LinkedList BinaryHep HashSet VecDeque BTreeSet BTreeMap`
### VecDeque
```rust
use std::collections::VecDeque;

fn main() {
    // 1. Creating VecDeque
    let mut dq: VecDeque<i32> = VecDeque::new();
    println!("Empty VecDeque: {:?}", dq);

    // 2. Adding elements
    dq.push_back(10);   // add to back
    dq.push_back(20);
    dq.push_front(5);   // add to front
    dq.push_front(2);
    println!("After push_front and push_back: {:?}", dq);

    // 3. Removing elements
    let front = dq.pop_front(); // remove from front
    let back = dq.pop_back();   // remove from back
    println!("Popped front: {:?}, back: {:?}", front, back);
    println!("VecDeque now: {:?}", dq);

    // 4. Accessing elements by index
    if let Some(first) = dq.get(0) {
        println!("First element by index: {}", first);
    }

    // 5. Iterating
    for val in &dq {
        println!("Value: {}", val);
    }

    // 6. Length and capacity
    println!("Length: {}", dq.len());       // number of elements
    println!("Capacity: {}", dq.capacity()); // internal allocated space

    // 7. Conversion from Vec
    let v = vec![1, 2, 3, 4];
    let dq_from_vec: VecDeque<_> = v.into_iter().collect();
    println!("VecDeque from Vec: {:?}", dq_from_vec);

    // 8. Using complex types
    #[derive(Debug)]
    struct Item {
        id: u32,
        name: String,
    }

    let mut items: VecDeque<Item> = VecDeque::new();
    items.push_back(Item { id: 1, name: "Sword".to_string() });
    items.push_front(Item { id: 2, name: "Shield".to_string() });
    println!("VecDeque with structs: {:?}", items);

    // 9. Pop until empty
    while let Some(val) = dq.pop_front() {
        println!("Removing: {}", val);
    }
    println!("VecDeque empty: {:?}", dq);
}
```

---
### BinaryHeap
```rust
use std::collections::BinaryHeap;

fn main() {
    // 1. Creating a BinaryHeap
    let mut heap = BinaryHeap::new();
    println!("Empty heap: {:?}", heap);

    // 2. Inserting elements
    heap.push(50);
    heap.push(20);
    heap.push(70);
    heap.push(10);
    println!("Heap after pushes: {:?}", heap); // Max element is on top

    // 3. Accessing the top element
    if let Some(max) = heap.peek() {
        println!("Max element: {}", max);
    }

    // 4. Removing elements (pop)
    while let Some(val) = heap.pop() {
        println!("Removing element: {}", val);
    }
    println!("Heap empty: {:?}", heap);

    // 5. Using BinaryHeap as min-heap
    use std::cmp::Reverse;

    let mut min_heap = BinaryHeap::new();
    min_heap.push(Reverse(50));
    min_heap.push(Reverse(20));
    min_heap.push(Reverse(70));
    min_heap.push(Reverse(10));

    println!("Min-heap elements in order:");
    while let Some(Reverse(val)) = min_heap.pop() {
        println!("{}", val); // smallest element first
    }

    // 6. BinaryHeap with custom struct
    #[derive(Eq, PartialEq, Debug)]
    struct Task {
        priority: u32,
        name: String,
    }

    // Implement Ord for max-heap based on priority
    use std::cmp::Ordering;
    impl Ord for Task {
        fn cmp(&self, other: &Self) -> Ordering {
            self.priority.cmp(&other.priority) // max-heap
        }
    }

    impl PartialOrd for Task {
        fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
            Some(self.cmp(other))
        }
    }

    let mut tasks = BinaryHeap::new();
    tasks.push(Task { priority: 3, name: "Low".to_string() });
    tasks.push(Task { priority: 10, name: "High".to_string() });
    tasks.push(Task { priority: 7, name: "Medium".to_string() });

    println!("Tasks in priority order:");
    while let Some(task) = tasks.pop() {
        println!("{} (priority {})", task.name, task.priority);
    }
}
```

---
### HashSet 
```rust
use std::collections::HashSet;

fn main() {
    println!("=== CREATING HASHSETS ===");
    // 1. Empty HashSet
    let mut fruits: HashSet<&str> = HashSet::new();
    println!("Empty HashSet: {:?}", fruits);

    // 2. From array or Vec
    let numbers = vec![1, 2, 3, 2, 3, 4];
    let mut num_set: HashSet<_> = numbers.into_iter().collect();
    println!("HashSet from Vec (duplicates removed): {:?}", num_set);

    println!("\n=== ADDING ELEMENTS ===");
    fruits.insert("Apple");
    fruits.insert("Banana");
    fruits.insert("Mango");
    fruits.insert("Apple"); // duplicate, ignored
    println!("After insertions: {:?}", fruits);

    println!("\n=== CHECKING EXISTENCE ===");
    if fruits.contains("Banana") {
        println!("Banana is in the set");
    }
    if !fruits.contains("Orange") {
        println!("Orange is not in the set");
    }

    println!("\n=== REMOVING ELEMENTS ===");
    fruits.remove("Mango");
    println!("After removal: {:?}", fruits);

    println!("\n=== ITERATION ===");
    for fruit in &fruits {
        println!("Fruit: {}", fruit);
    }

    println!("\n=== LENGTH & EMPTY CHECK ===");
    println!("Length: {}", fruits.len());
    println!("Is empty? {}", fruits.is_empty());

    println!("\n=== SET OPERATIONS ===");
    let set_a: HashSet<_> = [1, 2, 3, 4].iter().cloned().collect();
    let set_b: HashSet<_> = [3, 4, 5, 6].iter().cloned().collect();

    let union: HashSet<_> = set_a.union(&set_b).cloned().collect();
    println!("Union: {:?}", union);

    let intersection: HashSet<_> = set_a.intersection(&set_b).cloned().collect();
    println!("Intersection: {:?}", intersection);

    let difference: HashSet<_> = set_a.difference(&set_b).cloned().collect();
    println!("Difference (A-B): {:?}", difference);

    let sym_diff: HashSet<_> = set_a.symmetric_difference(&set_b).cloned().collect();
    println!("Symmetric difference: {:?}", sym_diff);

    println!("\n=== ADVANCED USAGE ===");
    // HashSet with Strings
    let mut names: HashSet<String> = HashSet::new();
    names.insert("Alice".to_string());
    names.insert("Bob".to_string());
    println!("HashSet of Strings: {:?}", names);

    // Using retain to filter
    names.retain(|name| name.starts_with('A'));
    println!("After retain (starts with 'A'): {:?}", names);

    // Extending from another set
    let mut more_names: HashSet<String> = ["Charlie".to_string(), "Alice".to_string()].iter().cloned().collect();
    names.extend(more_names);
    println!("After extending: {:?}", names);

    // Clearing all elements
    names.clear();
    println!("After clear, is empty? {}", names.is_empty());
}
```

---
### BTreeSet
```rust
use std::collections::BTreeSet;

fn main() {
    println!("=== CREATING BTREESET ===");
    // 1. Empty BTreeSet
    let mut set: BTreeSet<i32> = BTreeSet::new();
    println!("Empty BTreeSet: {:?}", set);

    // 2. Inserting elements
    set.insert(5);
    set.insert(1);
    set.insert(3);
    set.insert(5); // duplicate ignored
    println!("After insertions: {:?}", set); // elements sorted automatically

    println!("\n=== CHECKING EXISTENCE ===");
    println!("Contains 3? {}", set.contains(&3));
    println!("Contains 10? {}", set.contains(&10));

    println!("\n=== REMOVING ELEMENTS ===");
    set.remove(&1);
    println!("After removal: {:?}", set);

    println!("\n=== ITERATION ===");
    println!("Iterate ascending:");
    for x in &set {
        println!("{}", x);
    }

    println!("Iterate descending:");
    for x in set.iter().rev() {
        println!("{}", x);
    }

    println!("\n=== LENGTH & EMPTY CHECK ===");
    println!("Length: {}", set.len());
    println!("Is empty? {}", set.is_empty());

    println!("\n=== RANGE QUERIES ===");
    let mut range_set: BTreeSet<i32> = (1..10).collect();
    println!("Full set: {:?}", range_set);

    // Get range 3..7
    for x in range_set.range(3..7) {
        println!("In range 3..7: {}", x);
    }

    // Range inclusive 3..=7
    for x in range_set.range(3..=7) {
        println!("In range 3..=7: {}", x);
    }

    println!("\n=== SET OPERATIONS ===");
    let set_a: BTreeSet<_> = [1,2,3,4].iter().cloned().collect();
    let set_b: BTreeSet<_> = [3,4,5,6].iter().cloned().collect();

    let union: BTreeSet<_> = set_a.union(&set_b).cloned().collect();
    println!("Union: {:?}", union);

    let intersection: BTreeSet<_> = set_a.intersection(&set_b).cloned().collect();
    println!("Intersection: {:?}", intersection);

    let difference: BTreeSet<_> = set_a.difference(&set_b).cloned().collect();
    println!("Difference (A-B): {:?}", difference);

    let sym_diff: BTreeSet<_> = set_a.symmetric_difference(&set_b).cloned().collect();
    println!("Symmetric difference: {:?}", sym_diff);

    println!("\n=== ADVANCED USAGE ===");
    // BTreeSet of strings
    let mut names: BTreeSet<String> = BTreeSet::new();
    names.insert("Charlie".to_string());
    names.insert("Alice".to_string());
    names.insert("Bob".to_string());
    println!("BTreeSet of Strings (sorted): {:?}", names);

    // Removing all
    names.clear();
    println!("After clear, is empty? {}", names.is_empty());
}
```
---
### BTreeMap
```rust
use std::collections::BTreeMap;

fn main() {
    println!("=== CREATING BTREEMAP ===");
    // 1. Empty BTreeMap
    let mut scores: BTreeMap<&str, i32> = BTreeMap::new();
    println!("Empty BTreeMap: {:?}", scores);

    // 2. Inserting elements
    scores.insert("Alice", 50);
    scores.insert("Bob", 30);
    scores.insert("Charlie", 70);
    println!("After insertion: {:?}", scores); // sorted by keys

    // 3. Accessing values
    if let Some(score) = scores.get("Alice") {
        println!("Alice's score: {}", score);
    }

    // 4. Updating values
    scores.entry("Alice").and_modify(|s| *s += 10);
    println!("After updating Alice: {:?}", scores);

    // 5. Removing elements
    scores.remove("Bob");
    println!("After removal: {:?}", scores);

    println!("\n=== ITERATION ===");
    for (name, score) in &scores {
        println!("{} => {}", name, score);
    }

    println!("Iterate in reverse:");
    for (name, score) in scores.iter().rev() {
        println!("{} => {}", name, score);
    }

    println!("\n=== LENGTH & EMPTY CHECK ===");
    println!("Length: {}", scores.len());
    println!("Is empty? {}", scores.is_empty());

    println!("\n=== RANGE QUERIES ===");
    // Example: scores with keys from "A" to "C"
    for (name, score) in scores.range("A".."C") {
        println!("In range A..C: {} => {}", name, score);
    }

    println!("\n=== FROM ARRAY / VEC ===");
    let v = vec![("Dave", 40), ("Eve", 90)];
    let mut map_from_vec: BTreeMap<_, _> = v.into_iter().collect();
    println!("BTreeMap from Vec: {:?}", map_from_vec);

    println!("\n=== ADVANCED USAGE ===");
    // Complex types as values
    #[derive(Debug)]
    struct Player {
        level: u32,
        hp: u32,
    }

    let mut player_map: BTreeMap<String, Player> = BTreeMap::new();
    player_map.insert("Alice".to_string(), Player { level: 10, hp: 100 });
    player_map.insert("Bob".to_string(), Player { level: 5, hp: 50 });
    for (name, player) in &player_map {
        println!("{} => {:?}", name, player);
    }

    // Clearing all
    player_map.clear();
    println!("After clear, is empty? {}", player_map.is_empty());
}
```

---
### Linked List
```rust
use std::collections::LinkedList;

fn main() {
    println!("=== CREATING LINKEDLIST ===");
    // 1. Empty LinkedList
    let mut list: LinkedList<i32> = LinkedList::new();
    println!("Empty LinkedList: {:?}", list);

    println!("\n=== ADDING ELEMENTS ===");
    // 2. Add elements to back
    list.push_back(10);
    list.push_back(20);
    list.push_back(30);

    // 3. Add elements to front
    list.push_front(5);
    list.push_front(2);

    println!("After insertions: {:?}", list);

    println!("\n=== ACCESSING LENGTH & EMPTY CHECK ===");
    println!("Length: {}", list.len());
    println!("Is empty? {}", list.is_empty());

    println!("\n=== REMOVING ELEMENTS ===");
    list.pop_front();
    list.pop_back();
    println!("After pop_front and pop_back: {:?}", list);

    println!("\n=== ITERATION ===");
    println!("Iterate forward:");
    for val in &list {
        println!("{}", val);
    }

    println!("Iterate mutable (multiply by 2):");
    for val in &mut list {
        *val *= 2;
    }
    println!("After mutation: {:?}", list);

    println!("Iterate reverse:");
    for val in list.iter().rev() {
        println!("{}", val);
    }

    println!("\n=== ADVANCED OPERATIONS ===");
    // Merging two LinkedLists
    let mut list2: LinkedList<i32> = LinkedList::new();
    list2.push_back(100);
    list2.push_back(200);

    println!("List1 before append: {:?}", list);
    println!("List2: {:?}", list2);

    list.append(&mut list2); // list2 becomes empty
    println!("List1 after append: {:?}", list);
    println!("List2 after append (empty now): {:?}", list2);

    // Splitting a list
    let mut split_list: LinkedList<i32> = LinkedList::new();
    split_list.push_back(1);
    split_list.push_back(2);
    split_list.push_back(3);
    split_list.push_back(4);

    let mut second_half = split_list.split_off(2); // first 2 elements stay, rest move
    println!("First half after split: {:?}", split_list);
    println!("Second half after split: {:?}", second_half);

    // Clearing all elements
    split_list.clear();
    second_half.clear();
    println!("After clearing, is split_list empty? {}", split_list.is_empty());
    println!("After clearing, is second_half empty? {}", second_half.is_empty());
}
```

---
# Methods(impl)
Methods are similar to functions but are defined within `impl` blocks and are associated with a specific type (struct, enum, or trait). The first parameter is always `self`, which represents the instance the method is being called on.

```rust
// ============================================
// Basic impl block with methods
// ============================================

#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    // Associated function (no self parameter)
    // Called using :: syntax: Rectangle::square(10)
    fn square(size: u32) -> Rectangle {
        Rectangle { width: size, height: size }
    }

    // Method taking immutable reference (&self)
    // Can read data but cannot modify it
    fn area(&self) -> u32 {
        self.width * self.height
    }

    // Method taking mutable reference (&mut self)
    // Can read and modify data
    fn resize(&mut self, new_width: u32, new_height: u32) {
        self.width = new_width;
        self.height = new_height;
    }

    // Method taking ownership (self)
    // Consumes the instance, cannot be used after call
    fn into_parts(self) -> (u32, u32) {
        (self.width, self.height)
    }

    // Method chaining (builder pattern — takes ownership, returns Self)
    fn with_width(mut self, width: u32) -> Self {
        self.width = width;
        self
    }

    fn with_height(mut self, height: u32) -> Self {
        self.height = height;
        self
    }
}

// ============================================
// Multiple impl blocks are allowed
// ============================================

impl Rectangle {
    // Separate impl block for organization
    fn perimeter(&self) -> u32 {
        2 * (self.width + self.height)
    }

    fn is_square(&self) -> bool {
        self.width == self.height
    }
}

// ============================================
// Methods on enums
// ============================================

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("Quitting"),
            Message::Move { x, y } => println!("Moving to ({}, {})", x, y),
            Message::Write(text) => println!("Writing: {}", text),
            Message::ChangeColor(r, g, b) => println!("Color: ({}, {}, {})", r, g, b),
        }
    }

    fn description(&self) -> &str {
        match self {
            Message::Quit => "quit message",
            Message::Move { .. } => "move message",
            Message::Write(_) => "write message",
            Message::ChangeColor(..) => "color change message",
        }
    }
}

// ============================================
// Nested structs with methods
// ============================================

#[derive(Debug)]
struct Point {
    x: f64,
    y: f64,
}

#[derive(Debug)]
struct Circle {
    center: Point,
    radius: f64,
}

impl Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }

    fn circumference(&self) -> f64 {
        2.0 * std::f64::consts::PI * self.radius
    }

    fn contains(&self, point: &Point) -> bool {
        let dx = point.x - self.center.x;
        let dy = point.y - self.center.y;
        (dx * dx + dy * dy).sqrt() <= self.radius
    }

    fn translate(&mut self, dx: f64, dy: f64) {
        self.center.x += dx;
        self.center.y += dy;
    }
}

// ============================================
// Usage examples
// ============================================

fn main() {
    // Creating and using methods
    let mut rect = Rectangle { width: 30, height: 50 };
    println!("Area: {}", rect.area());           // 1500
    println!("Perimeter: {}", rect.perimeter()); // 160
    println!("Is square: {}", rect.is_square()); // false

    // Mutating through methods
    rect.resize(100, 200);
    println!("After resize: {:?}", rect);

    // Consuming method (takes ownership)
    let rect2 = Rectangle { width: 10, height: 20 };
    let (w, h) = rect2.into_parts();
    // rect2 is no longer valid here

    // Associated function (no instance needed)
    let sq = Rectangle::square(25);
    println!("Square area: {}", sq.area()); // 625

    // Method chaining pattern
    let chained = Rectangle { width: 0, height: 0 }
        .with_width(40)
        .with_height(60);
    println!("Chained rectangle: {:?}", chained);

    // Enum methods
    let msg = Message::Move { x: 10, y: 20 };
    msg.call();                          // "Moving to (10, 20)"
    println!("Type: {}", msg.description());

    // Nested struct methods
    let circle = Circle {
        center: Point { x: 0.0, y: 0.0 },
        radius: 5.0,
    };
    println!("Circle area: {:.2}", circle.area());
    println!("Circumference: {:.2}", circle.circumference());

    let point = Point { x: 3.0, y: 4.0 };
    println!("Contains point: {}", circle.contains(&point)); // true (distance = 5.0)
}
```

---
# Generics
Generics allow you to write code that works with multiple types without duplicating logic. Rust uses monomorphization — the compiler generates concrete type-specific versions at compile time, so there is zero runtime overhead.

```rust
// ============================================
// Generic functions
// ============================================

// Single generic type parameter
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    largest
}

// Multiple generic type parameters
fn pair<T, U>(first: T, second: U) -> (T, U) {
    (first, second)
}

// Generic function returning a new value
fn duplicate<T: Clone>(value: &T) -> (T, T) {
    (value.clone(), value.clone())
}

// ============================================
// Generic structs
// ============================================

// Generic struct with one type parameter
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

// Generic struct with multiple type parameters
#[derive(Debug)]
struct MixedPoint<T, U> {
    x: T,
    y: U,
}

// Generic struct with multiple fields of same type
#[derive(Debug)]
struct Container<T> {
    value: T,
    label: String,
}

// ============================================
// Generic enums
// ============================================

// Rust's built-in Option<T> and Result<T, E> are generic enums
#[derive(Debug)]
enum Maybe<T> {
    Just(T),
    Nothing,
}

#[derive(Debug)]
enum Outcome<T, E> {
    Success(T),
    Failure(E),
}

// ============================================
// Generic impl blocks
// ============================================

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }

    fn y(&self) -> &T {
        &self.y
    }
}

// impl block restricted to a specific concrete type
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

// impl block with additional trait bounds
impl<T: std::fmt::Display> Container<T> {
    fn describe(&self) -> String {
        format!("Container('{}') holds: {}", self.label, self.value)
    }
}

// ============================================
// Generic methods that introduce new type parameters
// ============================================

impl<T> Point<T> {
    // This method introduces its own generic parameter U
    fn mixup<U>(self, other: Point<U>) -> MixedPoint<T, U> {
        MixedPoint {
            x: self.x,
            y: other.y,
        }
    }
}

// ============================================
// Generic structs with const generics
// ============================================

// Const generics allow values (not just types) as parameters
#[derive(Debug)]
struct FixedArray<T, const N: usize> {
    data: [T; N],
}

impl<T: Default + Copy, const N: usize> FixedArray<T, N> {
    fn new() -> Self {
        FixedArray {
            data: [T::default(); N],
        }
    }

    fn len(&self) -> usize {
        N
    }

    fn get(&self, index: usize) -> Option<&T> {
        if index < N {
            Some(&self.data[index])
        } else {
            None
        }
    }
}

// ============================================
// Generic newtype wrappers
// ============================================

#[derive(Debug)]
struct Wrapper<T>(T);

impl<T> Wrapper<T> {
    fn inner(&self) -> &T {
        &self.0
    }

    fn into_inner(self) -> T {
        self.0
    }
}

// ============================================
// Usage examples
// ============================================

fn main() {
    // Generic functions
    let numbers = vec![34, 50, 25, 100, 65];
    let result = largest(&numbers);
    println!("Largest number: {}", result); // 100

    let chars = vec!['y', 'm', 'a', 'q'];
    let result = largest(&chars);
    println!("Largest char: {}", result); // 'y'

    let p = pair(5, "hello");
    println!("Pair: {:?}", p); // (5, "hello")

    let val = 42;
    let dup = duplicate(&val);
    println!("Duplicated: {:?}", dup); // (42, 42)

    // Generic structs
    let int_point = Point { x: 5, y: 10 };
    let float_point = Point { x: 1.0, y: 4.0 };
    println!("Int point: {:?}", int_point);
    println!("Float point: {:?}", float_point);

    // Mixed type generic struct
    let mixed = MixedPoint { x: 5, y: 4.0 };
    println!("Mixed point: {:?}", mixed);

    // Generic enum
    let something: Maybe<i32> = Maybe::Just(42);
    let nothing: Maybe<i32> = Maybe::Nothing;
    println!("{:?}, {:?}", something, nothing);

    let ok: Outcome<&str, &str> = Outcome::Success("done");
    let err: Outcome<&str, &str> = Outcome::Failure("error");
    println!("{:?}, {:?}", ok, err);

    // Generic impl methods
    println!("Point x: {}", int_point.x());
    println!("Distance: {}", float_point.distance_from_origin());

    // mixup — combines two Points of different types
    let p1 = Point { x: 5, y: 10 };
    let p2 = Point { x: 1.0, y: 4.0 };
    let p3 = p1.mixup(p2);
    println!("Mixed point after mixup: x={}, y={}", p3.x, p3.y);

    // Const generics
    let arr: FixedArray<i32, 5> = FixedArray::new();
    println!("FixedArray length: {}", arr.len()); // 5
    println!("FixedArray[0]: {:?}", arr.get(0));  // Some(0)
    println!("FixedArray[5]: {:?}", arr.get(5));  // None

    let filled = FixedArray { data: [1, 2, 3, 4, 5] };
    println!("Filled FixedArray: {:?}", filled);

    // Generic newtype
    let w = Wrapper(42);
    println!("Wrapper inner: {}", w.inner());
    let inner = w.into_inner();
    println!("Unwrapped: {}", inner);
}
```

---
# Interior-Mutability
Interior mutability is a design pattern in Rust that allows you to mutate data even when there are immutable references to it. Normally, Rust enforces borrowing rules at compile time: either one `&mut T` or many `&T`. Interior mutability defers this enforcement to runtime using `unsafe` internally, wrapped in safe APIs.

Key types: `Cell`, `RefCell`, `Mutex`, `RwLock`, `Atomic*`, `OnceCell`/`OnceLock`

```rust
use std::cell::{Cell, RefCell};
use std::sync::{Mutex, RwLock};
use std::sync::atomic::{AtomicUsize, Ordering};

// ============================================
// Cell<T> — for Copy types only
// Copies values in and out. No runtime checks.
// ============================================

fn demo_cell() {
    let c = Cell::new(5);

    // Get a copy of the value
    let val = c.get();
    println!("Cell value: {}", val); // 5

    // Set a new value (works through &Cell, not &mut)
    c.set(10);
    println!("After set: {}", c.get()); // 10

    // Replace and take
    let old = c.replace(20);
    println!("Replaced: {}, now: {}", old, c.get()); // 10, 20

    let taken = c.take(); // replaces with Default::default() (0 for i32)
    println!("Taken: {}, remaining: {}", taken, c.get()); // 20, 0
}

// ============================================
// RefCell<T> — runtime borrow checking
// Panics if you violate borrowing rules at runtime.
// ============================================

fn demo_refcell() {
    let data = RefCell::new(vec![1, 2, 3]);

    // Immutable borrow
    let borrowed = data.borrow();
    println!("RefCell contents: {:?}", *borrowed);
    // `borrowed` must be dropped before mutable borrow

    // Mutable borrow
    let mut borrowed_mut = data.borrow_mut();
    borrowed_mut.push(4);
    borrowed_mut.push(5);
    // drops here

    println!("After mutation: {:?}", data.borrow()); // [1, 2, 3, 4, 5]

    // try_borrow returns Result instead of panicking
    match data.try_borrow() {
        Ok(b) => println!("Borrowed: {:?}", *b),
        Err(e) => println!("Borrow failed: {}", e),
    }
}

// ============================================
// Interior mutability in structs (common pattern)
// Allows mutation through &self methods
// ============================================

#[derive(Debug)]
struct Cache {
    data: RefCell<Vec<String>>,
    hit_count: Cell<u32>,
}

impl Cache {
    fn new() -> Self {
        Cache {
            data: RefCell::new(Vec::new()),
            hit_count: Cell::new(0),
        }
    }

    // Mutates internal state through &self (not &mut self)
    fn add(&self, item: String) {
        self.data.borrow_mut().push(item);
    }

    fn hits(&self) -> u32 {
        self.hit_count.set(self.hit_count.get() + 1);
        self.hit_count.get()
    }

    fn dump(&self) -> Vec<String> {
        self.data.borrow().clone()
    }
}

// ============================================
// Mutex<T> — thread-safe interior mutability
// Uses OS-level locking. Blocks threads.
// ============================================

fn demo_mutex() {
    let counter = Mutex::new(0);

    // Lock and mutate
    {
        let mut num = counter.lock().unwrap();
        *num += 1;
    } // lock released here

    println!("Mutex counter: {}", *counter.lock().unwrap()); // 1

    // try_lock returns Result instead of blocking/deadlocking
    match counter.try_lock() {
        Ok(mut num) => *num += 1,
        Err(_) => println!("Could not acquire lock"),
    }
}

// ============================================
// RwLock<T> — multiple readers OR one writer
// ============================================

fn demo_rwlock() {
    let data = RwLock::new(vec![1, 2, 3]);

    // Multiple readers can coexist
    let r1 = data.read().unwrap();
    let r2 = data.read().unwrap();
    println!("Readers: {:?}, {:?}", *r1, *r2);
    drop(r1);
    drop(r2);

    // Exclusive write access
    {
        let mut w = data.write().unwrap();
        w.push(4);
    }

    println!("After write: {:?}", *data.read().unwrap()); // [1, 2, 3, 4]
}

// ============================================
// Atomic types — lock-free thread-safe mutation
// ============================================

fn demo_atomics() {
    let counter = AtomicUsize::new(0);

    // Atomic operations with memory ordering
    counter.fetch_add(1, Ordering::SeqCst);
    counter.fetch_add(1, Ordering::SeqCst);

    // load and store
    println!("Atomic counter: {}", counter.load(Ordering::SeqCst)); // 2

    // compare-and-swap style
    counter.compare_exchange(
        2,          // expected
        10,         // new value
        Ordering::SeqCst,
        Ordering::SeqCst,
    ).ok();

    println!("After CAS: {}", counter.load(Ordering::SeqCst)); // 10
}

// ============================================
// Rc<RefCell<T>> — shared ownership + mutation (single-threaded)
// ============================================

use std::rc::Rc;

fn demo_rc_refcell() {
    let shared = Rc::new(RefCell::new(vec![1, 2, 3]));

    let a = Rc::clone(&shared);
    let b = Rc::clone(&shared);

    // Both can mutate the same data
    a.borrow_mut().push(4);
    b.borrow_mut().push(5);

    println!("Shared data: {:?}", shared.borrow()); // [1, 2, 3, 4, 5]
    println!("Reference count: {}", Rc::strong_count(&shared)); // 3
}

// ============================================
// Practical example: Observer pattern with interior mutability
// ============================================

#[derive(Debug)]
struct Observable {
    value: Cell<i32>,
    observers: RefCell<Vec<Box<dyn Fn(i32)>>>,
}

impl Observable {
    fn new(initial: i32) -> Self {
        Observable {
            value: Cell::new(initial),
            observers: RefCell::new(Vec::new()),
        }
    }

    fn subscribe<F: Fn(i32) + 'static>(&self, callback: F) {
        self.observers.borrow_mut().push(Box::new(callback));
    }

    fn set(&self, new_value: i32) {
        self.value.set(new_value);
        for cb in self.observers.borrow().iter() {
            cb(new_value);
        }
    }

    fn get(&self) -> i32 {
        self.value.get()
    }
}

// ============================================
// Usage
// ============================================

fn main() {
    demo_cell();
    demo_refcell();
    demo_mutex();
    demo_rwlock();
    demo_atomics();
    demo_rc_refcell();

    // Cache with interior mutability
    let cache = Cache::new();
    cache.add("item1".to_string());
    cache.add("item2".to_string());
    println!("Cache hits: {}", cache.hits()); // 1
    println!("Cache hits: {}", cache.hits()); // 2
    println!("Cache dump: {:?}", cache.dump());

    // Observable pattern
    let obs = Observable::new(0);
    obs.subscribe(|v| println!("Observer 1 got: {}", v));
    obs.subscribe(|v| println!("Observer 2 got: {}", v));
    obs.set(42);
    // Observer 1 got: 42
    // Observer 2 got: 42
}
```

---
# Type-Aliases
Type aliases give an existing type a new name using the `type` keyword. They do not create new types — just aliases for readability.

```rust
// ============================================
// Basic type aliases
// ============================================

type Kilometers = i32;
type Thunk = Box<dyn std::fmt::Display + Send>;

fn main() {
    let x: Kilometers = 5;
    println!("x = {}", x);

    // Alias for long types
    type Result<T> = std::result::Result<T, std::io::Error>;
    type Map = std::collections::HashMap<String, Vec<i32>>;

    let mut map: Map = std::collections::HashMap::new();
    map.insert("key".to_string(), vec![1, 2, 3]);

    // Alias for function pointers
    type Callback = fn(i32, i32) -> i32;

    fn add(a: i32, b: i32) -> i32 { a + b }
    fn mul(a: i32, b: i32) -> i32 { a * b }

    let op: Callback = add;
    println!("Result: {}", op(3, 4)); // 7

    let op2: Callback = mul;
    println!("Result: {}", op2(3, 4)); // 12
}
```

---
# Lifetime
Lifetimes ensure that references are valid for as long as they are used. The compiler can often infer them, but explicit annotations are needed when it cannot.

```rust
// ============================================
// Lifetime annotations on functions
// ============================================

// Both params and return share the same lifetime
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Return lifetime tied to first param only
fn first_word<'a>(s: &'a str, _other: &str) -> &'a str {
    s.split_whitespace().next().unwrap_or(s)
}

// ============================================
// Lifetime annotations on structs
// ============================================

struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn text(&self) -> &str {
        self.part
    }

    fn announce_and_return(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part
    }
}

// ============================================
// Lifetime elision rules
// ============================================

// Compiler infers: each param gets its own lifetime,
// return gets the lifetime of self if it exists
struct Parser {
    input: String,
}

impl Parser {
    // Elided: fn parse(&self) -> &str
    fn parse(&self) -> &str {
        &self.input
    }
}

// ============================================
// Static lifetime
// ============================================

fn get_static() -> &'static str {
    "I live for the entire program duration"
}

// ============================================
// Lifetime bounds on generics
// ============================================

fn longest_with_announcement<'a, T>(
    x: &'a str,
    y: &'a str,
    ann: T,
) -> (&'a str, T)
where
    T: std::fmt::Display,
{
    println!("Announcement: {}", ann);
    (if x.len() > y.len() { x } else { y }, ann)
}

// ============================================
// Usage
// ============================================

fn main() {
    let s1 = String::from("long string");
    let result;
    {
        let s2 = String::from("xyz");
        result = longest(s1.as_str(), s2.as_str());
        println!("Longest: {}", result);
    }

    let excerpt = Excerpt { part: "important text" };
    println!("Excerpt: {}", excerpt.text());

    let parser = Parser { input: "hello world".to_string() };
    println!("Parsed: {}", parser.parse());

    let s = get_static();
    println!("Static: {}", s);

    let (longest, _) = longest_with_announcement("dog", "horse", 7);
    println!("Longest: {}", longest);
}
```

---
# Trait
Traits define shared behavior — similar to interfaces in other languages. They specify what methods a type must have.

```rust
// ============================================
// Defining and implementing traits
// ============================================

pub trait Summary {
    // Required method (no default)
    fn summarize_author(&self) -> String;

    // Default implementation (can be overridden)
    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}

struct NewsArticle {
    headline: String,
    location: String,
    author: String,
    content: String,
}

impl Summary for NewsArticle {
    fn summarize_author(&self) -> String {
        format!("@{}", self.author)
    }
}

struct Tweet {
    username: String,
    content: String,
    reply: bool,
    retweet: bool,
}

impl Summary for Tweet {
    fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }

    // Override default implementation
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}

// ============================================
// Trait as function parameters
// ============================================

fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

// Equivalent with trait bound syntax
fn notify2<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// Multiple trait bounds
fn notify3(item: &(impl Summary + std::fmt::Display)) {}
fn notify4<T: Summary + std::fmt::Display>(item: &T) {}

// Where clause (cleaner for many bounds)
fn notify5<T>(item: &T)
where
    T: Summary + std::fmt::Display,
{
}

// ============================================
// Returning types that implement traits
// ============================================

fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("horse_ebooks"),
        content: String::from("of course"),
        reply: false,
        retweet: false,
    }
}

// ============================================
// Conditional implementations with traits
// ============================================

use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Pair { x, y }
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("x >= y: {}", self.x);
        } else {
            println!("y > x: {}", self.y);
        }
    }
}

// ============================================
// Blanket implementations
// ============================================

trait ToJson {
    fn to_json(&self) -> String;
}

// Automatically implemented for all types that implement Display
impl<T: Display> ToJson for T {
    fn to_json(&self) -> String {
        format!("{{\"value\": \"{}\"}}", self)
    }
}

// ============================================
// Usage
// ============================================

fn main() {
    let tweet = Tweet {
        username: String::from("user"),
        content: String::from("hello world"),
        reply: false,
        retweet: false,
    };
    println!("Tweet: {}", tweet.summarize());

    let article = NewsArticle {
        headline: String::from("Headline"),
        location: String::from("NY"),
        author: String::from("Author"),
        content: String::from("Content"),
    };
    println!("Article: {}", article.summarize());

    notify(&tweet);
    notify(&article);

    let ret = returns_summarizable();
    println!("Returned: {}", ret.summarize());

    let pair = Pair::new(10, 20);
    pair.cmp_display();

    // Blanket impl — i32 implements Display, so it gets ToJson
    println!("{}", 42.to_json());
    println!("{}", 3.14.to_json());
}
```

---
# Closures
Closures are anonymous functions that can capture variables from their environment. They are written with `|args| body` syntax.

```rust
// ============================================
// Closure syntax variations
// ============================================

fn main() {
    // No parameters, no capture
    let greet = || println!("Hello!");
    greet();

    // With parameters
    let add = |a: i32, b: i32| a + b;
    println!("Add: {}", add(3, 4)); // 7

    // Type inference on params
    let double = |x| x * 2;
    println!("Double: {}", double(5)); // 10

    // Multi-line closure
    let process = |x: i32| {
        let result = x * x;
        println!("Processing: {} -> {}", x, result);
        result
    };
    process(6);

    // ============================================
    // Capturing environment
    // ============================================

    let x = 10;
    let print_x = || println!("Captured x: {}", x);
    print_x();

    // ============================================
    // Fn, FnMut, FnOnce traits
    // ============================================

    // Fn: captures by reference, can be called multiple times
    let s = String::from("hello");
    let borrow = || println!("{}", s);
    borrow();
    borrow();
    println!("s still valid: {}", s);

    // FnMut: captures by mutable reference
    let mut count = 0;
    let mut increment = || {
        count += 1;
        count
    };
    println!("Count: {}", increment()); // 1
    println!("Count: {}", increment()); // 2

    // FnOnce: takes ownership, can only be called once
    let greeting = String::from("hi");
    let consume = || {
        println!("{}", greeting);
    };
    consume();
    // consume(); // Error: FnOnce, already consumed

    // ============================================
    // move keyword — force ownership capture
    // ============================================

    let data = vec![1, 2, 3];
    let handle = std::thread::spawn(move || {
        println!("Thread got: {:?}", data);
    });
    handle.join().unwrap();
    // data is moved, no longer accessible here

    // ============================================
    // Closures as function parameters
    // ============================================

    fn apply<F>(f: F, val: i32) -> i32
    where
        F: Fn(i32) -> i32,
    {
        f(val)
    }

    println!("Apply: {}", apply(|x| x * x, 7)); // 49

    // ============================================
    // Closures returning iterators
    // ============================================

    let nums = vec![1, 2, 3, 4, 5];
    let doubled: Vec<_> = nums.iter().map(|x| x * 2).collect();
    println!("Doubled: {:?}", doubled);

    let evens: Vec<_> = nums.iter().filter(|x| *x % 2 == 0).collect();
    println!("Evens: {:?}", evens);
}
```

---
# Common-Macros
Rust provides several built-in macros that are used frequently.

```rust
// ============================================
// println! / print! — formatted output
// ============================================

fn main() {
    let name = "World";
    let num = 42;

    println!("Hello, {}!", name);           // positional
    println!("{0} + {1} = {result}", 1, 2, result = 3); // named
    println!("{:?}", vec![1, 2, 3]);        // Debug
    println!("{:#?}", vec![1, 2, 3]);       // Pretty Debug
    println!("{:x}", 255);                  // Hex
    println!("{:b}", 10);                   // Binary
    println!("{:.2}", 3.14159);             // 2 decimal places
    println!("{:>10}", "right");            // Right-aligned width 10
    println!("{:0>5}", 42);                 // Zero-padded: 00042

    // ============================================
    // format! — returns String instead of printing
    // ============================================

    let s = format!("{} is {}", name, num);
    println!("Formatted: {}", s);

    // ============================================
    // eprintln! / eprint! — stderr output
    // ============================================

    eprintln!("This goes to stderr");

    // ============================================
    // vec! — create Vec with values
    // ============================================

    let v = vec![1, 2, 3, 4, 5];
    let repeated = vec![0; 10]; // ten zeros

    // ============================================
    // assert! / assert_eq! / assert_ne!
    // ============================================

    assert!(true);
    assert_eq!(1 + 1, 2);
    assert_ne!(1 + 1, 3);

    // With custom message
    // assert!(false, "This will panic with this message");

    // ============================================
    // dbg! — quick debug printing
    // ============================================

    let x = 5;
    let y = dbg!(x * 2); // prints [file:line] x * 2 = 10
    println!("y = {}", y);

    // ============================================
    // panic! — explicit panic
    // ============================================

    // panic!("Something went wrong!");

    // ============================================
    // todo! / unimplemented! / unreachable!
    // ============================================

    // todo!();           // "not yet implemented"
    // unimplemented!();  // same as todo!
    // unreachable!();    // "internal error: entered unreachable code"

    // ============================================
    // concat! / env! / env!
    // ============================================

    let path = concat!(env!("CARGO_MANIFEST_DIR"), "/src/main.rs");
    println!("Path: {}", path);

    // ============================================
    // stringify! — turns tokens into string literal
    // ============================================

    let s = stringify!(1 + 2);
    println!("Stringified: {}", s); // "1 + 2"

    // ============================================
    // include! / include_str! / include_bytes!
    // ============================================

    // let code = include_str!("path/to/file.rs");
    // let data = include_bytes!("path/to/file.bin");
}
```

---
# Macros
Macros are code that writes code. Declarative macros (`macro_rules!`) match patterns and expand, while procedural macros operate on the AST.

```rust
// ============================================
// Declarative macros with macro_rules!
// ============================================

// Simple macro
macro_rules! say_hello {
    () => {
        println!("Hello from macro!");
    };
}

// Macro with arguments
macro_rules! create_function {
    ($func_name:ident) => {
        fn $func_name() {
            println!("Function {:?} was called!", stringify!($func_name));
        }
    };
}

create_function!(foo);
create_function!(bar);

// Macro with expressions
macro_rules! my_vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}

// Macro with repetition and separators
macro_rules! hashmap {
    ( $( $key:expr => $value:expr ),* $(,)? ) => {
        {
            let mut map = std::collections::HashMap::new();
            $(
                map.insert($key, $value);
            )*
            map
        }
    };
}

// Macro with different match arms
macro_rules! match_type {
    ($e:expr) => {
        match $e {
            $e:ident => println!("identifier: {}", stringify!($e)),
            $e:literal => println!("literal: {}", $e),
            _ => println!("something else"),
        }
    };
}

// ============================================
// Procedural macros (require separate crate)
// ============================================

// #[derive(MyMacro)]   — Custom derive
// #[my_attribute]      — Attribute-like
// my_macro!(...)        — Function-like

// Example of a derive macro (would be in a proc-macro crate):
// use proc_macro::TokenStream;
// #[proc_macro_derive(HelloMacro)]
// pub fn hello_macro_derive(input: TokenStream) -> TokenStream { ... }

// ============================================
// Usage
// ============================================

fn main() {
    say_hello!();
    foo();
    bar();

    let v = my_vec![1, 2, 3, 4, 5];
    println!("my_vec: {:?}", v);

    let map = hashmap! {
        "a" => 1,
        "b" => 2,
        "c" => 3,
    };
    println!("hashmap: {:?}", map);
}
```

---
# Iterators
Iterators provide a way to process sequences of items lazily. All iterators implement the `Iterator` trait.

```rust
// ============================================
// Creating and using iterators
// ============================================

fn main() {
    let v = vec![1, 2, 3, 4, 5];

    // iter() — borrows each element
    for val in v.iter() {
        println!("Borrowed: {}", val);
    }

    // into_iter() — takes ownership
    for val in v.clone().into_iter() {
        println!("Owned: {}", val);
    }

    // iter_mut() — mutable borrow
    let mut v2 = vec![1, 2, 3];
    for val in v2.iter_mut() {
        *val += 10;
    }
    println!("Mutated: {:?}", v2); // [11, 12, 13]

    // ============================================
    // Iterator adaptors (lazy — do nothing until consumed)
    // ============================================

    let nums = vec![1, 2, 3, 4, 5];

    // map — transform each element
    let doubled: Vec<_> = nums.iter().map(|x| x * 2).collect();
    println!("Doubled: {:?}", doubled);

    // filter — keep elements matching predicate
    let evens: Vec<_> = nums.iter().filter(|x| *x % 2 == 0).collect();
    println!("Evens: {:?}", evens);

    // filter_map — filter and transform in one step
    let parsed: Vec<i32> = ["1", "two", "3", "4"]
        .iter()
        .filter_map(|s| s.parse().ok())
        .collect();
    println!("Parsed: {:?}", parsed); // [1, 3, 4]

    // enumerate — add index
    let enumerated: Vec<_> = nums.iter().enumerate().collect();
    println!("Enumerated: {:?}", enumerated);

    // zip — combine two iterators
    let a = [1, 2, 3];
    let b = [4, 5, 6];
    let zipped: Vec<_> = a.iter().zip(b.iter()).collect();
    println!("Zipped: {:?}", zipped); // [(1,4), (2,5), (3,6)]

    // take / skip
    let first_three: Vec<_> = nums.iter().take(3).collect();
    println!("First 3: {:?}", first_three);

    let skipped: Vec<_> = nums.iter().skip(2).collect();
    println!("Skipped 2: {:?}", skipped);

    // chain — concatenate iterators
    let chained: Vec<_> = a.iter().chain(b.iter()).collect();
    println!("Chained: {:?}", chained);

    // flat_map — flatten nested iterators
    let nested = vec![vec![1, 2], vec![3, 4], vec![5]];
    let flat: Vec<_> = nested.iter().flat_map(|v| v.iter()).collect();
    println!("Flattened: {:?}", flat);

    // ============================================
    // Iterator consumers (produce a final value)
    // ============================================

    let nums = vec![1, 2, 3, 4, 5];

    // sum / product
    let total: i32 = nums.iter().sum();
    let product: i32 = nums.iter().product();
    println!("Sum: {}, Product: {}", total, product);

    // fold / reduce
    let folded = nums.iter().fold(0, |acc, x| acc + x);
    println!("Folded: {}", folded);

    // find — first matching element
    let found = nums.iter().find(|x| *x > 3);
    println!("Found > 3: {:?}", found);

    // position — index of first match
    let pos = nums.iter().position(|x| *x == 3);
    println!("Position of 3: {:?}", pos);

    // count
    let count = nums.iter().count();
    println!("Count: {}", count);

    // max / min
    println!("Max: {:?}", nums.iter().max());
    println!("Min: {:?}", nums.iter().min());

    // any / all
    println!("Any > 4: {}", nums.iter().any(|x| *x > 4));
    println!("All > 0: {}", nums.iter().all(|x| *x > 0));

    // collect into different types
    let squares: std::collections::HashMap<_, _> =
        nums.iter().map(|x| (x, x * x)).collect();
    println!("Squares map: {:?}", squares);

    // ============================================
    // Implementing Iterator for a custom type
    // ============================================

    struct Counter {
        count: u32,
        max: u32,
    }

    impl Counter {
        fn new(max: u32) -> Self {
            Counter { count: 0, max }
        }
    }

    impl Iterator for Counter {
        type Item = u32;

        fn next(&mut self) -> Option<Self::Item> {
            if self.count < self.max {
                self.count += 1;
                Some(self.count)
            } else {
                None
            }
        }
    }

    let counter = Counter::new(5);
    let sum: u32 = counter.zip(Counter::new(5).skip(1))
        .map(|(a, b)| a * b)
        .sum();
    println!("Counter product sum: {}", sum);
}
```

---
# Attributes
Attributes are metadata applied to modules, crates, functions, etc. They use `#[...]` syntax. Inner attributes use `#![...]`.

```rust
// ============================================
// Crate-level attributes (inner)
// ============================================

// #![warn(unused)]
// #![allow(dead_code)]

// ============================================
// Conditional compilation
// ============================================

#[cfg(target_os = "linux")]
fn linux_only() {
    println!("Running on Linux");
}

#[cfg(target_os = "windows")]
fn windows_only() {
    println!("Running on Windows");
}

#[cfg(debug_assertions)]
fn debug_only() {
    println!("Debug build");
}

#[cfg(feature = "serde")]
fn with_serde() {
    println!("Serde feature enabled");
}

#[cfg(all(target_os = "linux", target_arch = "x86_64"))]
fn linux_x86_64() {
    println!("Linux x86_64");
}

#[cfg(any(unix, windows))]
fn unix_or_windows() {
    println!("Unix or Windows");
}

// ============================================
// Derive macros
// ============================================

#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
struct User {
    name: String,
    age: u32,
}

// ============================================
// Test attribute
// ============================================

#[test]
fn it_works() {
    assert_eq!(2 + 2, 4);
}

#[test]
#[should_panic]
fn this_panics() {
    panic!("expected panic");
}

#[test]
#[ignore]
fn expensive_test() {
    // Skipped unless --include-ignored is passed
}

// ============================================
// Lint control attributes
// ============================================

#[allow(dead_code)]
fn unused_function() {}

#[warn(unused_variables)]
fn with_warning(x: i32) {
    let _y = 5;
}

#[deny(unused_mut)]
fn strict_mut(x: i32) {
    let _y = x;
}

// ============================================
// Other common attributes
// ============================================

#[must_use]
fn important_result() -> bool {
    true
}

#[inline]
fn fast_function() {}

#[inline(always)]
fn always_inline() {}

#[cold]
fn rarely_called() {}

// ============================================
// Doc comments (desugar to #[doc = "..."])
// ============================================

/// Adds two numbers together.
///
/// # Examples
/// 
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// 
///fn add(a: i32, b: i32) -> i32 {
/// a + b
///}

// ============================================
// Usage
// ============================================

fn main() {
    let user = User {
        name: "Alice".to_string(),
        age: 30,
    };
    println!("{:?}", user);

    #[cfg(target_os = "linux")]
    linux_only();

    let _ = important_result();
    println!("Add: {}", add(2, 3));
}
```

---
# Arc
`Arc<T>` (Atomic Reference Counted) enables shared ownership across multiple threads. It uses atomic operations for thread-safe reference counting.

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    // ============================================
    // Basic Arc usage
    // ============================================

    let data = Arc::new(vec![1, 2, 3, 4, 5]);
    let mut handles = vec![];

    for i in 0..3 {
        let data_clone = Arc::clone(&data);
        let handle = thread::spawn(move || {
            println!("Thread {}: {:?}", i, data_clone);
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    // ============================================
    // Arc with Mutex for shared mutable access
    // ============================================

    let counter = Arc::new(std::sync::Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Counter: {}", *counter.lock().unwrap()); // 10

    // ============================================
    // Arc::strong_count
    // ============================================

    let val = Arc::new(42);
    println!("Count: {}", Arc::strong_count(&val)); // 1

    let v2 = Arc::clone(&val);
    println!("Count: {}", Arc::strong_count(&val)); // 2

    drop(v2);
    println!("Count: {}", Arc::strong_count(&val)); // 1

    // ============================================
    // Arc::try_unwrap — convert back to owned T
    // ============================================

    let arc = Arc::new(String::from("hello"));
    if let Ok(inner) = Arc::try_unwrap(arc) {
        println!("Unwrapped: {}", inner);
    }
}
```

---
# Box
`Box<T>` allocates data on the heap. It provides single ownership of heap-allocated data.

```rust
fn main() {
    // ============================================
    // Basic Box usage
    // ============================================

    let b = Box::new(5);
    println!("b = {}", b);

    // ============================================
    // Recursive types (Box is required)
    // ============================================

    #[derive(Debug)]
    enum List {
        Cons(i32, Box<List>),
        Nil,
    }

    use List::{Cons, Nil};
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
    println!("List: {:?}", list);

    // ============================================
    // Trait objects (dynamic dispatch)
    // ============================================

    trait Draw {
        fn draw(&self);
    }

    struct Button;
    struct TextField;

    impl Draw for Button {
        fn draw(&self) { println!("Drawing button"); }
    }

    impl Draw for TextField {
        fn draw(&self) { println!("Drawing text field"); }
    }

    let components: Vec<Box<dyn Draw>> = vec![
        Box::new(Button),
        Box::new(TextField),
    ];

    for c in &components {
        c.draw();
    }

    // ============================================
    // Box::leak — convert to &'static mut
    // ============================================

    let s: &'static mut String = Box::leak(Box::new(String::from("leaked")));
    s.push_str(" forever");
    println!("Leaked: {}", s);

    // ============================================
    // From/Into conversions
    // ============================================

    let boxed: Box<[i32]> = vec![1, 2, 3].into_boxed_slice();
    println!("Boxed slice: {:?}", boxed);
}
```

---
# Channels
Channels enable message-passing between threads using `mpsc` (multi-producer, single-consumer).

```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    // ============================================
    // Basic channel usage
    // ============================================

    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        tx.send("Hello from thread!").unwrap();
    });

    let received = rx.recv().unwrap();
    println!("Received: {}", received);

    // ============================================
    // Multiple messages
    // ============================================

    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("msg 1"),
            String::from("msg 2"),
            String::from("msg 3"),
        ];
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_millis(100));
        }
    });

    for received in rx {
        println!("Got: {}", received);
    }

    // ============================================
    // Multiple producers (clone tx)
    // ============================================

    let (tx, rx) = mpsc::channel();
    let tx1 = tx.clone();

    thread::spawn(move || {
        tx.send(vec![1, 2, 3]).unwrap();
    });

    thread::spawn(move || {
        tx1.send(vec![4, 5, 6]).unwrap();
    });

    for received in rx {
        println!("Got vector: {:?}", received);
    }

    // ============================================
    // sync_channel — bounded (synchronous)
    // ============================================

    let (tx, rx) = mpsc::sync_channel(1); // buffer size 1

    thread::spawn(move || {
        tx.send("synced").unwrap();
    });

    println!("Bounded: {}", rx.recv().unwrap());

    // ============================================
    // try_recv — non-blocking receive
    // ============================================

    let (tx, rx) = mpsc::channel();
    tx.send("quick").unwrap();

    match rx.try_recv() {
        Ok(msg) => println!("try_recv: {}", msg),
        Err(_) => println!("No message"),
    }
}
```

---
# Deref and DerefMut
The `Deref` trait allows customizing the behavior of the `*` dereference operator. It enables smart pointers to behave like references.

```rust
use std::ops::{Deref, DerefMut};

// ============================================
// Custom Deref implementation
// ============================================

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T> DerefMut for MyBox<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

// ============================================
// Deref coercion
// ============================================

fn hello(name: &str) {
    println!("Hello, {}!", name);
}

// ============================================
// Smart pointer with Deref
// ============================================

struct Wrapper {
    data: String,
    cached_len: std::cell::Cell<usize>,
}

impl Deref for Wrapper {
    type Target = String;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl DerefMut for Wrapper {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.data
    }
}

// ============================================
// Usage
// ============================================

fn main() {
    let x = MyBox::new(5);
    println!("Dereferenced: {}", *x);

    // Deref coercion: &MyBox<String> → &String → &str
    let m = MyBox::new(String::from("World"));
    hello(&m); // automatically coerced

    // DerefMut
    let mut w = Wrapper {
        data: String::from("hello"),
        cached_len: std::cell::Cell::new(5),
    };
    w.push_str(" world");
    println!("Wrapper: {}", w);
}
```

---
# Drop
The `Drop` trait lets you run code when a value goes out of scope — useful for cleanup like closing files, releasing locks, or freeing resources.

```rust
use std::ops::Drop;

// ============================================
// Basic Drop implementation
// ============================================

struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`", self.data);
    }
}

// ============================================
// Drop order (reverse of declaration)
// ============================================

struct NamedDrop(&'static str);

impl Drop for NamedDrop {
    fn drop(&mut self) {
        println!("Dropping {}", self.0);
    }
}

// ============================================
// std::mem::drop — force early drop
// ============================================

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("Smart pointers created.");
    // d drops first, then c (reverse order)

    // Force drop early
    let e = CustomSmartPointer {
        data: String::from("early drop"),
    };
    std::mem::drop(e); // explicit drop
    // e.drop() would be error — Drop::drop takes &mut self
    println!("e dropped early.");

    // Drop order demo
    {
        let _a = NamedDrop("a");
        let _b = NamedDrop("b");
        let _c = NamedDrop("c");
        // Drops: c, b, a
    }

    // ============================================
    // Drop with resource cleanup
    // ============================================

    struct TempFile {
        path: String,
    }

    impl Drop for TempFile {
        fn drop(&mut self) {
            println!("Cleaning up temp file: {}", self.path);
            // std::fs::remove_file(&self.path).ok();
        }
    }

    let _file = TempFile {
        path: "/tmp/test.txt".to_string(),
    };
}
```

---
# rc
`Rc<T>` (Reference Counted) enables shared ownership within a single thread. It tracks how many references point to a value and cleans up when the count reaches zero.

```rust
use std::rc::Rc;

fn main() {
    // ============================================
    // Basic Rc usage
    // ============================================

    let a = Rc::new(vec![1, 2, 3]);
    let b = Rc::clone(&a);
    let c = Rc::clone(&a);

    println!("a: {:?}", a);
    println!("b: {:?}", b);
    println!("c: {:?}", c);
    println!("Strong count: {}", Rc::strong_count(&a)); // 3

    drop(c);
    println!("After drop(c): {}", Rc::strong_count(&a)); // 2

    // ============================================
    // Rc with nested data
    // ============================================

    #[derive(Debug)]
    enum List {
        Cons(i32, Rc<List>),
        Nil,
    }

    use List::{Cons, Nil};

    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    let b = Cons(3, Rc::clone(&a));
    let c = Cons(4, Rc::clone(&a));

    println!("b: {:?}", b);
    println!("c: {:?}", c);
    println!("Rc count after creating b and c: {}", Rc::strong_count(&a)); // 3

    // ============================================
    // Rc::try_unwrap — convert to owned if count == 1
    // ============================================

    let rc = Rc::new(42);
    drop(b);
    drop(c);

    if let Ok(val) = Rc::try_unwrap(a) {
        println!("Unwrapped: {:?}", val);
    }

    // ============================================
    // Weak references (avoid cycles)
    // ============================================

    use std::rc::Weak;

    struct Node {
        value: i32,
        children: std::cell::RefCell<Vec<Rc<Node>>>,
        parent: std::cell::RefCell<Weak<Node>>,
    }

    let leaf = Rc::new(Node {
        value: 3,
        children: std::cell::RefCell::new(vec![]),
        parent: std::cell::RefCell::new(Weak::new()),
    });

    println!("Leaf parent: {:?}", leaf.parent.borrow().upgrade()); // None

    let branch = Rc::new(Node {
        value: 5,
        children: std::cell::RefCell::new(vec![Rc::clone(&leaf)]),
        parent: std::cell::RefCell::new(Weak::new()),
    });

    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);
    println!("Leaf parent: {:?}", leaf.parent.borrow().upgrade()); // Some
}
```

---
# Standard libraries
Key modules in Rust's standard library (`std`).

```rust
// ============================================
// std::env — environment variables
// ============================================

fn demo_env() {
    for (key, value) in std::env::vars() {
        println!("{}: {}", key, value);
    }

    match std::env::var("HOME") {
        Ok(val) => println!("HOME: {}", val),
        Err(e) => println!("No HOME: {}", e),
    }

    println!("Current dir: {:?}", std::env::current_dir().unwrap());
    println!("Temp dir: {:?}", std::env::temp_dir());
}

// ============================================
// std::fs — file system operations
// ============================================

fn demo_fs() {
    // Read entire file
    // let content = std::fs::read_to_string("file.txt").unwrap();

    // Write entire file
    // std::fs::write("output.txt", "hello").unwrap();

    // Read directory
    for entry in std::fs::read_dir(".").unwrap() {
        let entry = entry.unwrap();
        println!("{:?}", entry.path());
    }

    // Create directory
    // std::fs::create_dir_all("nested/path").unwrap();

    // Copy / remove
    // std::fs::copy("src", "dst").unwrap();
    // std::fs::remove_file("file.txt").unwrap();
}

// ============================================
// std::io — input/output
// ============================================

use std::io::{self, BufRead, Write, BufReader};

fn demo_io() {
    // Read from stdin line by line
    // let stdin = io::stdin();
    // for line in stdin.lock().lines() {
    //     println!("Got: {}", line.unwrap());
    // }

    // Write to stdout
    let mut stdout = io::stdout();
    stdout.write_all(b"Hello stdout\n").unwrap();

    // Read from a string as a reader
    let data = "line1\nline2\nline3";
    let reader = BufReader::new(data.as_bytes());
    for line in reader.lines() {
        println!("Line: {}", line.unwrap());
    }
}

// ============================================
// std::path — path manipulation
// ============================================

fn demo_path() {
    use std::path::{Path, PathBuf};

    let path = Path::new("/home/user/file.txt");
    println!("File name: {:?}", path.file_name());
    println!("Extension: {:?}", path.extension());
    println!("Parent: {:?}", path.parent());
    println!("Is absolute: {}", path.is_absolute());

    let mut buf = PathBuf::from("/tmp");
    buf.push("subdir");
    buf.push("file.txt");
    println!("PathBuf: {:?}", buf);
}

// ============================================
// std::time — time and duration
// ============================================

use std::time::{Duration, Instant, SystemTime};

fn demo_time() {
    let now = Instant::now();
    std::thread::sleep(Duration::from_millis(10));
    println!("Elapsed: {:?}", now.elapsed());

    let sys_now = SystemTime::now();
    println!("System time: {:?}", sys_now);

    let dur = Duration::from_secs(3600)
        + Duration::from_millis(500)
        + Duration::from_nanos(100);
    println!("Duration: {:?}", dur);
}

// ============================================
// std::process — spawning processes
// ============================================

use std::process::Command;

fn demo_process() {
    let output = Command::new("echo")
        .arg("Hello from child process")
        .output()
        .expect("Failed to execute");

    println!("stdout: {}", String::from_utf8_lossy(&output.stdout));
    println!("exit status: {}", output.status);
}

// ============================================
// Usage
// ============================================

fn main() {
    demo_env();
    demo_path();
    demo_time();
    demo_io();
    // demo_fs();
    // demo_process();
}
```

---
# async-await
Async/await enables writing non-blocking code that looks synchronous. Rust uses a poll-based async model with `Future`.

```rust
// Requires an async runtime like tokio or async-std
// #[tokio::main]
// async fn main() { ... }

// ============================================
// Basic async function
// ============================================

async fn fetch_data(url: &str) -> String {
    // Simulated async work
    format!("Data from {}", url)
}

// ============================================
// Async blocks
// ============================================

async fn demo_blocks() {
    let result = async {
        let a = 10;
        let b = 20;
        a + b
    }
    .await;

    println!("Block result: {}", result);
}

// ============================================
// Concurrent execution with join!
// ============================================

async fn demo_concurrent() {
    // With tokio:
    // let (a, b) = tokio::join!(
    //     fetch_data("http://example.com/1"),
    //     fetch_data("http://example.com/2"),
    // );
    // println!("{} and {}", a, b);

    // Sequential (not concurrent):
    let a = fetch_data("http://example.com/1").await;
    let b = fetch_data("http://example.com/2").await;
    println!("{} then {}", a, b);
}

// ============================================
// Async traits (Rust 1.75+ with return-position impl Trait in trait)
// ============================================

trait AsyncProcessor {
    async fn process(&self, data: &str) -> String;
}

struct SimpleProcessor;

impl AsyncProcessor for SimpleProcessor {
    async fn process(&self, data: &str) -> String {
        format!("Processed: {}", data)
    }
}

// ============================================
// Async streams (with async-stream crate or tokio-stream)
// ============================================

// async fn tick_stream() -> impl futures::Stream<Item = u64> {
//     async_stream::stream! {
//         let mut i = 0;
//         loop {
//             yield i;
//             i += 1;
//             tokio::time::sleep(std::time::Duration::from_secs(1)).await;
//         }
//     }
// }

// ============================================
// Select — race between futures
// ============================================

async fn demo_select() {
    // With tokio:
    // tokio::select! {
    //     val = fetch_data("url1") => println!("First: {}", val),
    //     val = fetch_data("url2") => println!("Second: {}", val),
    // }
}

// ============================================
// Manual Future implementation
// ============================================

use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct ReadyFuture<T>(Option<T>);

impl<T> Future for ReadyFuture<T> {
    type Output = T;

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {
        Poll::Ready(self.0.take().expect("polled after ready"))
    }
}

// ============================================
// Usage (requires runtime)
// ============================================

fn main() {
    // In a real project with tokio:
    // tokio::runtime::Runtime::new().unwrap().block_on(async {
    //     demo_blocks().await;
    //     demo_concurrent().await;
    // });

    // Without runtime, you can define async functions but not .await them
    println!("Async functions defined. Use a runtime to execute them.");
}
```

---
# Concurrency
Rust provides multiple approaches to concurrent programming: threads, channels, shared state, and async.

```rust
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

// ============================================
// Thread basics
// ============================================

fn demo_threads() {
    let mut handles = vec![];

    for i in 0..5 {
        let handle = thread::spawn(move || {
            println!("Thread {} started", i);
            thread::sleep(Duration::from_millis(100));
            println!("Thread {} done", i);
            i * 2
        });
        handles.push(handle);
    }

    for (i, handle) in handles.into_iter().enumerate() {
        let result = handle.join().unwrap();
        println!("Thread {} returned: {}", i, result);
    }
}

// ============================================
// Shared state with Arc + Mutex
// ============================================

fn demo_shared_state() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    println!("Counter: {}", *counter.lock().unwrap()); // 10
}

// ============================================
// Thread-local storage
// ============================================

thread_local! {
    static THREAD_ID: std::cell::Cell<u32> = const { std::cell::Cell::new(0) };
}

fn demo_thread_local() {
    let mut handles = vec![];

    for i in 0..3 {
        handles.push(thread::spawn(move || {
            THREAD_ID.with(|id| id.set(i));
            THREAD_ID.with(|id| println!("Thread {} has id {}", i, id.get()));
        }));
    }

    for h in handles {
        h.join().unwrap();
    }
}

// ============================================
// Scoped threads (no move required)
// ============================================

fn demo_scoped() {
    let mut a = vec![1, 2, 3];
    let mut x = 0;

    thread::scope(|s| {
        s.spawn(|| {
            println!("Hello from {:?}", a);
        });

        s.spawn(|| {
            x += 1;
            println!("x is now {}", x);
        });
    });

    println!("a: {:?}", a);
    println!("x: {}", x);
}

// ============================================
// Rayon-style parallel iterators (conceptual)
// ============================================

fn demo_parallel() {
    let nums: Vec<u64> = (0..1_000_000).collect();

    // With rayon: let sum: u64 = nums.par_iter().sum();
    let sum: u64 = nums.iter().sum(); // sequential version
    println!("Sum: {}", sum);
}

// ============================================
// Usage
// ============================================

fn main() {
    demo_threads();
    demo_shared_state();
    demo_thread_local();
    demo_scoped();
    demo_parallel();
}
```

---
# Threads
Threads are lightweight processes that run concurrently. Rust's `std::thread` module provides OS-level threads.

```rust
use std::thread;
use std::time::Duration;

fn main() {
    // ============================================
    // Spawning threads
    // ============================================

    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("Child: {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("Main: {}", i);
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap(); // wait for child

    // ============================================
    // Thread with move closure
    // ============================================

    let v = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        println!("Thread got vector: {:?}", v);
    });
    handle.join().unwrap();

    // ============================================
    // Thread naming
    // ============================================

    let builder = thread::Builder::new()
        .name("worker".to_string())
        .stack_size(32 * 1024); // 32KB

    let handle = builder
        .spawn(|| {
            println!(
                "Thread name: {:?}",
                thread::current().name()
            );
        })
        .unwrap();

    handle.join().unwrap();

    // ============================================
    // Thread yield / park
    // ============================================

    let child = thread::spawn(move || {
        thread::park(); // sleeps until unparked
        println!("Child unparked!");
    });

    thread::sleep(Duration::from_millis(100));
    child.thread_handle().map(|h| {
        // Note: thread::Thread::unpark requires the thread handle
    });
    child.join().unwrap();

    // ============================================
    // Thread::sleep vs thread::yield_now
    // ============================================

    thread::yield_now(); // give up current timeslice
    thread::sleep(Duration::from_millis(10)); // sleep for duration

    // ============================================
    // Available parallelism
    // ============================================

    match thread::available_parallelism() {
        Ok(n) => println!("Available CPUs: {}", n),
        Err(e) => println!("Could not determine: {}", e),
    }
}
```

---
# Future
A `Future` represents a value that may not be ready yet. It is the foundation of async Rust.

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};
use std::sync::{Arc, Mutex};

// ============================================
// What is a Future?
// ============================================

// A Future is a trait:
// pub trait Future {
//     type Output;
//     fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
// }
//
// Poll::Ready(T)  — value is available
// Poll::Pending   — value not ready, waker will notify when ready

// ============================================
// Simple custom Future
// ============================================

struct DelayedValue {
    ready: bool,
    value: Option<i32>,
}

impl Future for DelayedValue {
    type Output = i32;

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.ready {
            Poll::Ready(self.value.take().unwrap())
        } else {
            self.ready = true;
            Poll::Pending
        }
    }
}

// ============================================
// async fn desugars to a Future
// ============================================

async fn add(a: i32, b: i32) -> i32 {
    a + b
}

// This is roughly equivalent to:
fn add_future(a: i32, b: i32) -> impl Future<Output = i32> {
    async move { a + b }
}

// ============================================
// Pin — preventing moves of self-referential data
// ============================================

fn demo_pin() {
    let mut x = 42;
    let pin = Pin::new(&mut x);
    println!("Pinned value: {}", *pin);

    // Box::pin for heap-pinned data
    let boxed = Box::pin(async { 100 });
    // boxed can be polled
}

// ============================================
// Context and Waker
// ============================================

struct NotifyingFuture {
    count: u32,
}

impl Future for NotifyingFuture {
    type Output = u32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        self.count += 1;
        if self.count >= 3 {
            Poll::Ready(self.count)
        } else {
            cx.waker().wake_by_ref(); // schedule re-poll
            Poll::Pending
        }
    }
}

// ============================================
// JoinHandle (from thread::spawn) is also a Future in async runtimes
// ============================================

fn main() {
    demo_pin();

    // To actually poll futures you need an executor/runtime
    // e.g., tokio, async-std, smol, or a simple executor

    println!("Futures defined. Use an executor to poll them.");
}
```

---
# Streams
Streams are async iterators — they produce a sequence of values over time. Not in std; use `futures` crate or `tokio-stream`.

```rust
// Requires: futures = "0.3" or tokio-stream
// use futures::stream::{self, Stream, StreamExt};
// use futures::pin_mut;

// ============================================
// Stream trait (conceptual)
// ============================================

// pub trait Stream {
//     type Item;
//     fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>>;
// }

// ============================================
// Creating streams
// ============================================

// From iterator:
// let s = stream::iter(vec![1, 2, 3, 4, 5]);

// From async block:
// let s = stream::once(async { 42 });

// Repeated:
// let s = stream::repeat(1).take(5);

// ============================================
// Stream combinators
// ============================================

// async fn demo_stream_combinators() {
//     let s = stream::iter(vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
//
//     // map
//     let doubled: Vec<_> = s.map(|x| x * 2).collect().await;
//
//     // filter
//     let evens: Vec<_> = stream::iter(1..=10)
//         .filter(|x| futures::future::ready(x % 2 == 0))
//         .collect()
//         .await;
//
//     // take / skip
//     let first3: Vec<_> = stream::iter(1..=10).take(3).collect().await;
//
//     // fold
//     let sum = stream::iter(1..=10).fold(0, |acc, x| async move { acc + x }).await;
//
//     // chain
//     let chained: Vec<_> = stream::iter(vec![1,2])
//         .chain(stream::iter(vec![3,4]))
//         .collect().await;
//
//     // flatten (flatten nested streams)
//     let nested = stream::iter(vec![
//         stream::iter(vec![1, 2]),
//         stream::iter(vec![3, 4]),
//     ]);
//     let flat: Vec<_> = nested.flatten().collect().await;
// }

// ============================================
// Async read as stream (tokio)
// ============================================

// use tokio_stream::wrappers::LinesStream;
// use tokio::io::BufReader;

// async fn read_lines() {
//     let file = tokio::fs::File::open("input.txt").await.unwrap();
//     let reader = BufReader::new(file);
//     let lines = tokio::io::AsyncBufReadExt::lines(reader);
//     let stream = LinesStream::new(lines);
//
//     tokio::pin!(stream);
//     while let Some(line) = stream.next().await {
//         println!("Line: {}", line.unwrap());
//     }
// }

// ============================================
// Interval stream
// ============================================

// use tokio_stream::wrappers::IntervalStream;

// async fn tick_every_second() {
//     let mut interval = tokio::time::interval(Duration::from_secs(1));
//     let stream = IntervalStream::new(interval);
//
//     tokio::pin!(stream);
//     while let Some(_) = stream.next().await {
//         println!("Tick!");
//     }
// }

fn main() {
    println!("Streams require an async runtime and the futures/tokio-stream crate.");
    println!("Key methods: .next().await, .collect().await, .map(), .filter(), .fold()");
}
```

---
# oop
Rust is not an OOP language but supports OOP patterns through structs, traits, and composition.

```rust
// ============================================
// Encapsulation — private fields, public API
// ============================================

mod encapsulated {
    pub struct AveragedCollection {
        list: Vec<i32>,
        average: f64,
    }

    impl AveragedCollection {
        pub fn new() -> Self {
            AveragedCollection {
                list: vec![],
                average: 0.0,
            }
        }

        pub fn add(&mut self, value: i32) {
            self.list.push(value);
            self.update_average();
        }

        pub fn remove(&mut self) -> Option<i32> {
            let result = self.list.pop();
            match result {
                Some(value) => {
                    self.update_average();
                    Some(value)
                }
                None => None,
            }
        }

        pub fn average(&self) -> f64 {
            self.average
        }

        fn update_average(&mut self) {
            let total: i32 = self.list.iter().sum();
            self.average = total as f64 / self.list.len() as f64;
        }
    }
}

// ============================================
// Inheritance via traits (composition over inheritance)
// ============================================

trait Drawable {
    fn draw(&self);
    fn bounding_box(&self) -> (f64, f64, f64, f64);

    // Default method (like an inherited implementation)
    fn render(&self) {
        self.draw();
        println!("Rendered at {:?}", self.bounding_box());
    }
}

struct Circle {
    x: f64,
    y: f64,
    radius: f64,
}

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle at ({}, {})", self.x, self.y);
    }

    fn bounding_box(&self) -> (f64, f64, f64, f64) {
        (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )
    }
}

struct Rectangle {
    x: f64,
    y: f64,
    width: f64,
    height: f64,
}

impl Drawable for Rectangle {
    fn draw(&self) {
        println!("Drawing rectangle at ({}, {})", self.x, self.y);
    }

    fn bounding_box(&self) -> (f64, f64, f64, f64) {
        (self.x, self.y, self.x + self.width, self.y + self.height)
    }
}

// ============================================
// Polymorphism via trait objects
// ============================================

fn render_all(drawables: &[&dyn Drawable]) {
    for d in drawables {
        d.render();
    }
}

// ============================================
// Composition (preferred over inheritance in Rust)
// ============================================

struct Position {
    x: f64,
    y: f64,
}

struct Size {
    width: f64,
    height: f64,
}

struct GameObject {
    position: Position,
    size: Size,
    name: String,
}

impl GameObject {
    fn new(name: &str, x: f64, y: f64, w: f64, h: f64) -> Self {
        GameObject {
            position: Position { x, y },
            size: Size { width: w, height: h },
            name: name.to_string(),
        }
    }
}

// ============================================
// Usage
// ============================================

fn main() {
    let mut collection = encapsulated::AveragedCollection::new();
    collection.add(10);
    collection.add(20);
    collection.add(30);
    println!("Average: {}", collection.average());

    let circle = Circle { x: 0.0, y: 0.0, radius: 5.0 };
    let rect = Rectangle { x: 10.0, y: 10.0, width: 20.0, height: 15.0 };

    render_all(&[&circle, &rect]);

    let obj = GameObject::new("Player", 0.0, 0.0, 32.0, 32.0);
    println!("Object '{}' at ({}, {})", obj.name, obj.position.x, obj.position.y);
}
```

---
# Trait-objects
Trait objects enable dynamic dispatch — calling methods on values of different types through a common interface at runtime.

```rust
// ============================================
// Trait object syntax
// ============================================

trait Draw {
    fn draw(&self);
}

struct Button;
struct TextField;
struct SelectBox;

impl Draw for Button {
    fn draw(&self) { println!("Drawing a button"); }
}

impl Draw for TextField {
    fn draw(&self) { println!("Drawing a text field"); }
}

impl Draw for SelectBox {
    fn draw(&self) { println!("Drawing a select box"); }
}

// ============================================
// Using trait objects in collections
// ============================================

fn main() {
    let components: Vec<Box<dyn Draw>> = vec![
        Box::new(Button),
        Box::new(TextField),
        Box::new(SelectBox),
    ];

    for component in &components {
        component.draw();
    }

    // ============================================
    // Trait objects as function parameters
    // ============================================

    fn run_gui(components: &[&dyn Draw]) {
        for c in components {
            c.draw();
        }
    }

    run_gui(&[&Button, &TextField, &SelectBox]);

    // ============================================
    // &dyn Trait vs Box<dyn Trait>
    // ============================================

    // &dyn Draw — borrowed, no allocation
    // Box<dyn Draw> — owned, heap allocated
    // Rc<dyn Draw> — shared ownership

    let button = Button;
    let drawable: &dyn Draw = &button;
    drawable.draw();

    // ============================================
    // Trait objects with multiple traits (not directly supported)
    // Use a supertrait or wrapper
    // ============================================

    trait DebugDraw: Draw + std::fmt::Debug {}
    impl DebugDraw for Button {}
    impl DebugDraw for TextField {}
    impl DebugDraw for SelectBox {}

    // Now you can use: &dyn DebugDraw

    // ============================================
    // Object safety rules
    // ============================================

    // A trait is object-safe if:
    // 1. It does not return Self
    // 2. It has no generic methods
    // 3. It does not require Self: Sized

    // NOT object-safe:
    // trait NotObjectSafe {
    //     fn clone(&self) -> Self;           // returns Self
    //     fn generic<T>(&self, x: T);        // generic method
    // }

    // Object-safe:
    trait Cloneable {
        fn clone_box(&self) -> Box<dyn Cloneable>;
    }

    impl Cloneable for Button {
        fn clone_box(&self) -> Box<dyn Cloneable> {
            Box::new(Button)
        }
    }

    // ============================================
    // Dynamic vs static dispatch
    // ============================================

    // Static (monomorphized) — compile-time, faster:
    fn draw_static<T: Draw>(item: &T) {
        item.draw();
    }

    // Dynamic (trait object) — runtime, flexible:
    fn draw_dynamic(item: &dyn Draw) {
        item.draw();
    }

    draw_static(&Button);
    draw_dynamic(&Button);
}
```

---
# External-Crates(rand,rayon,serde,chrono,regex)
Commonly used external crates in Rust projects.

```rust
// ============================================
// rand — random number generation
// ============================================

// use rand::Rng;

fn demo_rand() {
    // let mut rng = rand::thread_rng();

    // Random integer in range
    // let n: i32 = rng.gen_range(1..=100);

    // Random float
    // let f: f64 = rng.gen_range(0.0..1.0);

    // Random boolean
    // let b: bool = rng.gen();

    // Random element from slice
    // let choices = [1, 2, 3, 4, 5];
    // let pick = rng.choice(&choices);

    // Shuffle
    // let mut nums = vec![1, 2, 3, 4, 5];
    // nums.shuffle(&mut rng);

    println!("rand: use rand::Rng trait for .gen_range(), .gen(), .choice(), .shuffle()");
}

// ============================================
// rayon — data parallelism
// ============================================

// use rayon::prelude::*;

fn demo_rayon() {
    // Parallel iterator
    // let sum: i32 = (1..1_000_000).into_par_iter().sum();

    // Parallel map
    // let doubled: Vec<_> = vec![1,2,3,4,5].par_iter().map(|x| x * 2).collect();

    // Parallel filter
    // let evens: Vec<_> = (0..100).into_par_iter().filter(|x| x % 2 == 0).collect();

    // Parallel sort
    // let mut v = vec![5, 3, 1, 4, 2];
    // v.par_sort();

    println!("rayon: use .par_iter(), .into_par_iter(), .par_sort(), .par_bridge()");
}

// ============================================
// serde — serialization/deserialization
// ============================================

// use serde::{Serialize, Deserialize};

fn demo_serde() {
    // #[derive(Serialize, Deserialize, Debug)]
    // struct User {
    //     name: String,
    //     age: u32,
    //     #[serde(default)]
    //     active: bool,
    // }

    // Serialize to JSON
    // let user = User { name: "Alice".into(), age: 30, active: true };
    // let json = serde_json::to_string(&user).unwrap();

    // Deserialize from JSON
    // let parsed: User = serde_json::from_str(&json).unwrap();

    // Serialize to TOML, YAML, etc. with respective crates

    println!("serde: derive Serialize/Deserialize, use serde_json for JSON");
}

// ============================================
// chrono — date and time
// ============================================

// use chrono::{DateTime, Utc, Local, Duration};

fn demo_chrono() {
    // Current time
    // let now: DateTime<Utc> = Utc::now();

    // Parse from string
    // let dt = "2024-01-15T10:30:00Z".parse::<DateTime<Utc>>().unwrap();

    // Arithmetic
    // let tomorrow = Utc::now() + Duration::days(1);
    // let yesterday = Utc::now() - Duration::days(1);

    // Formatting
    // println!("{}", now.format("%Y-%m-%d %H:%M:%S"));

    // Timezone conversion
    // let local: DateTime<Local> = now.with_timezone(&Local);

    println!("chrono: use Utc::now(), Duration, DateTime, .format()");
}

// ============================================
// regex — regular expressions
// ============================================

// use regex::Regex;

fn demo_regex() {
    // let re = Regex::new(r"^\d{4}-\d{2}-\d{2}$").unwrap();

    // Match
    // assert!(re.is_match("2024-01-15"));

    // Find
    // if let Some(m) = re.find("Date: 2024-01-15") {
    //     println!("Found: {}", m.as_str());
    // }

    // Captures
    // let re = Regex::new(r"(\d{4})-(\d{2})-(\d{2})").unwrap();
    // let caps = re.captures("2024-01-15").unwrap();
    // println!("Year: {}, Month: {}, Day: {}", &caps[1], &caps[2], &caps[3]);

    // Replace
    // let result = re.replace_all("2024-01-15 and 2023-12-01", "DATE");

    // Find all
    // for mat in re.find_iter("2024-01-15 2023-12-01") {
    //     println!("{}", mat.as_str());
    // }

    println!("regex: use Regex::new(), .is_match(), .find(), .captures(), .replace_all()");
}

// ============================================
// Usage
// ============================================

fn main() {
    demo_rand();
    demo_rayon();
    demo_serde();
    demo_chrono();
    demo_regex();
}
```

---
# oo
Object-oriented design patterns in Rust using composition, traits, and generics.

```rust
// ============================================
// Factory pattern
// ============================================

trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &str;
}

struct Circle { radius: f64 }
struct Square { side: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
    fn name(&self) -> &str { "Circle" }
}

impl Shape for Square {
    fn area(&self) -> f64 { self.side * self.side }
    fn name(&self) -> &str { "Square" }
}

struct ShapeFactory;

impl ShapeFactory {
    fn create(kind: &str, size: f64) -> Box<dyn Shape> {
        match kind {
            "circle" => Box::new(Circle { radius: size }),
            "square" => Box::new(Square { side: size }),
            _ => panic!("Unknown shape"),
        }
    }
}

// ============================================
// Builder pattern
// ============================================

#[derive(Debug)]
struct HttpRequest {
    method: String,
    url: String,
    headers: Vec<(String, String)>,
    body: Option<String>,
}

struct HttpRequestBuilder {
    method: String,
    url: String,
    headers: Vec<(String, String)>,
    body: Option<String>,
}

impl HttpRequestBuilder {
    fn new(method: &str, url: &str) -> Self {
        HttpRequestBuilder {
            method: method.to_string(),
            url: url.to_string(),
            headers: vec![],
            body: None,
        }
    }

    fn header(mut self, key: &str, value: &str) -> Self {
        self.headers.push((key.to_string(), value.to_string()));
        self
    }

    fn body(mut self, body: &str) -> Self {
        self.body = Some(body.to_string());
        self
    }

    fn build(self) -> HttpRequest {
        HttpRequest {
            method: self.method,
            url: self.url,
            headers: self.headers,
            body: self.body,
        }
    }
}

// ============================================
// Strategy pattern
// ============================================

trait SortStrategy {
    fn sort(&self, data: &mut Vec<i32>);
}

struct QuickSort;
struct BubbleSort;

impl SortStrategy for QuickSort {
    fn sort(&self, data: &mut Vec<i32>) {
        data.sort();
    }
}

impl SortStrategy for BubbleSort {
    fn sort(&self, data: &mut Vec<i32>) {
        let n = data.len();
        for i in 0..n {
            for j in 0..n - i - 1 {
                if data[j] > data[j + 1] {
                    data.swap(j, j + 1);
                }
            }
        }
    }
}

struct Sorter {
    strategy: Box<dyn SortStrategy>,
}

impl Sorter {
    fn new(strategy: Box<dyn SortStrategy>) -> Self {
        Sorter { strategy }
    }

    fn set_strategy(&mut self, strategy: Box<dyn SortStrategy>) {
        self.strategy = strategy;
    }

    fn sort(&self, data: &mut Vec<i32>) {
        self.strategy.sort(data);
    }
}

// ============================================
// Observer pattern
// ============================================

use std::cell::RefCell;

struct EventPublisher {
    listeners: RefCell<Vec<Box<dyn Fn(&str)>>>,
}

impl EventPublisher {
    fn new() -> Self {
        EventPublisher {
            listeners: RefCell::new(vec![]),
        }
    }

    fn subscribe<F: Fn(&str) + 'static>(&self, listener: F) {
        self.listeners.borrow_mut().push(Box::new(listener));
    }

    fn publish(&self, event: &str) {
        for listener in self.listeners.borrow().iter() {
            listener(event);
        }
    }
}

// ============================================
// Usage
// ============================================

fn main() {
    // Factory
    let shapes = vec![
        ShapeFactory::create("circle", 5.0),
        ShapeFactory::create("square", 4.0),
    ];
    for s in &shapes {
        println!("{} area: {}", s.name(), s.area());
    }

    // Builder
    let request = HttpRequestBuilder::new("GET", "https://api.example.com")
        .header("Content-Type", "application/json")
        .header("Authorization", "Bearer token")
        .body("{\"key\": \"value\"}")
        .build();
    println!("{:?}", request);

    // Strategy
    let mut sorter = Sorter::new(Box::new(QuickSort));
    let mut data = vec![5, 3, 1, 4, 2];
    sorter.sort(&mut data);
    println!("Sorted: {:?}", data);

    // Observer
    let publisher = EventPublisher::new();
    publisher.subscribe(|e| println!("Listener 1: {}", e));
    publisher.subscribe(|e| println!("Listener 2: {}", e));
    publisher.publish("user_login");
}
```

---
# oo-Design-Paterns
Common design patterns implemented in Rust.

```rust
// ============================================
// Singleton (using OnceLock)
// ============================================

use std::sync::OnceLock;

struct Config {
    database_url: String,
    max_connections: u32,
}

impl Config {
    fn global() -> &'static Config {
        static INSTANCE: OnceLock<Config> = OnceLock::new();
        INSTANCE.get_or_init(|| Config {
            database_url: "postgres://localhost/db".to_string(),
            max_connections: 10,
        })
    }
}

// ============================================
// Adapter pattern
// ============================================

trait Target {
    fn request(&self) -> String;
}

struct Adaptee;

impl Adaptee {
    fn specific_request(&self) -> String {
        "Adaptee response".to_string()
    }
}

struct Adapter {
    adaptee: Adaptee,
}

impl Target for Adapter {
    fn request(&self) -> String {
        self.adaptee.specific_request()
    }
}

// ============================================
// Decorator pattern
// ============================================

trait Component {
    fn operation(&self) -> String;
}

struct ConcreteComponent;

impl Component for ConcreteComponent {
    fn operation(&self) -> String {
        "ConcreteComponent".to_string()
    }
}

struct LoggingDecorator<T: Component> {
    inner: T,
}

impl<T: Component> Component for LoggingDecorator<T> {
    fn operation(&self) -> String {
        let result = self.inner.operation();
        format!("[LOG] {}", result)
    }
}

// ============================================
// Repository pattern
// ============================================

#[derive(Debug)]
struct User {
    id: u64,
    name: String,
}

trait UserRepository {
    fn find_by_id(&self, id: u64) -> Option<User>;
    fn save(&mut self, user: User);
    fn delete(&mut self, id: u64);
}

struct InMemoryUserRepo {
    users: std::collections::HashMap<u64, User>,
    next_id: u64,
}

impl UserRepository for InMemoryUserRepo {
    fn find_by_id(&self, id: u64) -> Option<User> {
        self.users.get(&id).cloned()
    }

    fn save(&mut self, user: User) {
        self.users.insert(user.id, user);
    }

    fn delete(&mut self, id: u64) {
        self.users.remove(&id);
    }
}

// ============================================
// Command pattern
// ============================================

trait Command {
    fn execute(&self);
    fn undo(&self);
}

struct LightOnCommand;
struct LightOffCommand;

impl Command for LightOnCommand {
    fn execute(&self) { println!("Light ON"); }
    fn undo(&self) { println!("Light OFF (undo)"); }
}

impl Command for LightOffCommand {
    fn execute(&self) { println!("Light OFF"); }
    fn undo(&self) { println!("Light ON (undo)"); }
}

struct RemoteControl {
    last_command: Option<Box<dyn Command>>,
}

impl RemoteControl {
    fn new() -> Self {
        RemoteControl { last_command: None }
    }

    fn press(&mut self, cmd: Box<dyn Command>) {
        cmd.execute();
        self.last_command = Some(cmd);
    }

    fn undo(&self) {
        if let Some(cmd) = &self.last_command {
            cmd.undo();
        }
    }
}

// ============================================
// Usage
// ============================================

fn main() {
    // Singleton
    let config = Config::global();
    println!("DB: {}, Max connections: {}", config.database_url, config.max_connections);

    // Adapter
    let adapter = Adapter { adaptee: Adaptee };
    println!("Adapter: {}", adapter.request());

    // Decorator
    let component = ConcreteComponent;
    let decorated = LoggingDecorator { inner: component };
    println!("Decorated: {}", decorated.operation());

    // Repository
    let mut repo = InMemoryUserRepo {
        users: std::collections::HashMap::new(),
        next_id: 1,
    };
    repo.save(User { id: 1, name: "Alice".to_string() });
    println!("Find: {:?}", repo.find_by_id(1));

    // Command
    let mut remote = RemoteControl::new();
    remote.press(Box::new(LightOnCommand));
    remote.undo();
}
```

---
# Paterns
Common Rust patterns and idioms.

```rust
use std::collections::HashMap;

// ============================================
// Newtype pattern
// ============================================

struct Meters(f64);
struct Feet(f64);

impl Meters {
    fn to_feet(&self) -> Feet { Feet(self.0 * 3.28084) }
}

impl Feet {
    fn to_meters(&self) -> Meters { Meters(self.0 / 3.28084) }
}

// ============================================
// RAII (Resource Acquisition Is Initialization)
// ============================================

struct LockGuard {
    resource_id: u32,
}

impl LockGuard {
    fn acquire(id: u32) -> Self {
        println!("Acquiring resource {}", id);
        LockGuard { resource_id: id }
    }
}

impl Drop for LockGuard {
    fn drop(&mut self) {
        println!("Releasing resource {}", self.resource_id);
    }
}

// ============================================
// Typestate pattern
// ============================================

struct Draft;
struct Reviewed;
struct Published;

struct Article<State> {
    content: String,
    _state: std::marker::PhantomData<State>,
}

impl Article<Draft> {
    fn new(content: &str) -> Self {
        Article {
            content: content.to_string(),
            _state: std::marker::PhantomData,
        }
    }

    fn review(self) -> Article<Reviewed> {
        Article {
            content: self.content,
            _state: std::marker::PhantomData,
        }
    }
}

impl Article<Reviewed> {
    fn publish(self) -> Article<Published> {
        Article {
            content: self.content,
            _state: std::marker::PhantomData,
        }
    }
}

impl Article<Published> {
    fn content(&self) -> &str {
        &self.content
    }
}

// ============================================
// Error handling patterns
// ============================================

fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

// Using ? operator
fn compute() -> Result<f64, String> {
    let x = divide(10.0, 2.0)?;
    let y = divide(x, 0.0)?; // returns early with Err
    Ok(y)
}

// ============================================
// Borrowing pattern — entry API
// ============================================

fn word_count(text: &str) -> HashMap<String, u32> {
    let mut counts = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word.to_string()).or_insert(0) += 1;
    }
    counts
}

// ============================================
// Smart pointer pattern
// ============================================

struct SmartPtr<T> {
    data: T,
}

impl<T> SmartPtr<T> {
    fn new(data: T) -> Self {
        SmartPtr { data }
    }
}

impl<T> std::ops::Deref for SmartPtr<T> {
    type Target = T;
    fn deref(&self) -> &T { &self.data }
}

impl<T> std::ops::DerefMut for SmartPtr<T> {
    fn deref_mut(&mut self) -> &mut T { &mut self.data }
}

// ============================================
// Usage
// ============================================

fn main() {
    // Newtype
    let m = Meters(10.0);
    let f = m.to_feet();
    println!("{} meters = {:?} feet", m.0, f.0);

    // RAII
    {
        let _guard = LockGuard::acquire(42);
        println!("Working with resource...");
    } // automatically released

    // Typestate
    let article = Article::new("Draft content")
        .review()
        .publish();
    println!("Published: {}", article.content());

    // Error handling
    match divide(10.0, 0.0) {
        Ok(v) => println!("Result: {}", v),
        Err(e) => println!("Error: {}", e),
    }

    // Entry API
    let counts = word_count("the quick brown fox the fox");
    println!("Word counts: {:?}", counts);
}
```

---
# Refutability
Refutability determines whether a pattern match can fail. Refutable patterns can fail; irrefutable patterns always match.

```rust
// ============================================
// Irrefutable patterns — cannot fail
// ============================================

fn demo_irrefutable() {
    // let, function parameters, for loops require irrefutable patterns
    let x = 5;           // always matches
    let (a, b) = (1, 2); // always matches
    let [x, y] = [1, 2]; // always matches

    println!("x={}, a={}, b={}, [{}, {}]", x, a, b, x, y);
}

// ============================================
// Refutable patterns — can fail
// ============================================

fn demo_refutable() {
    // if let, while let, match arms accept refutable patterns

    let option: Option<i32> = Some(5);

    // if let — refutable
    if let Some(x) = option {
        println!("Got: {}", x);
    }

    // while let — refutable
    let mut stack = vec![1, 2, 3];
    while let Some(top) = stack.pop() {
        println!("Popped: {}", top);
    }

    // match arms — each arm is refutable
    let x = Some(5);
    match x {
        Some(n) if n > 10 => println!("Big number: {}", n),
        Some(n) => println!("Small number: {}", n),
        None => println!("Nothing"),
    }
}

// ============================================
// Where each pattern type is allowed
// ============================================

fn demo_contexts() {
    // let — MUST be irrefutable
    let x = 5;

    // if let — refutable
    let opt: Option<i32> = Some(3);
    if let Some(v) = opt {
        println!("if let: {}", v);
    }

    // let else — refutable with fallback
    let val: Option<i32> = None;
    let Some(v) = val else {
        println!("let else fallback");
        return;
    };

    // for — irrefutable (uses ref pattern internally)
    for i in 0..3 {
        println!("for: {}", i);
    }

    // fn params — irrefutable
    fn take_tuple((a, b): (i32, i32)) {
        println!("tuple params: {}, {}", a, b);
    }
    take_tuple((1, 2));

    // closure params — irrefutable
    let add = |(a, b): (i32, i32)| a + b;
    println!("closure: {}", add((3, 4)));
}

// ============================================
// Refutable pattern in wrong context (compile error)
// ============================================

// let Some(x) = Some(5); // ERROR: refutable pattern in let
// if let x = 5 { }       // WARNING: irrefutable in if let (useless)

// ============================================
// Usage
// ============================================

fn main() {
    demo_irrefutable();
    demo_refutable();
    demo_contexts();
}
```

---
# Unsafe-Rust
Unsafe Rust allows operations the compiler cannot verify for safety. It does not disable the borrow checker — it just relaxes certain checks.

```rust
// ============================================
// Dereferencing raw pointers
// ============================================

fn demo_raw_pointers() {
    let mut num = 5;

    // Create raw pointers
    let r1 = &num as *const i32;
    let r2 = &mut num as *mut i32;

    // Dereference in unsafe block
    unsafe {
        println!("r1 = {}", *r1);
        *r2 = 10;
        println!("r2 = {}", *r2);
    }

    // Raw pointers can be null
    let null_ptr: *const i32 = std::ptr::null();
    unsafe {
        if !null_ptr.is_null() {
            println!("{}", *null_ptr);
        }
    }

    // Raw pointers can dangle (but dereferencing is UB)
    let dangling: *const i32 = {
        let x = 42;
        &x as *const i32
    };
    // unsafe { println!("{}", *dangling); } // UB! Don't do this.
}

// ============================================
// Calling unsafe functions
// ============================================

unsafe fn dangerous() {
    println!("This function is unsafe!");
}

fn demo_unsafe_fn() {
    unsafe {
        dangerous();
    }
}

// ============================================
// Creating a safe abstraction over unsafe code
// ============================================

fn split_at_mut(slice: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    assert!(mid <= slice.len());

    let len = slice.len();
    let ptr = slice.as_mut_ptr();

    unsafe {
        (
            std::slice::from_raw_parts_mut(ptr, mid),
            std::slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

// ============================================
// extern "C" — calling C code (FFI)
// ============================================

extern "C" {
    fn abs(input: i32) -> i32;
}

fn demo_ffi() {
    unsafe {
        println!("Absolute value of -3: {}", abs(-3));
    }
}

// Exporting Rust functions for C to call
#[no_mangle]
pub extern "C" fn call_from_c() {
    println!("Called from C!");
}

// ============================================
// Unsafe traits
// ============================================

unsafe trait Foo {
    fn foo(&self);
}

struct Bar;

unsafe impl Foo for Bar {
    fn foo(&self) {
        println!("unsafe trait impl");
    }
}

// ============================================
// std::mem — unsafe memory operations
// ============================================

fn demo_mem() {
    let mut x = 5;
    let y = &mut x as *mut i32;

    unsafe {
        // Read without taking a reference
        let val = std::ptr::read(y);
        println!("Read: {}", val);

        // Write without taking a reference
        std::ptr::write(y, 10);
        println!("After write: {}", x);

        // Swap
        let mut a = 1;
        let mut b = 2;
        std::mem::swap(&mut a, &mut b);
        println!("Swapped: a={}, b={}", a, b);

        // Transmute (reinterpret bits — extremely dangerous)
        let f: f32 = 1.0;
        let bits: u32 = std::mem::transmute(f);
        println!("Float bits: {:032b}", bits);
    }
}

// ============================================
// Union (unsafe to access)
// ============================================

#[repr(C)]
union MyUnion {
    f1: u32,
    f2: f32,
}

fn demo_union() {
    let u = MyUnion { f1: 42 };
    unsafe {
        println!("f1 = {}", u.f1);
    }

    let u = MyUnion { f2: 3.14 };
    unsafe {
        println!("f2 = {}", u.f2);
    }
}

// ============================================
// Unsafe blocks in safe functions
// ============================================

fn safe_wrapper() -> i32 {
    let x = 5;
    let ptr = &x as *const i32;
    // This is safe because we know ptr is valid
    unsafe { *ptr }
}

// ============================================
// Usage
// ============================================

fn main() {
    demo_raw_pointers();
    demo_unsafe_fn();

    let v = &mut [1, 2, 3, 4, 5];
    let (left, right) = split_at_mut(v, 2);
    println!("Left: {:?}, Right: {:?}", left, right);

    demo_ffi();
    demo_mem();
    demo_union();

    println!("Safe wrapper: {}", safe_wrapper());

    let bar = Bar;
    bar.foo();
}
```
