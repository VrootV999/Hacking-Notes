# Unit 1: Introduction to Function

> **Course:** Fundamentals of Mathematics — BCA Semester 1  
> **University:** Manipal University Jaipur (MUJ)  
> **Unit:** 1 — Introduction to Function

---

## Table of Contents

| # | Section | Topic |
|---|---------|-------|
| 1 | [Introduction](#1-introduction) | Why Mathematics matters for BCA |
| 1.1 | [Learning Objectives](#11-learning-objectives) | What you'll learn in this unit |
| 2 | [Relations](#2-relation-pictorial-diagrams-domain-co-domain-range-of-a-relation) | Relations, Types, Pictorial Diagrams, Domain, Co-Domain, Range |
| 2.1 | [Relations](#21-relations) | Definition and example |
| 2.1.1 | [Types of Relations](#211-types-of-relations) | Empty, Universal, Reflexive, Symmetric, Transitive, Equivalence |
| 2.2 | [Pictorial Diagrams](#22-pictorial-diagrams) | Visual representations of relations |
| 2.3 | [Domain](#23-domain) | Input values |
| 2.4 | [Co-Domain](#24-co-domain) | Possible output values |
| 2.5 | [Range of a Relation](#25-range-of-a-relation) | Actual output values |
| 3 | [Function](#3-function) | Definition, One-One, Onto, Bijective |
| 4 | [Domain and Range of a Function](#4-domain-and-range-of-a-function) | Finding domain and range |
| 4.1 | [Finding Domain & Range](#41-finding-domain-and-range-of-specific-functions) | Linear, Square Root, Absolute Value, Quadratic |
| 4.2 | [Types of Functions](#42-types-of-functions) | 10 function types with formulas |
| 5 | [Properties of Functions](#5-properties-of-functions) | Injective, Surjective, Composite, Inverse, Binary Operation |

---

## 1. Introduction

Mathematics forms the **backbone of logical reasoning** and analytical thought processes, which are indispensable in the field of computing and information technology.

- It equips students with the essential tools to **tackle complex problems, devise algorithms**, and understand the theoretical underpinnings of computer science.
- The study of **relations, sets, functions, and their properties** lays the groundwork for understanding more advanced topics such as **database structures, programming, and software development**.
- A strong foundation in these mathematical concepts not only enhances **computational skills** but also fosters a rigorous **analytical mindset**, enabling students to approach problems methodically and innovate solutions effectively.

### Unit 1 Scope

- Unit 1 delves into the intricacies of **relations, pictorial diagrams, domains, codomains, and the range** of a relation.
- The concept of relations establishes a framework to **model and analyse connections between different sets of data** — an aspect central to computing and programming.
- By understanding how elements from one set relate to elements in another through various types of relations such as **reflexive, symmetric, and transitive**, students can better grasp data organization, database relationships, and algorithm efficiency.

---

## 2. Relation, Pictorial Diagrams, Domain, Co-Domain, Range of a Relation

### 2.1 Relations

A **relation** is a mathematical concept that describes how elements from one set are related to elements in another set. It defines connections or associations between these elements.

**Definition:** A relation $R$ is a **subset of $A \times A$**.

A relation is typically expressed as a **set of ordered pairs**, where each pair consists of an element from the first set (called the **domain**) and an element from the second set (called the **co-domain**). Relations can model a wide range of real-world scenarios, such as the relationships between people, numbers, or any other objects.

> [!example] Example
> Consider a relation $R$ in the set $A = \{1, 2, 3, 4\}$ given by:
>
> $$R = \{(a, b) : a - b = 10\}$$
>
> This is an **empty set**, as no pair $(a, b)$ satisfies the condition $a - b = 10$.

---

### 2.1.1 Types of Relations

#### 1. Empty Relation

**Definition:** A relation $R$ in a set $A$ is called an **empty relation** if no element of $A$ is related to any element of $A$, i.e.,

$$R = \emptyset \subset A \times A$$

#### 2. Universal Relation

**Definition:** A relation $R$ in a set $A$ is called a **universal relation** if each element of $A$ is related to every element of $A$, i.e.,

$$R = A \times A$$

> [!note] Both the **empty** and **universal** relations are also called **trivial relations**.

> [!example] Example
> Let $A$ be the set of all students of a boys school.
>
> - $R = \{(a, b) : a \text{ is sister of } b\}$ $\rightarrow$ **Empty relation** (no student can be sister of another in a boys school)
> - $R' = \{(a, b) : \text{the difference between heights of } a \text{ and } b \text{ is less than 3 meters}\}$ $\rightarrow$ **Universal relation** (always true for any two students)

---

#### 3. Reflexive, Symmetric, Transitive

A relation $R$ in a set $A$ is called:

| Property | Condition |
|:---------|:----------|
| **Reflexive** | $(a, a) \in R$, for every $a \in A$ |
| **Symmetric** | $(a_1, a_2) \in R$ implies that $(a_2, a_1) \in R$, for all $a_1, a_2 \in A$ |
| **Transitive** | $(a_1, a_2) \in R$ and $(a_2, a_3) \in R$ implies that $(a_1, a_3) \in R$, for all $a_1, a_2, a_3 \in A$ |

---

#### 4. Equivalence Relation

**Definition:** A relation $R$ in a set $A$ is said to be an **equivalence relation** if $R$ is **reflexive, symmetric, and transitive**.

> [!example] Example 1 — Triangles Congruence
> Let $T$ be the set of all triangles in a plane with $R = \{(T_1, T_2) : T_1 \text{ is congruent to } T_2\}$.
>
> | Property | Verification | |
> |:---------|:-------------|:-|
> | **Reflexive** | Every triangle is congruent to itself | $\checkmark$ |
> | **Symmetric** | $T_1 \cong T_2 \implies T_2 \cong T_1$ | $\checkmark$ |
> | **Transitive** | $T_1 \cong T_2$ and $T_2 \cong T_3 \implies T_1 \cong T_3$ | $\checkmark$ |
>
> $\therefore$ $R$ is an **equivalence relation**.

> [!example] Example 2 — Divisibility by 2 in $\mathbb{Z}$
> Show that $R = \{(a, b) : 2 \text{ divides } a - b\}$ is an equivalence relation in $\mathbb{Z}$.
>
> | Property | Verification | |
> |:---------|:-------------|:-|
> | **Reflexive** | $2$ divides $(a - a)$ for all $a \in \mathbb{Z}$ | $\checkmark$ |
> | **Symmetric** | If $2$ divides $(a - b)$, then $2$ divides $(b - a)$ | $\checkmark$ |
> | **Transitive** | If $2 \mid (a - b)$ and $2 \mid (b - c)$, then $a - c = (a - b) + (b - c)$ is even, so $2 \mid (a - c)$ | $\checkmark$ |
>
> $\therefore$ $R$ is an **equivalence relation**.
>
> **Key observations:**
>
> - All **even integers** are related to zero — $(0, \pm 2), (0, \pm 4), \ldots$ lie in $R$
> - No **odd integer** is related to $0$ — $(0, \pm 1), (0, \pm 3), \ldots$ do not lie in $R$
> - All **odd integers** are related to one; no even integer is related to one

---

### Equivalence Classes and Partitions

The set $E$ of all even integers and the set $O$ of all odd integers are subsets of $\mathbb{Z}$ satisfying:

1. All elements of $E$ are related to each other; all elements of $O$ are related to each other.
2. No element of $E$ is related to any element of $O$ and vice-versa.
3. $E$ and $O$ are disjoint and $\mathbb{Z} = E \cup O$.

| Notation | Meaning |
|:---------|:--------|
| $[0]$ | Equivalence class containing zero (all even integers) |
| $[1]$ | Equivalence class containing one (all odd integers) |

> [!tip] Note
> $[0] \neq [1]$, $\;[0] = [2r]$, $\;[1] = [2r + 1]$, $\;\forall\, r \in \mathbb{Z}$.

**General property:** Given an arbitrary equivalence relation $R$ in an arbitrary set $X$, $R$ divides $X$ into **mutually disjoint subsets $A_i$** called **partitions** (or subdivisions) of $X$ satisfying:

1. All elements of $A_i$ are related to each other, for all $i$.
2. No element of $A_i$ is related to any element of $A_j$, $i \neq j$.
3. $\bigcup A_j = X$ and $A_i \cap A_j = \emptyset$, $i \neq j$.

> [!example] Example — Partition by Multiples of 3
>
> | Subset | Definition | Elements |
> |:-------|:-----------|:---------|
> | $A_1$ | $\{x \in \mathbb{Z} : x \text{ is a multiple of } 3\}$ | $\{\ldots, -6, -3, 0, 3, 6, \ldots\}$ |
> | $A_2$ | $\{x \in \mathbb{Z} : x - 1 \text{ is a multiple of } 3\}$ | $\{\ldots, -5, -2, 1, 4, 7, \ldots\}$ |
> | $A_3$ | $\{x \in \mathbb{Z} : x - 2 \text{ is a multiple of } 3\}$ | $\{\ldots, -4, -1, 2, 5, 8, \ldots\}$ |
>
> Here $A_1 = [3r]$, $A_2 = [3r + 1]$, $A_3 = [3r + 2]$, for all $r \in \mathbb{Z}$.

---

### 2.2 Pictorial Diagrams

**Pictorial diagrams** are visual representations used to illustrate relations or connections between elements from different sets.

- They provide a **graphical way** to understand and present relationships.
- You can use **arrows, lines, or other symbols** to show how elements from one set correspond to elements in another.
- Pictorial diagrams make abstract concepts more accessible and aid in problem-solving and comprehension.

---

### 2.3 Domain

**Definition:** The **domain** of a relation is the set of all **input or independent values** (elements) for which the relation is defined. It represents the possible input values that can be used to determine the relation's output values.

- The domain specifies the "starting point" — the values that you can plug into the relation to obtain corresponding output values.
- The domain is essential for understanding the scope of a relation and for ensuring that you use valid inputs.

---

### 2.4 Co-Domain

**Definition:** The **co-domain** of a relation is the set of all **possible output or dependent values** (elements) that the relation can produce. It represents the full range of potential output values, regardless of whether they are actually produced by the relation.

- The co-domain defines the "destination" or the set of possible output values that the relation can map elements from the domain to.
- It is important to note that **not all elements from the co-domain may have a corresponding element in the range**.
- The co-domain is a **broader concept**, while the range describes the actual output values produced by the relation.

---

### 2.5 Range of a Relation

**Definition:** The **range** of a relation is the set of all **actual output values** (elements) produced by the relation when elements from the domain are used as input. It represents the **subset of the co-domain** that is "covered" or "occupied" by the relation.

- The range is a subset of the co-domain and defines the actual output values generated by the relation for the given inputs.
- The range may be **smaller than the co-domain** if not all possible outputs are achieved.

---

### Quick Reference: Domain vs Co-Domain vs Range

| Concept | Definition | Analogy |
|:--------|:-----------|:--------|
| **Domain** | Set of all valid input values | "Where do we begin?" |
| **Co-Domain** | Set of all *possible* output values | "Where *could* we end up?" |
| **Range** | Set of all *actual* output values | "Who *actually* showed up?" |

---

## 3. Function

**Definition:** A **function** is a mathematical relationship that assigns each input element from a set (called the **domain**) to a **unique** output element in another set (called the **codomain**). It can be represented by a rule or equation and is denoted as:

$$f(x) \qquad \text{or} \qquad y = f(x)$$

Functions provide a structured way to understand how variables change with respect to each other.

---

### Types of Functions (by Mapping)

#### Definition 1 — One-One (Injective)

**Definition:** A function $f : X \to Y$ is defined to be **one-one (injective)**, if the images of distinct elements of $X$ under $f$ are distinct, i.e.,

$$\forall\; x_1, x_2 \in X, \quad f(x_1) = f(x_2) \implies x_1 = x_2$$

Otherwise, $f$ is called **many-one**.

#### Definition 2 — Onto (Surjective)

**Definition:** A function $f : X \to Y$ is said to be **onto (surjective)**, if every element of $Y$ is the image of some element of $X$ under $f$, i.e.,

$$\forall\; y \in Y, \;\exists\; x \in X \text{ such that } f(x) = y$$

> [!tip] Remark
> $f : X \to Y$ is onto **if and only if** $\text{Range of } f = Y$.

#### Definition 3 — Bijective (One-One and Onto)

**Definition:** A function $f : X \to Y$ is said to be **one-one and onto (bijective)**, if $f$ is **both** one-one and onto.

---

### Quick Comparison: One-One, Onto, Bijective

| Property | Condition |
|:---------|:----------|
| **One-One (Injective)** | Distinct inputs map to distinct outputs: $f(x_1) = f(x_2) \implies x_1 = x_2$ |
| **Onto (Surjective)** | Every element in codomain is an image of some element in domain: $\text{Range} = \text{Codomain}$ |
| **Bijective** | Both one-one and onto |

---

> [!example] Example
> Let $\mathbb{N}$ be the set of natural numbers and the relation $R$ be defined on $\mathbb{N}$ such that:
>
> $$R = \{(x, y) : y = 2x,\; x, y \in \mathbb{N}\}$$
>
> **Question:** What is the domain, codomain and range of $R$? Is this relation a function?
>
> **Solution:**
>
> | Component | Value |
> |:----------|:------|
> | **Domain** | The set of natural numbers $\mathbb{N}$ |
> | **Codomain** | $\mathbb{N}$ |
> | **Range** | The set of **even natural numbers** $\{2, 4, 6, 8, \ldots\}$ |
>
> Since every natural number $n$ has **one and only one** image, this relation **is a function**.

---

## 4. Domain and Range of a Function

### Domain of a Function

**Definition:** The **domain** of a function is the set of all possible **input values** for which the function is defined. It's the collection of values that you can plug into the function to get meaningful output.

> [!example] Example
> In the function $f(x) = \sqrt{x}$, the domain would include all **non-negative real numbers**, as the square root of a negative number is undefined in the real number system.

### Range of a Function

**Definition:** The **range** of a function is the set of all possible **output values** that the function can produce based on its domain. It represents the values that the function "maps" its domain elements to.

> [!example] Example
> In the function $f(x) = x^2$, the range consists of all **non-negative real numbers**, as the function squares the input values, resulting in non-negative outputs.

---

### 4.1 Finding Domain and Range of Specific Functions

> [!example] 1. Linear Function
> **Consider:** $f(x) = 2x - 3$
>
> | | Details |
> |:--|:--------|
> | **Domain** | No restrictions on input. Domain = all real numbers: $(-\infty, \infty)$ |
> | **Range** | As $x$ varies from $-\infty$ to $+\infty$, $f(x)$ also covers all real numbers. Range = $(-\infty, \infty)$ |

---

> [!example] 2. Square Root Function
> **Consider:** $g(x) = \sqrt{4 - x^2}$
>
> | | Details |
> |:--|:--------|
> | **Domain** | The expression inside the square root must be **non-negative**: $4 - x^2 \geq 0$. Solving gives $-2 \leq x \leq 2$. Domain = $[-2, 2]$ |
> | **Range** | The square root of a non-negative value is always non-negative. Range = $[0, \infty)$ |
>
> **Steps to solve $4 - x^2 \geq 0$:**
>
> $$4 - x^2 \geq 0 \;\implies\; x^2 \leq 4 \;\implies\; |x| \leq 2 \;\implies\; -2 \leq x \leq 2$$

---

> [!example] 3. Absolute Value Function
> **Consider:** $h(x) = |2x - 5|$
>
> | | Details |
> |:--|:--------|
> | **Domain** | No restrictions. Domain = all real numbers: $(-\infty, \infty)$ |
> | **Range** | The absolute value function always produces **non-negative** values. Range = $[0, \infty)$ |

---

> [!example] 4. Quadratic Function
> **Consider:** $p(x) = x^2 - 4x + 3$
>
> | | Details |
> |:--|:--------|
> | **Domain** | No restrictions. Domain = all real numbers: $(-\infty, \infty)$ |
> | **Range** | Consider the **vertex** at $x = 2$ (found by completing the square). Since $x^2$ is always non-negative, the lowest value the function can have is $0$. Range = $[0, \infty)$ |
>
> [!tip] Tip
> To find the vertex of $p(x) = x^2 - 4x + 3$, complete the square or use $x = \dfrac{-b}{2a} = \dfrac{4}{2} = 2$.

---

### Summary Table: Domain and Range

| Function Type | Example | Domain | Range |
|:--------------|:--------|:-------|:------|
| **Linear** | $f(x) = 2x - 3$ | $(-\infty, \infty)$ | $(-\infty, \infty)$ |
| **Square Root** | $g(x) = \sqrt{4 - x^2}$ | $[-2, 2]$ | $[0, \infty)$ |
| **Absolute Value** | $h(x) = \|2x - 5\|$ | $(-\infty, \infty)$ | $[0, \infty)$ |
| **Quadratic** | $p(x) = x^2 - 4x + 3$ | $(-\infty, \infty)$ | $[0, \infty)$ |

---

## 4.2 Types of Functions

---

### 4.2.1 Real-Valued Functions

**Definition:** A **real-valued function** is a function that assigns real numbers as output values for real numbers in its domain. In other words, it takes real numbers as input and produces real numbers as output.

Real-valued functions are widely used in mathematics, science, and engineering to model various phenomena. They can represent relationships, measurements, and behaviours in the real world, making them essential for applications like physics, economics, and more.

---

### 4.2.2 Constant Function

**Definition:** A function $f: \mathbb{R} \to \mathbb{R}$ defined by:

$$f(x) = c, \quad x \in \mathbb{R}$$

where $c$ is a constant and each $x \in \mathbb{R}$.

| Property | Value |
|:---------|:------|
| **Domain** | The set of all real numbers $\mathbb{R}$ |
| **Range** | A single real number $\{c\}$ |

> [!example] Example
> $f(x) = 3$
>
> - **Domain:** All real numbers
> - **Range:** $\{3\}$

---

### 4.2.3 Identity Function

**Definition:** Let $\mathbb{R}$ be the set of real numbers. Define the real-valued function $f: \mathbb{R} \to \mathbb{R}$ by:

$$f(x) = x, \quad \text{for each } x \in \mathbb{R}$$

Such a function is called the **identity function**. Here the domain and range of $f$ are $\mathbb{R}$. The graph is a **straight line passing through the origin**.

| Property | Value |
|:---------|:------|
| **Domain** | The set of all real numbers $\mathbb{R}$ |
| **Range** | The set of all real numbers $\mathbb{R}$ |

> [!example] Example
> $f(x) = x$
>
> - **Domain:** All real numbers
> - **Range:** All real numbers

---

### 4.2.4 Polynomial Function

**Definition:** A function $f: \mathbb{R} \to \mathbb{R}$ is said to be a **polynomial function** if for each $x$ in $\mathbb{R}$:

$$f(x) = a_0 + a_1 x + a_2 x^2 + \cdots + a_n x^n$$

where $n$ is a **non-negative integer** and $a_0, a_1, a_2, \ldots, a_n \in \mathbb{R}$.

| Function | Polynomial? |
|:---------|:------------|
| $f(x) = x^3 - x^2 + 2$ | Yes |
| $g(x) = x^4 + \sqrt{2}\, x$ | Yes |
| $h(x) = x^{3/2} + 2x$ | **No** (exponent $\frac{3}{2}$ is not a non-negative integer) |

| Property | Value |
|:---------|:------|
| **Domain** | The set of all real numbers $\mathbb{R}$ |
| **Range** | Can vary depending on the degree and leading coefficients of the polynomial |

> [!example] Example
> $f(x) = 2x^3 - 5x^2 + 4x - 1$
>
> - **Domain:** All real numbers
> - **Range:** All real numbers

---

### 4.2.5 Rational Function

**Definition:** Rational functions are functions of the type:

$$\frac{f(x)}{g(x)}$$

where $f(x)$ and $g(x)$ are **polynomial functions** of $x$, defined in a domain where $g(x) \neq 0$.

| Property | Value |
|:---------|:------|
| **Domain** | All real numbers **except** the values that make the denominator equal to zero (since division by zero is undefined) |
| **Range** | Can vary; typically covering a wide range of real numbers |

> [!example] Example
> $f(x) = \dfrac{1}{x}$
>
> - **Domain:** All real numbers **except** $x = 0$
> - **Range:** All real numbers **except** $0$

---

### 4.2.6 Modulus Function (Absolute Value)

**Definition:** The function $f: \mathbb{R} \to \mathbb{R}$ defined by:

$$f(x) = |x|, \quad \text{for each } x \in \mathbb{R}$$

is called the **modulus function**. For each non-negative value of $x$, $f(x)$ is equal to $x$. But for negative values of $x$, the value of $f(x)$ is the negative of the value of $x$, i.e.,

$$f(x) = \begin{cases} x, & x \geq 0 \\ -x, & x < 0 \end{cases}$$

| Property | Value |
|:---------|:------|
| **Domain** | All real numbers $\mathbb{R}$ |
| **Range** | Set of **non-negative** real numbers $[0, \infty)$ |

> [!example] Example
> $f(x) = |x|$
>
> - **Domain:** All real numbers
> - **Range:** Non-negative real numbers

---

### 4.2.7 Signum Function (Sign Function)

**Definition:** The function $f: \mathbb{R} \to \mathbb{R}$ defined by

$$f(x) = \begin{cases} 1, & x > 0 \\ 0, & x = 0 \\ -1, & x < 0 \end{cases}$$

is called the **signum function**. The domain of the signum function is $\mathbb{R}$ and the range is the set $\{-1, 0, 1\}$.

| Property | Value |
|:---------|:------|
| **Domain** | All real numbers $\mathbb{R}$ |
| **Range** | The set $\{-1, 0, 1\}$ |

> [!example] Example
> $f(x) = \text{sgn}(x)$
>
> - **Domain:** All real numbers
> - **Range:** $\{-1, 0, 1\}$

---

### 4.2.8 Exponential Function

**Definition:** Exponential function, as its name suggests, involves exponents. But note that, an exponential function has a **constant as its base** and a **variable as its exponent**.

| Property | Value |
|:---------|:------|
| **Domain** | All real numbers $\mathbb{R}$ |
| **Range** | Typically all **positive** real numbers (depends on base and whether it represents growth or decay) |

> [!example] Example
> $f(x) = 2^x$
>
> - **Domain:** All real numbers
> - **Range:** Positive real values only

---

### 4.2.9 Logarithmic Function

**Definition:** The basic **logarithmic function** is of the form:

$$f(x) = \log_a(x), \quad \text{where } a > 0$$

| Property | Value |
|:---------|:------|
| **Domain** | The set of all **positive** real numbers (logarithm of zero or a negative number is **undefined**) |
| **Range** | All real numbers $\mathbb{R}$ |

> [!example] Example
> $f(x) = \log(x)$
>
> - **Domain:** All positive real numbers
> - **Range:** All real numbers

---

### 4.2.10 Greatest Integer Function (Step Function)

**Definition:** The function $f: \mathbb{R} \to \mathbb{R}$ defined by:

$$f(x) = \lfloor x \rfloor, \quad x \in \mathbb{R}$$

assumes the value of the **greatest integer less than or equal to** $x$. Such a function is also called the **step function**.

**Values of $\lfloor x \rfloor$:**

| Interval | $\lfloor x \rfloor$ |
|:---------|:--------------------|
| $-1 \leq x < 0$ | $-1$ |
| $0 \leq x < 1$ | $0$ |
| $1 \leq x < 2$ | $1$ |
| $2 \leq x < 3$ | $2$ |
| $\vdots$ | $\vdots$ |

| Property | Value |
|:---------|:------|
| **Domain** | All real numbers $\mathbb{R}$ |
| **Range** | All integers $\mathbb{Z}$ |

> [!example] Example
> $f(x) = \lfloor x \rfloor$
>
> - **Domain:** All real numbers
> - **Range:** All integers

---

### Summary: Comparison of All Function Types

| # | Function Type | Formula / Definition | Domain | Range |
|:--|:-------------|:---------------------|:-------|:------|
| 1 | **Real-Valued** | Assigns real output for real input | $\mathbb{R}$ | $\mathbb{R}$ |
| 2 | **Constant** | $f(x) = c$ | $\mathbb{R}$ | $\{c\}$ |
| 3 | **Identity** | $f(x) = x$ | $\mathbb{R}$ | $\mathbb{R}$ |
| 4 | **Polynomial** | $f(x) = a_0 + a_1 x + a_2 x^2 + \cdots + a_n x^n$ | $\mathbb{R}$ | Varies with degree & leading coefficients |
| 5 | **Rational** | $f(x) = \dfrac{p(x)}{q(x)},\; q(x) \neq 0$ | All $\mathbb{R}$ except where $q(x) = 0$ | Varies; typically wide range of reals |
| 6 | **Modulus** | $f(x) = \|x\|$ | $\mathbb{R}$ | $[0, \infty)$ |
| 7 | **Signum** | $f(x) = \text{sgn}(x)$ | $\mathbb{R}$ | $\{-1, 0, 1\}$ |
| 8 | **Exponential** | $f(x) = a^x$ | $\mathbb{R}$ | $(0, \infty)$ |
| 9 | **Logarithmic** | $f(x) = \log_a(x),\; a > 0$ | $(0, \infty)$ | $\mathbb{R}$ |
| 10 | **Greatest Integer** | $f(x) = \lfloor x \rfloor$ | $\mathbb{R}$ | $\mathbb{Z}$ |

---

## 5. Properties of Functions

### One-to-One Function (Injective)

**Definition:** A function is **one-to-one** if, for every distinct pair of elements $a$ and $b$ in the domain, the function assigns distinct values to them, i.e.,

$$f(a) \neq f(b)$$

> [!example] Example
> The function $f(x) = 2x$ is **one-to-one** because it maps distinct inputs to distinct outputs.

---

### Onto Function (Surjective)

**Definition:** A function is **onto** if, for every element in the co-domain, there is at least one element in the domain that maps to it. In other words, the function **covers the entire codomain**.

> [!example] Example
> The function $f(x) = x^2$ from the set of real numbers to the set of non-negative real numbers is **onto**.

---

### Composite Function

**Definition:** A **composite function** is formed by applying one function to the output of another function. If $f$ and $g$ are functions, then the composite function $f \circ g$ is defined as:

$$(f \circ g)(x) = f(g(x))$$

> [!example] Example
> If $f(x) = 2x$ and $g(x) = x + 3$, then:
>
> $$(f \circ g)(x) = f(g(x)) = f(x + 3) = 2(x + 3) = 2x + 6$$

---

### Inverse of a Function

**Definition:** The **inverse** of a function $f$ is another function denoted as $f^{-1}$ such that:

$$f\big(f^{-1}(x)\big) = x \quad \text{for all } x \text{ in the domain of } f^{-1}$$
$$f^{-1}\big(f(x)\big) = x \quad \text{for all } x \text{ in the domain of } f$$

> [!example] Example
> The inverse of the function $f(x) = 3x$ is $f^{-1}(x) = \dfrac{x}{3}$, as:
>
> $$f\big(f^{-1}(x)\big) = 3\left(\frac{x}{3}\right) = x$$

---

### Binary Operation

**Definition:** A **binary operation** is a function that takes two elements from a set and combines them to produce another element in the same set. It associates two elements with a third.

> [!example] Example
> Addition ($+$) and multiplication ($\times$) are **binary operations** on the set of real numbers because adding or multiplying two real numbers results in another real number.
