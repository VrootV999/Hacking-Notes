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
        [3, _ , tail @ ..] => println!("the other elements after the third value is", tail), //can't use more than one ..
        [3, name @ ..] => println!("the other elements from the second ones {}", name)
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
```rust

```

---
# Generics
```rust

```

---
# Interior-Mutability

---
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
