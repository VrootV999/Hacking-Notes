# Rust Practice Questions
## Structs, Enums, Tuples, Match, impl

---

### 🔹 Structs

**1.** What are the three kinds of structs in Rust? Give a one-line example of each.
struct Player{}; struct RGBA(i8,i8,i8,f32);

**2.** How does struct update syntax (`..instance`) work? What gets copied vs moved?


**3.** Can a struct contain a direct reference to itself (e.g., `next: &Node`)? Why or why not? How do you work around it?
use method and in a fuction can't call itself

**4.** What does `#[derive(Debug, Clone, PartialEq)]` actually generate? When would you implement one manually instead?
Debug lets you debug using {:#?} or {:?}
Clone lets you clone the struct

**5.** How do you define a generic struct? Show the syntax for a struct with two type parameters and one const generic parameter.

---

### 🔹 Enums

**6.** How can enum variants hold different types and amounts of data? Show an enum with a unit variant, a tuple variant, and a struct variant.

**7.** What is the memory layout of a Rust enum? How does it differ from a C `enum`?

**8.** Why don't `Option<T>` and `Result<T, E>` need to be imported? What are their variants and typical use cases?

**9.** Can you attach methods to an enum? Show how to implement a method that matches on `self` and returns different values per variant.

**10.** What is an "exhaustive match" on an enum? What happens if you forget a variant?

---

### 🔹 Tuples

**11.** How do you access elements in a tuple? What is the indexing syntax? Can you use variables as indices?

**12.** What is the unit type `()`? How is it related to tuples? When does a function implicitly return it?

**13.** Show how to destructure a nested tuple like `((i32, &str), bool, char)` into named variables.

**14.** What is the difference between a tuple `(i32, String)` and a tuple struct `struct Pair(i32, String)`?

**15.** Can tuples be mutable? How do you mutate a specific element inside a tuple?

---

### 🔹 Match

**16.** Why must `match` arms be exhaustive? What compiler error do you get if they aren't? How do you handle the "catch-all" case?

**17.** How do you bind a matched value to a variable inside an arm? Show the `@` (bind-and-test) syntax.

**18.** What are match guards? Show an example using `if` inside a match arm.

**19.** How does `match` handle references? Do you need to explicitly dereference, or does Rust do it automatically? Show an example.

**20.** What is the difference between `match`, `if let`, and `while let`? When would you choose one over the others?

---

### 🔹 impl

**21.** What is the difference between a **method** and an **associated function**? How do you call each?

**22.** Explain the difference between `self`, `&self`, and `&mut self`. What happens to ownership in each case?

**23.** Can you have multiple `impl` blocks for the same type? Why would you split them?

**24.** How do you write an `impl` block for a generic struct? Show the syntax for `impl<T> MyStruct<T>`.

**25.** What is the `Self` type inside an `impl` block? How does it differ from `self`? Show an example where `Self` is useful.

---

### 🔹 Combined / Advanced

**26.** How would you implement a builder-pattern method that returns a modified struct without consuming the original?

**27.** Show how to pattern match on a struct inside `match`, including: field renaming, ignoring fields with `..`, and matching nested tuples.

**28.** Can an enum variant contain a struct? Can a struct contain an enum? Show both and explain how you'd match on them.

**29.** How does `match` behave differently on tuple structs vs regular structs vs enums? Show one example of each.

**30.** What happens if you try to match on a reference to an enum (e.g., `match &my_enum`)? How does Rust's pattern matching handle the reference automatically?

---

> Answer each question with code examples where applicable.
> You can answer in batches or all at once.
