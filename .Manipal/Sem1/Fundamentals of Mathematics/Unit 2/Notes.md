# Unit 2: Composite Function

> **Course:** Fundamentals of Mathematics — BCA Semester 1  
> **University:** Manipal University Jaipur (MUJ)  
> **Unit:** 2 — Composite Function

---

## Table of Contents

| # | Section | Topic |
|---|---------|-------|
| 1 | [Introduction](#1-introduction) | Recap of Unit 1 & motivation for Unit 2 |
| 1.1 | [Objectives](#11-objectives) | What you'll learn in this unit |
| 2 | [Composite Function](#2-composite-function) | Definition & step-by-step composition |
| 2.1 | [Properties of Composite Functions](#21-properties-of-composite-functions) | All 8 properties |
| 2.2 | [Real-world Applications](#22-real-world-applications) | Finance, physics & CS connection |
| 2.3 | [Problems](#23-problems) | 10 solved problems |
| 3 | [Operations on a Function](#3-operations-on-a-function) | Sum, difference, product, quotient |
| 4 | [Periodic Function](#4-periodic-function) | Period, frequency, amplitude, midline |
| 4.1 | [Properties of Even and Odd Functions](#41-properties-of-even-and-odd-functions) | Symmetry properties & their relation |
| 5 | [Summary](#5-summary) | Key takeaways |
| 6 | [Self-Assessment Questions](#6-self-assessment-questions--1) | SAQ–1 with answer key |
| 7 | [Terminal Questions](#7-terminal-questions) | Practice questions with answers |

---

## 1. Introduction

Unit 1 laid the groundwork for everything that follows in this course:

- It explored **relations** — connections between elements across different sets — supported by **pictorial diagrams** that make these abstract ideas visual and accessible.
- It clarified the distinctions between **domain, co-domain, and range**, which define the scope and output of mathematical interactions.
- It introduced **functions** as a special kind of relation that ensures a **unique output for every input**, along with an array of function types: constant, identity, polynomial, rational, modulus, signum, exponential, logarithmic, and greatest integer functions.
- It dissected types of relations (**reflexive, symmetric, transitive, equivalence**) and concepts like **one-to-one, onto functions, composite functions, inverses of functions, and binary operations**.

Unit 2 shifts the focus to **Composite Functions** — a concept that epitomises mathematical elegance and functional complexity:

- It mirrors the **layered nature of software development and algorithm design**, where functions and procedures are nested and combined to achieve sophisticated outcomes.
- The output of one function can seamlessly become the **input for another**, forming a new, more complex function — much like data passed through multiple layers of processing and transformation in real computer systems.
- Mastering composition helps students understand the **flow of data and logic within software systems**, making it easier to debug, optimise, and innovate.

> [!TIP]
> Recommended approach: start with the basics and ensure solid grasp of fundamental definitions before complex territory; use visual aids (diagrams, graphs); practise with varied examples; collaborate through group discussions; leverage online resources, simulations, and mathematical software.

### 1.1 Objectives

In this unit you will learn about:

- **Define** the concept of composite functions and their significance in mathematics and practical applications.
- **Explain** the process of creating composite functions and interpret the results.
- **Apply** composite functions to solve problems in various contexts, such as algorithm design, data analysis, and cryptography.
- **Analyse** the properties and behaviour of composite functions through mathematical operations and real-world examples.

---

## 2. Composite Function

### Definition

A **composite function** (also called a *composition of functions*) is a mathematical concept that involves **applying one function to the output of another function**. In other words, it is the process of using the result of one function as the **input** for another function. This creates a new function that encapsulates the **combined behaviour** of the two original functions.

Given two functions $f(x)$ and $g(x)$, the composite function $f(g(x))$ is formed by applying $g(x)$ to the input $x$ first, then applying $f(x)$ to that result. In notation:

$$f(g(x))$$

**Step-by-step breakdown:**

1. **Apply $g(x)$ to the input $x$:** substitute $x$ into the expression for $g(x)$ to get its output. For example, if $g(x) = x + 3$, then:
   $$g(x) = x + 3$$
2. **Apply $f(x)$ to the result of $g(x)$:** take the output of $g$ and feed it into $f$. If $f(x) = 2x$, then:
   $$f(g(x)) = f(x + 3) = 2(x + 3) = 2x + 6$$

---

### 2.1 Properties of Composite Functions

Understanding composite functions is fundamental in calculus and mathematics as a whole. Key properties:

| # | Property | Statement |
|:-|:---------|:----------|
| 1 | **Associativity** | The order of grouping does not affect the result: $(f \circ g) \circ h = f \circ (g \circ h)$ |
| 2 | **Identity Function** | $I(x) = x$ is the neutral element for composition: $f \circ I = I \circ f = f$ |
| 3 | **Distributive Property** | Composition distributes over addition, subtraction, and multiplication: $(f+g)\circ h = (f\circ h)+(g\circ h)$, $(f-g)\circ h = (f\circ h)-(g\circ h)$, $(f \cdot g)\circ h = (f\circ h)\cdot(g\circ h)$ |
| 4 | **Inverse Functions** | If $f$ has inverse $f^{-1}$, then $f \circ f^{-1} = I$ and $f^{-1} \circ f = I$ |
| 5 | **Domain and Range** | The domain of a composite is determined by the domain of the **innermost** function; the range by the range of the **outermost** function |
| 6 | **Not Commutative** | Order matters: in general $f \circ g \neq g \circ f$, unless $f$ and $g$ are inverses of each other |
| 7 | **Transitivity** | If $g \circ f$ and $h \circ g$ are defined, they can themselves be composed, leading to a new composite function |
| 8 | **Invertibility** | A composite function is invertible **if and only if** each component function is invertible; the inverse of a composite is the composite of the inverses in **reverse order** |

> [!WARNING] Source note
> In the official PDF, the formula printed under property 7 (Transitivity) appears garbled; the property is stated above in words as the text describes it.

#### Worked Example

Given $f(x) = 2x$ and $g(x) = x + 3$, find $f(g(x))$:

1. Apply $g(x)$ to the input: $g(x) = x + 3$
2. Apply $f(x)$ to the result: $f(g(x)) = f(x+3) = 2(x+3) = 2x + 6$

$$\therefore\; f(g(x)) = 2x + 6$$

Composite functions matter beyond pure mathematics: in programming they allow building complex processes from simpler ones — e.g., a sequence of data transformations in data processing, or encryption/decryption processes in cryptography.

---

### 2.2 Real-world Applications

- **Finance:** model the effects of multiple financial transactions applied successively.
- **Physics:** describe successive transformations of physical quantities.
- **Computer Science connection:** composite functions align with **function chaining**. By breaking tasks into smaller functions and composing them, programmers build **efficient and modular** solutions when designing algorithms and writing code.

---

### 2.3 Problems

> [!example] Problem 1
> Given $f(x) = 2x + 1$ and $g(x) = x^2$, find $f(g(x))$.
>
> - Apply $g(x)$ to $x$: $g(x) = x^2$
> - Apply $f(x)$ to $g(x)$: $f(g(x)) = f(x^2) = 2(x^2) + 1$
>
> $$\text{Ans: } f(g(x)) = 2x^2 + 1$$

> [!example] Problem 2
> Let $h(x) = 3x - 4$ and $k(x) = x^3$. Determine $h(k(x))$.
>
> - Apply $k(x)$ to $x$: $k(x) = x^3$
> - Apply $h(x)$ to $k(x)$: $h(k(x)) = h(x^3) = 3(x^3) - 4$
>
> $$\text{Ans: } h(k(x)) = 3x^3 - 4$$

> [!example] Problem 3
> Consider $f(x) = \sqrt{x}$ and $g(x) = 2x$. Find $f(g(x))$.
>
> - Apply $g(x)$ to $x$: $g(x) = 2x$
> - Apply $f(x)$ to $g(x)$: $f(g(x)) = f(2x) = \sqrt{2x}$
>
> $$\text{Ans: } f(g(x)) = \sqrt{2x}$$

> [!example] Problem 4
> Given $u(x) = x + 5$ and $v(x) = x^2 - 3x$. Calculate $v(u(x))$.
>
> - Apply $u(x)$ to $x$: $u(x) = x + 5$
> - Apply $v(x)$ to $u(x)$: $v(u(x)) = v(x+5) = (x+5)^2 - 3(x+5)$
>
> $$\text{Ans: } v(u(x)) = x^2 + 10x + 25 - 3x - 15 = x^2 + 7x + 10$$

> [!example] Problem 5
> If $m(x) = 2x$ and $n(x) = x - 3$, find $m(n(x))$.
>
> - Apply $n(x)$ to $x$: $n(x) = x - 3$
> - Apply $m(x)$ to $n(x)$: $m(n(x)) = m(x-3) = 2(x-3)$
>
> $$\text{Ans: } m(n(x)) = 2x - 6$$

> [!example] Problem 6
> Given $f(x) = x^2$ and $g(x) = 2x - 1$, determine $g(f(3))$.
>
> - Apply $f(x)$ to $3$: $f(3) = 3^2 = 9$
> - Apply $g(x)$ to $f(3)$: $g(f(3)) = g(9) = 2(9) - 1 = 18 - 1$
>
> $$\text{Ans: } g(f(3)) = 17$$

> [!example] Problem 7
> Consider $h(x) = \sqrt{x + 4}$ and $k(x) = 3x$. Calculate $h(k(2))$.
>
> - Apply $k(x)$ to $2$: $k(2) = 3(2) = 6$
> - Apply $h(x)$ to $k(2)$: $h(k(2)) = h(6) = \sqrt{6 + 4} = \sqrt{10}$
>
> $$\text{Ans: } h(k(2)) = \sqrt{10}$$

> [!example] Problem 8
> Given $f(x) = x^3$ and $g(x) = x + 2$, find $g(f(x))$.
>
> - Apply $f(x)$ to $x$: $f(x) = x^3$
> - Apply $g(x)$ to $f(x)$: $g(f(x)) = g(x^3) = x^3 + 2$
>
> $$\text{Ans: } g(f(x)) = x^3 + 2$$

> [!example] Problem 9
> Let $p(x) = x^2 + 1$ and $q(x) = 4x$. Determine $q(p(x))$.
>
> - Apply $p(x)$ to $x$: $p(x) = x^2 + 1$
> - Apply $q(x)$ to $p(x)$: $q(p(x)) = q(x^2 + 1) = 4(x^2 + 1)$
>
> $$\text{Ans: } q(p(x)) = 4x^2 + 4$$
>
> > [!WARNING]
> > The PDF's printed answer line shows $4x^2 + 4x + 4$, which contradicts its own working step $4(x^2 + 1)$. The correct expansion of $4(x^2+1)$ is $4x^2 + 4$.

> [!example] Problem 10
> Consider $r(x) = x - 2$ and $s(x) = x^2$. Calculate $s(r(x))$.
>
> - Apply $r(x)$ to $x$: $r(x) = x - 2$
> - Apply $s(x)$ to $r(x)$: $s(r(x)) = s(x-2) = (x-2)^2$
>
> $$\text{Ans: } s(r(x)) = x^2 - 4x + 4$$

---

## 3. Operations on a Function

Functions can be combined via addition, subtraction, multiplication, and division to create new functions — the **sum, difference, product, and quotient** of functions.

### 1. Sum of Functions

$$(f + g)(x) = f(x) + g(x)$$

> [!example]
> If $f(x) = 2x$ and $g(x) = 3x^2$, then $(f+g)(x) = 2x + 3x^2$.

### 2. Difference of Functions

$$(f - g)(x) = f(x) - g(x)$$

> [!example]
> If $f(x) = 5x$ and $g(x) = 2x^3$, then $(f-g)(x) = 5x - 2x^3$.

### 3. Product of Functions

$$(f \cdot g)(x) = f(x) \cdot g(x)$$

> [!example]
> If $f(x) = x^2$ and $g(x) = 3x$, then $(f \cdot g)(x) = x^2 \cdot 3x = 3x^3$.

### 4. Quotient of Functions

$$\left(\frac{f}{g}\right)(x) = \frac{f(x)}{g(x)}$$

defined where $g(x) \neq 0$.

> [!example]
> If $f(x) = 2x$ and $g(x) = x^2$, then $\left(\dfrac{f}{g}\right)(x) = \dfrac{2x}{x^2} = \dfrac{2}{x}$.

---

## 4. Periodic Function

A **periodic function** is a function that **repeats its values at regular intervals**, called *periods*. Its behaviour within each period is consistent. Periodic functions have widespread applications in physics, engineering, and signal processing.

### Key Concepts

| Concept | Description |
|:--------|:------------|
| **Period ($T$)** | Length of one complete cycle/repetition. Satisfies $f(x) = f(x + T)$ — values repeat with period $T$ |
| **Frequency ($f$)** | Number of cycles per unit interval; reciprocal of period: $f = \dfrac{1}{T}$ |
| **Amplitude** | Maximum absolute value of the function within one period; vertical distance from midline to highest/lowest point |
| **Midline** | Horizontal line representing the average/central value over a period; helps identify amplitude and see oscillation above/below it |

### Examples of Periodic Functions

1. **Sine and Cosine Functions:** $\sin(x)$ and $\cos(x)$ repeat every $2\pi$ units; used to model waveforms like sound and light waves.
2. **Square Wave:** alternates between two values, typically $1$ and $-1$; its period determines how often it switches between them.
3. **Sawtooth Wave:** rises linearly, then drops suddenly before repeating; its period defines the rise-and-fall cycle length.
4. **Triangular Wave:** similar to sawtooth but with a symmetric triangular shape within each period.

### Applications

Periodic functions are used for:

- Modelling periodic phenomena in science and engineering — oscillations, vibrations, waveforms
- Signal processing — sound and image analysis
- Electrical engineering — describing alternating current (AC) circuits
- Music theory and analysis of musical sounds
- Analysing physical systems — pendulums, spring-mass systems

A good grasp of **period, frequency, amplitude, and midline** is crucial for manipulating periodic functions and understanding recurring patterns.

---

### 4.1 Properties of Even and Odd Functions

Even and odd functions are significant categories of real-valued functions. Their names describe behaviour under reflection across the **y-axis** (even) and across the **origin** (odd).

#### Even Functions

An even function satisfies:

$$f(-x) = f(x) \quad \text{for all } x \text{ in the domain of } f$$

Reflecting the graph across the y-axis leaves it unchanged. Key properties:

1. **Symmetry:** graph is symmetric with respect to the **y-axis** — folding along the y-axis makes both halves coincide.
2. **Even Powers:** often contain even powers of $x$ like $x^2, x^4$, etc. However, not all functions with even powers are even — it is the **symmetry property** that defines them.
3. **Examples:** $f(x) = x^2$ and $f(x) = \cos(x)$.

> [!WARNING] Source note
> The PDF also lists "$f(0) = 0$" and "$\int_{-a}^{a} f(x)\,dx = 0$" under even-function properties. These appear to be printing errors in the source — for even functions neither claim holds in general (e.g., $f(x) = x^2$ has $f(0)=0$ but $\int_{-a}^{a} x^2\,dx \neq 0$). Treat those two lines with caution.

#### Odd Functions

An odd function satisfies:

$$f(-x) = -f(x) \quad \text{for all } x \text{ in the domain of } f$$

Reflecting the graph across the origin flips and negates it. Key properties:

1. **Symmetry:** graph is symmetric with respect to the **origin $(0,0)$** — rotating the graph by 180° about the origin leaves it unchanged.
2. **Odd Powers:** often contain odd powers of $x$ like $x, x^3, x^5$, etc. Again, not all functions with odd powers are odd — symmetry is what defines them.
3. **Examples:** $f(x) = x$, $f(x) = \sin(x)$, and $f(x) = \tan(x)$.
4. **Properties:** $f(0) = 0$; the integral of an odd function over a symmetric interval about the origin is zero:
   $$\int_{-a}^{a} f(x)\,dx = 0$$

#### Relation between Even and Odd Functions

A function can be **neither** even nor odd, **both**, or exactly one of the two:

- **Neither:** if it does not exhibit either required symmetry property.
- **Both:** only possible when the function is identically equal to zero ($f(x) = 0$).
- **Exactly one:** even or odd, but not both — the two properties are mutually exclusive otherwise.

---

## 5. Summary

- Unit 1 established relations and functions: pictorial diagrams, domains, co-domains, ranges, and function types (constant, identity, polynomial, etc.), plus relation types (reflexive, symmetric, transitive, equivalence), one-to-one and onto functions, composites, inverses, and binary operations.
- Unit 2 covered **composite functions**: the output of one function flows seamlessly into another, creating a blended new function — like a relay race where team performance hinges on seamless handoffs, or combining spices to create a new flavour.
- Function composition mirrors real-world processes, especially in computer science, where functions and procedures are nested and combined to achieve sophisticated outcomes.
- These foundations build a robust analytical framework applicable to software development, algorithm design, and understanding natural phenomena.

---

## 6. Self-Assessment Questions – 1

**1. What is a composite function?**
   a) A function that has multiple inputs and multiple outputs
   b) A function that combines two or more functions to create a new function
   c) A function that is defined using complex mathematical expressions
   d) A function that only takes integers as input

**2. Which process describes the creation of a composite function?**
   a) Applying one function to the output of another function
   b) Applying both functions to the same input simultaneously
   c) Applying a function to its own output
   d) Combining multiple functions into a single function

**3. If $f(x) = 3x$ and $g(x) = x^2$, what is the composite function $f(g(x))$?**
   a) $f(g(x)) = 3x^2$
   b) $f(g(x)) = 9x$
   c) $f(g(x)) = x^2 + 3$
   d) $f(g(x)) = x^3$

**4. What is the mathematical notation for the composite function of $f(g(x))$?**
   a) $f \circ g(x)$
   b) $g(f(x))$
   c) $g(x) \circ f(x)$
   d) $f(x) \circ g(x)$

**5. How is understanding composite functions useful in computer science and data analysis?**
   a) Composite functions simplify complex mathematical problems
   b) Composite functions only apply to abstract mathematical concepts
   c) Composite functions help create encryption keys
   d) Composite functions allow the creation of complex processes by combining simpler functions

**6. What is the sum of two functions $f(x) = 2x^2 + 3x - 1$ and $g(x) = 4x^2 - x + 2$?**
   a) $6x^2 + 2x + 1$
   b) $6x^2 + 2x - 1$
   c) $6x^2 + 2x$
   d) $6x^2 + 4x - 3$

**7. Which of the following represents the quotient of functions $f(x) = 3x^2 - 5x + 1$ and $g(x) = x - 2$?**
   a) $3x - 1$
   b) $3x - 1 + \dfrac{2}{x-2}$
   c) $3x - 1 - \dfrac{2}{x-2}$
   d) $3x - 1 - 2(x-2)$

**8. Which of the following functions is an example of a periodic function?**
   a) $f(x) = e^x$
   b) $f(x) = \sin(x)$
   c) $f(x) = \ln(x)$
   d) $f(x) = x^2 + 3x - 5$

**9. Which of the following properties correctly describes an odd function?**
   a) $f(x) = f(-x)$
   b) $f(x) = -f(-x)$
   c) $f(x) = -f(x)$
   d) $f(x) = f(x+1)$

### Answer Key

| Q | Answer |
|:-|:-------|
| 1 | b) |
| 2 | a) |
| 3 | a) $f(g(x)) = 3x^2$ |
| 4 | a) $f \circ g(x)$ |
| 5 | d) |
| 6 | a) $6x^2 + 2x + 1$ |
| 7 | c) $3x - 1 - \dfrac{2}{x-2}$ |
| 8 | b) $f(x) = \sin(x)$ |
| 9 | b) $f(x) = -f(-x)$ |

---

## 7. Terminal Questions

1. Why is understanding composite functions important in mathematical analysis and real-world applications?
2. How does the order of composition, i.e., $f(g(x))$ vs $g(f(x))$, impact the resulting composite function?
3. Given $f(x) = 2x + 1$ and $g(x) = x^2 - 3x$, find the composite function $f(g(x))$.
4. If $h(x) = x^3$ and $k(x) = 2x - 5$, calculate the composite function $h(k(x))$.
5. Consider $p(x) = x^2 + 3$ and $q(x) = \sqrt{x}$. Determine the composite function $p(q(x))$.
6. Given $m(x) = 3x + 2$ and $n(x) = x^2 - 4x + 5$, calculate the composite function $m(n(x))$.
7. For $f(x) = 4x - 1$ and $g(x) = x^2 + 2x$, find the composite function $g(f(x))$.
8. If $u(x) = x^2$ and $v(x) = \sqrt{x}$, determine the composite function $u(v(x))$.
9. Consider $r(x) = x^2 + 4$ and $s(x) = 3x - 2$. Calculate the composite function $s(r(x))$.
10. Given functions $a(x) = x + 5$ and $b(x) = 2x - 3$, find the composite function $a(b(x))$.

### Answers

1. Understanding composite functions helps analyse complex relationships between functions and is crucial for modelling real-world scenarios where multiple processes interact.
2. The order of composition affects the outcome — changing the order may yield different mathematical expressions and results.
3. $f(g(x)) = 2(x^2 - 3x) + 1 = 2x^2 - 6x + 1$
4. $h(k(x)) = h(2x - 5) = (2x - 5)^3$

   > [!WARNING] Source note
   > The PDF's answer section repeats Q3's answer here; the working shown above follows from the question as stated.

5. $p(q(x)) = (\sqrt{x})^2 + 3 = x + 3$
6. $m(n(x)) = 3(x^2 - 4x + 5) + 2 = 3x^2 - 12x + 15 + 2 = 3x^2 - 12x + 17$
7. $g(f(x)) = (4x-1)^2 + 2(4x-1) = 16x^2 - 8x + 1 + 8x - 2 = 16x^2 - 1$
8. $u(v(x)) = (\sqrt{x})^2 = x$
9. $s(r(x)) = 3(x^2 + 4) - 2 = 3x^2 + 12 - 2 = 3x^2 + 10$
10. $a(b(x)) = a(2x - 3) = (2x - 3) + 5 = 2x + 2$

    > [!WARNING] Source note
    > The PDF's printed answer ("$11x - 15$") does not follow from substituting into $a(x) = x + 5$; the correct evaluation is shown above.
