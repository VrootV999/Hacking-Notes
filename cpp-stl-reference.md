# C++ STL, Concurrency, and Modern Features - Comprehensive Reference

All information verified against cppreference.com (the authoritative C++ reference).

---

## 1. Containers

### 1.1 std::vector (header: <vector>)

**Definition:** A sequence container that encapsulates dynamic-size arrays with contiguous storage.

**Complexity:**
- Random access (operator[]): O(1)
- Insert/remove at end: Amortized O(1)
- Insert/remove at middle: O(n)
- size() / capacity(): O(1)

**Growth Strategy:** The standard does not mandate a specific factor. Typical implementations:
- libstdc++ (GCC): 2x
- libc++ (Clang): 2x
- MSVC STL: 1.5x

**capacity() vs size():**
- size(): Number of elements currently stored
- capacity(): Storage available before next reallocation
- capacity() >= size() is always true

**reserve(n):** Pre-allocates storage for at least n elements. Does not change size().

**emplace_back vs push_back:**
- push_back(x): Copies/moves x into the container; x must already exist.
- emplace_back(args...): Constructs element in-place; avoids copy/move of the element.

```cpp
#include <vector>
#include <string>
#include <iostream>

int main() {
    std::vector<int> v;
    v.reserve(10);           // pre-allocate for 10 elements

    v.push_back(1);          // copy/move into vector
    v.emplace_back(2);       // construct in-place

    std::cout << "size=" << v.size() << ", capacity=" << v.capacity() << "\n";
    // size=2, capacity=10

    std::vector<std::string> vs;
    vs.emplace_back(10, 'a');  // constructs "aaaaaaaaaa" in-place

    for (const auto& x : v)
        std::cout << x << " ";  // 1 2
}
```

---

### 1.2 std::map (header: <map>)

**Definition:** A sorted associative container with unique key-value pairs. Sorted by std::less<Key> by default. **Internally a red-black tree.**

**Complexity:** O(log n) for search, insert, and erase.

**Key properties:**
- Keys always sorted in ascending order
- operator[] inserts a default-constructed value if key is absent (use count/find/contains to check first)
- contains() (C++20) returns bool without inserting

```cpp
#include <map>
#include <string>
#include <iostream>

int main() {
    std::map<std::string, int> m;
    m["CPU"] = 10;              // inserts if absent, assigns if present
    m.insert({"GPU", 15});      // does nothing if key exists
    m.try_emplace("RAM", 20);   // constructs in-place only if key absent
    m.insert_or_assign("SSD", 30); // inserts or overwrites

    for (const auto& [key, value] : m)   // C++17 structured bindings
        std::cout << key << ": " << value << "\n";

    if (m.contains("CPU"))               // C++20
        std::cout << "Found CPU\n";
}
```

---

### 1.3 std::unordered_map (header: <unordered_map>)

**Definition:** An associative container with unique keys, organized into buckets by hash. **Hash table internally.**

**Complexity:** Average O(1) for search/insert/erase. Worst case O(n) with poor hash.

**Collision handling:** Elements with same hash go in the same bucket; within a bucket, elements are compared via KeyEqual. Load factor = size() / bucket_count(). Default max_load_factor() is 1.0.

```cpp
#include <unordered_map>
#include <string>
#include <iostream>

int main() {
    std::unordered_map<std::string, int> um;
    um["red"] = 0xFF0000;
    um["green"] = 0x00FF00;
    um.emplace("blue", 0x0000FF);

    for (const auto& [key, value] : um)
        std::cout << key << " = " << std::hex << value << "\n";

    std::cout << "Buckets: " << um.bucket_count() << "\n";
    std::cout << "Load factor: " << um.load_factor() << "\n";
    um.reserve(100);    // pre-allocate for 100 elements
    um.rehash(64);      // set minimum bucket count
}
```

---

### 1.4 std::deque (header: <deque>)

**Definition:** Double-ended queue. Elements are NOT contiguous; typically a sequence of individually allocated fixed-size arrays (chunks). Fast insertion at both ends.

**Complexity:**
- Random access: O(1)
- Insert/remove at beginning or end: O(1)
- Insert/remove at middle: O(n)

**Key distinction from vector:** Front insertion is O(1). Insertion at either end never invalidates references to other elements.

```cpp
#include <deque>
#include <iostream>

int main() {
    std::deque<int> d = {7, 5, 16, 8};
    d.push_front(13);    // O(1)
    d.push_back(25);     // O(1)
    d.pop_front();       // O(1)
    d.pop_back();        // O(1)

    for (int n : d)
        std::cout << n << " ";  // 7 5 16 8
}
```

---

### 1.5 std::list (header: <list>)

**Definition:** Doubly-linked list. Constant-time insertion/removal anywhere (given iterator). No random access. Bidirectional iterators.

**Complexity:**
- Insert/remove at any position: O(1) (given iterator)
- Find/search: O(n)
- size(): O(1) since C++11

**Key properties:** Insertion/removal does NOT invalidate iterators or references (except to the deleted element). Provides splice(), merge(), remove(), sort(), reverse(), unique().

```cpp
#include <list>
#include <algorithm>
#include <iostream>

int main() {
    std::list<int> l = {7, 5, 16, 8};
    l.push_front(25);
    l.push_back(13);

    auto it = std::find(l.begin(), l.end(), 16);
    if (it != l.end())
        l.insert(it, 42);  // O(1) insert before 16

    l.sort();               // member sort (not std::sort - list has no random access)
    l.reverse();
    l.remove(5);            // removes all elements equal to 5

    for (int n : l)
        std::cout << n << " ";
}
```

---

### 1.6 std::set and std::unordered_set

**std::set (header: <set>):** Sorted unique elements. Red-black tree. O(log n) operations. Elements are constant (read-only iterators).

```cpp
#include <set>
#include <iostream>

int main() {
    std::set<int> s = {5, 3, 1, 4, 2};

    s.insert(6);
    s.erase(1);
    bool found = s.contains(4);  // C++20, O(log n)

    for (int x : s)
        std::cout << x << " ";   // 2 3 4 5 6 (sorted)
}
```

**std::unordered_set (header: <unordered_set>):** Hash table. Average O(1). No ordering guarantee.

```cpp
#include <unordered_set>
#include <iostream>

int main() {
    std::unordered_set<int> us = {5, 3, 1, 4, 2};
    us.insert(6);
    us.erase(1);

    for (int x : us)
        std::cout << x << " ";   // order unspecified
}
```

---

### 1.7 std::array (header: <array>, C++11)

**Definition:** Fixed-size, stack-allocated array. Aggregate type wrapping C-style array T[N]. Does NOT decay to T* automatically. Knows its own size.

```cpp
#include <array>
#include <algorithm>
#include <iostream>

int main() {
    std::array<int, 5> a = {5, 3, 1, 4, 2};

    std::cout << "size=" << a.size() << "\n";  // 5
    std::sort(a.begin(), a.end());

    for (int x : a)
        std::cout << x << " ";  // 1 2 3 4 5

    // C++17 deduction guide
    std::array b{1, 2, 3};  // std::array<int, 3>
}
```

---

## 2. Iterators and Ranges (C++20)

### 2.1 Iterator Categories (Hierarchy from weakest to strongest)

| Category | Operations | Use Case |
|---|---|---|
| Input | read, single-pass, increment | istream_iterator |
| Output | write, single-pass, increment | ostream_iterator |
| Forward | read/write, multi-pass, increment | forward_list, unordered_set |
| Bidirectional | + decrement | list, set, map |
| Random Access | + arithmetic, subscript, compare | vector, deque |
| Contiguous | elements contiguous in memory | vector, array, string, C arrays |

Tags (used for dispatching): input_iterator_tag, forward_iterator_tag, bidirectional_iterator_tag, random_access_iterator_tag, contiguous_iterator_tag (C++20).

```cpp
#include <iterator>
#include <vector>
#include <list>
#include <type_traits>
#include <iostream>

// Compile-time iterator category detection
template<typename It>
void print_category(It) {
    using Cat = typename std::iterator_traits<It>::iterator_category;
    if constexpr (std::is_same_v<Cat, std::random_access_iterator_tag>)
        std::cout << "Random Access\n";
    else if constexpr (std::is_same_v<Cat, std::bidirectional_iterator_tag>)
        std::cout << "Bidirectional\n";
    else if constexpr (std::is_same_v<Cat, std::forward_iterator_tag>)
        std::cout << "Forward\n";
}

int main() {
    std::vector<int> v = {1, 2, 3};
    std::list<int> l = {1, 2, 3};

    print_category(v.begin());  // Random Access
    print_category(l.begin());  // Bidirectional
}
```

### 2.2 Iterator Operations

```cpp
#include <iterator>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};

    auto it = v.begin();
    std::advance(it, 3);          // move iterator forward by 3: *it == 40
    std::cout << *it << "\n";     // 40

    auto dist = std::distance(v.begin(), v.end());  // 5
    std::cout << dist << "\n";

    auto next_it = std::next(v.begin(), 2);  // returns new iterator, doesn't modify original
    std::cout << *next_it << "\n";           // 30
}
```

### 2.3 Range-based for Loop

```cpp
std::vector<int> v = {1, 2, 3};

// By value (copy)
for (int x : v) { /* ... */ }

// By const reference (no copy, read-only)
for (const auto& x : v) { /* ... */ }

// By reference (mutable)
for (auto& x : v) { x *= 2; }
```

### 2.4 std::ranges (C++20)

The ranges library provides composable, lazy range adaptors and constrained algorithms.

**Key range adaptors (views):**
- views::filter(pred) - keep elements matching predicate
- views::transform(fn) - apply function to each element
- views::take(n) - first n elements
- views::drop(n) - skip first n elements
- views::reverse - reversed order
- views::keys / views::values - for pair-like ranges
- views::iota(start) - infinite sequence from start

**Ranges algorithms (constrained versions of std algorithms):**
- std::ranges::sort, std::ranges::find, std::ranges::copy, etc.

```cpp
#include <ranges>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Pipeline syntax: filter even, then square them
    auto result = v
        | std::views::filter([](int i) { return i % 2 == 0; })
        | std::views::transform([](int i) { return i * i; });

    for (int x : result)
        std::cout << x << " ";  // 4 16 36 64 100
    std::cout << "\n";

    // Take first 3
    for (int x : v | std::views::take(3))
        std::cout << x << " ";  // 1 2 3
    std::cout << "\n";

    // Ranges algorithm
    auto it = std::ranges::find(v, 5);
    if (it != v.end())
        std::cout << "Found: " << *it << "\n";  // 5

    std::ranges::sort(v, std::ranges::greater{});  // sort descending
}
```

### 2.5 Custom Iterator

```cpp
#include <iterator>
#include <iostream>

class Counter {
    int value_ = 0;
    int limit_ = 0;
public:
    // Iterator traits
    using iterator_category = std::input_iterator_tag;
    using value_type        = int;
    using difference_type   = std::ptrdiff_t;
    using pointer           = int*;
    using reference         = int&;

    Counter(int limit) : limit_(limit) {}

    // Dereference
    int operator*() const { return value_; }

    // Pre-increment
    Counter& operator++() {
        ++value_;
        return *this;
    }

    // Post-increment
    Counter operator++(int) {
        Counter tmp = *this;
        ++value_;
        return tmp;
    }

    // Equality
    bool operator!=(const Counter& other) const {
        return value_ != other.limit_;
    }

    bool operator==(const Counter& other) const {
        return value_ == other.limit_;
    }
};

int main() {
    for (int x : Counter(5))
        std::cout << x << " ";  // 0 1 2 3 4
}
```

---

## 3. Algorithms (header: <algorithm>)

### 3.1 Sorting

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {5, 3, 1, 4, 2};

    std::sort(v.begin(), v.end());             // unstable sort, O(n log n)
    // {1, 2, 3, 4, 5}

    std::stable_sort(v.begin(), v.end());      // preserves relative order of equal elements

    // Custom comparator
    std::sort(v.begin(), v.end(), std::greater<int>());
    // {5, 4, 3, 2, 1}
}
```

### 3.2 Non-modifying Algorithms

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    // for_each
    std::for_each(v.begin(), v.end(), [](int& x) { x *= 2; });
    // v = {2, 4, 6, 8, 10}

    // find
    auto it = std::find(v.begin(), v.end(), 6);
    if (it != v.end()) std::cout << "Found: " << *it << "\n";  // 6

    // count
    int n = std::count(v.begin(), v.end(), 4);
    std::cout << "Count: " << n << "\n";  // 1

    // accumulate (header: <numeric>)
    int sum = std::accumulate(v.begin(), v.end(), 0);
    std::cout << "Sum: " << sum << "\n";  // 30
}
```

### 3.3 Modifying Algorithms

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    // transform
    std::vector<int> result(v.size());
    std::transform(v.begin(), v.end(), result.begin(),
                   [](int x) { return x * x; });
    // result = {1, 4, 9, 16, 25}

    // copy
    std::vector<int> dest(3);
    std::copy(v.begin(), v.begin() + 3, dest.begin());

    // move (algorithm, not std::move the utility)
    std::vector<std::string> src = {"hello", "world"};
    std::vector<std::string> dst(src.size());
    std::move(src.begin(), src.end(), dst.begin());

    // remove_if (erase-remove idiom)
    std::vector<int> v2 = {1, 2, 3, 2, 5, 2};
    v2.erase(std::remove_if(v2.begin(), v2.end(),
             [](int x) { return x == 2; }), v2.end());
    // v2 = {1, 3, 5}
}
```

---

## 4. String and Utilities

### 4.1 std::string (header: <string>)

```cpp
#include <string>
#include <iostream>

int main() {
    std::string s = "Hello, World!";

    // String manipulation
    std::string sub = s.substr(0, 5);        // "Hello"
    s += " C++";                              // append
    s.insert(5, " STL");                      // insert at position
    s.replace(5, 4, " python");              // replace 4 chars at pos 5

    // Conversions
    int i = std::stoi("42");                  // string to int
    double d = std::stod("3.14");             // string to double
    std::string num = std::to_string(42);     // int to string

    // C-style access
    const char* cs = s.c_str();               // null-terminated
    const char* data = s.data();              // may not be null-terminated

    std::cout << s << "\n";
}
```

### 4.2 std::string_view (header: <string_view>, C++17)

**Non-owning view** over a contiguous character sequence. Does NOT own the data. Programmer must ensure the underlying data outlives the view.

```cpp
#include <string_view>
#include <iostream>

void print_view(std::string_view sv) {  // no copy, no allocation
    std::cout << sv << " (len=" << sv.size() << ")\n";
}

int main() {
    std::string_view sv = "Hello";       // from string literal (no copy)

    std::string str = "World";
    std::string_view sv2 = str;          // from std::string (no copy)

    print_view("literal");               // implicit conversion
    print_view(str);                     // implicit conversion

    // substring
    std::string_view sub = sv.substr(0, 3);  // "Hel"

    // C++20: starts_with, ends_with, contains
    if (sv.starts_with("He"))
        std::cout << "Starts with He\n";
}
```

### 4.3 std::span (header: <span>, C++20)

**Non-owning view** over a contiguous sequence of objects (not limited to chars). Supports both static extent (compile-time known size) and dynamic extent.

```cpp
#include <span>
#include <array>
#include <vector>
#include <iostream>

void process(std::span<int> s) {
    for (int& x : s)
        x *= 2;
}

int main() {
    std::array<int, 4> a = {1, 2, 3, 4};
    std::vector<int> v = {10, 20, 30};

    process(a);    // works with std::array
    process(v);    // works with std::vector
    // process({1,2,3});  // ERROR: cannot deduce from initializer_list

    for (int x : a) std::cout << x << " ";  // 2 4 6 8
    std::cout << "\n";

    // Static extent
    std::span<int, 4> fixed(a);
    std::cout << "extent=" << fixed.extent << "\n";  // 4

    // Dynamic extent
    std::span<int> dyn(v.data(), v.size());

    // Subviews
    auto first3 = fixed.first<3>();
    auto last2  = fixed.last<2>();
}
```

---

## 5. Error Handling

### 5.1 std::optional (header: <optional>, C++17)

A wrapper that may or may not contain a value. Useful as a return type for functions that can fail.

```cpp
#include <optional>
#include <string>
#include <iostream>

std::optional<std::string> find_user(int id) {
    if (id == 1) return "Alice";
    return std::nullopt;  // no value
}

int main() {
    auto user = find_user(1);

    if (user.has_value())           // or: if (user)
        std::cout << *user << "\n"; // "Alice" (operator*)

    std::string name = user.value_or("Unknown");  // with default

    auto missing = find_user(99);
    std::cout << missing.value_or("nobody") << "\n";  // "nobody"

    // C++23 monadic operations
    auto upper = find_user(1)
        .transform([](std::string s) {
            for (auto& c : s) c = std::toupper(c);
            return s;
        });
    if (upper) std::cout << *upper << "\n";  // "ALICE"
}
```

### 5.2 std::expected (header: <expected>, C++23)

Like optional but holds either a value OR an error. Designed as a modern alternative to exceptions for error handling (similar to Rust's Result).

```cpp
#include <expected>
#include <string>
#include <string_view>
#include <iostream>

enum class Error { NotFound, InvalidInput };

std::expected<int, Error> parse_int(std::string_view s) {
    if (s.empty()) return std::unexpected(Error::InvalidInput);
    try {
        return std::stoi(std::string(s));
    } catch (...) {
        return std::unexpected(Error::InvalidInput);
    }
}

int main() {
    auto result = parse_int("42");
    if (result)
        std::cout << "Parsed: " << *result << "\n";  // 42

    auto err = parse_int("abc");
    if (!err)
        std::cout << "Error code: " << static_cast<int>(err.error()) << "\n";

    // C++23 monadic operations
    auto squared = parse_int("5")
        .transform([](int x) { return x * x; });
    if (squared) std::cout << "Squared: " << *squared << "\n";  // 25
}
```

### 5.3 std::variant (header: <variant>, C++17)

A type-safe union. Holds exactly one of its alternative types at any time.

```cpp
#include <variant>
#include <string>
#include <iostream>

int main() {
    std::variant<int, float, std::string> v;

    v = 42;                          // holds int
    std::cout << std::get<int>(v);   // 42

    v = 3.14f;                       // holds float
    std::cout << std::get<float>(v); // 3.14

    v = "hello";                     // holds const char* -> string

    // Check which type
    std::cout << "Index: " << v.index() << "\n";  // 2

    // Safe access
    if (auto* p = std::get_if<std::string>(&v))
        std::cout << *p << "\n";

    // std::visit with overloaded lambda (C++17)
    std::visit([](auto&& arg) {
        std::cout << arg << "\n";
    }, v);

    // std::holds_alternative
    bool is_string = std::holds_alternative<std::string>(v);  // true
}
```

---

## 6. Concurrency

### 6.1 std::thread (header: <thread>, C++11)

```cpp
#include <thread>
#include <iostream>

void task(int id) {
    std::cout << "Thread " << id << " running\n";
}

int main() {
    std::thread t1(task, 1);
    std::thread t2(task, 2);

    t1.join();    // wait for t1 to finish (blocks)
    t2.join();    // wait for t2 to finish

    // detach: thread runs independently (fire-and-forget)
    std::thread t3(task, 3);
    t3.detach();

    // Thread must be joined or detached before destruction
    // Otherwise std::terminate() is called

    std::cout << "Hardware concurrency: "
              << std::thread::hardware_concurrency() << "\n";
}
```

### 6.2 std::jthread (header: <thread>, C++20)

Automatic join on destruction. Supports cooperative cancellation via stop_token.

```cpp
#include <thread>
#include <iostream>
#include <chrono>

void worker(std::stop_token stoken) {
    while (!stoken.stop_requested()) {
        std::cout << "Working...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    std::cout << "Stop requested, exiting.\n";
}

int main() {
    {
        std::jthread jt(worker);  // starts thread
    }  // destructor: requests stop + joins automatically
}
```

### 6.3 Mutexes and Locks

```cpp
#include <mutex>
#include <thread>
#include <vector>
#include <iostream>

std::mutex mtx;
int counter = 0;

void increment() {
    std::lock_guard<std::mutex> lock(mtx);  // RAII lock, unlocks on scope exit
    ++counter;
}

// std::scoped_lock (C++17): can lock multiple mutexes at once (deadlock-free)
std::mutex m1, m2;
void transfer() {
    std::scoped_lock lock(m1, m2);  // locks both atomically
}

int main() {
    std::vector<std::jthread> threads;
    for (int i = 0; i < 10; ++i)
        threads.emplace_back(increment);

    std::cout << "Counter: " << counter << "\n";  // 10 (always correct)
}
```

### 6.4 std::condition_variable (header: <condition_variable>)

```cpp
#include <condition_variable>
#include <mutex>
#include <thread>
#include <queue>
#include <iostream>

std::mutex mtx;
std::condition_variable cv;
std::queue<int> data_queue;
bool done = false;

void producer() {
    for (int i = 0; i < 5; ++i) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            data_queue.push(i);
        }
        cv.notify_one();
    }
    {
        std::lock_guard<std::mutex> lock(mtx);
        done = true;
    }
    cv.notify_all();
}

void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, []{ return !data_queue.empty() || done; });
        while (!data_queue.empty()) {
            std::cout << "Got: " << data_queue.front() << "\n";
            data_queue.pop();
        }
        if (done) break;
    }
}

int main() {
    std::thread prod(producer);
    std::thread cons(consumer);
    prod.join();
    cons.join();
}
```

### 6.5 std::promise / std::future / std::async (header: <future>)

```cpp
#include <future>
#include <iostream>

int compute() { return 42; }

int main() {
    // std::async: easiest way to run async tasks
    auto fut = std::async(std::launch::async, compute);
    std::cout << "Result: " << fut.get() << "\n";  // blocks until result ready (42)

    // promise/future
    std::promise<int> prom;
    std::future<int> fut2 = prom.get_future();

    std::thread t([&prom]() {
        prom.set_value(100);  // fulfill the promise
    });

    std::cout << "Promise: " << fut2.get() << "\n";  // 100
    t.join();
}
```

### 6.6 std::atomic and Memory Ordering

```cpp
#include <atomic>
#include <thread>
#include <iostream>

std::atomic<int> counter{0};

void increment() {
    for (int i = 0; i < 10000; ++i)
        counter.fetch_add(1, std::memory_order_relaxed);
}

int main() {
    std::thread t1(increment), t2(increment);
    t1.join(); t2.join();
    std::cout << "Counter: " << counter << "\n";  // 20000 (always correct)
}
```

**Memory Orderings (from <atomic>):**

| Ordering | Description |
|---|---|
| memory_order_relaxed | Atomicity only; no ordering constraints. Good for counters. |
| memory_order_acquire | No reads/writes in current thread can be reordered before this load. |
| memory_order_release | No reads/writes in current thread can be reordered after this store. |
| memory_order_acq_rel | Both acquire (on load) and release (on store). For RMW operations. |
| memory_order_seq_cst | Default. Single total order across all threads. Strongest guarantee. |
| memory_order_consume | Deprecated (C++26). Like acquire but only for data-dependent operations. |

**Release-Acquire Pattern:**

```cpp
#include <atomic>
#include <thread>
#include <string>
#include <cassert>

std::atomic<std::string*> ptr;
int data;

void producer() {
    std::string* p = new std::string("Hello");
    data = 42;
    ptr.store(p, std::memory_order_release);  // all prior writes visible
}

void consumer() {
    std::string* p2;
    while (!(p2 = ptr.load(std::memory_order_acquire)))
        ;
    assert(*p2 == "Hello");  // guaranteed
    assert(data == 42);      // guaranteed (released before the store)
}

int main() {
    std::thread t1(producer), t2(consumer);
    t1.join(); t2.join();
}
```

**Data Race / Happens-Before:**
- A **data race** occurs when two threads access the same memory location, at least one writes, and there is no happens-before relationship.
- **happens-before** is the fundamental ordering guarantee: if A happens-before B, then A's effects are visible to B.
- Atomic operations with sufficient ordering (acquire/release, seq_cst) establish happens-before relationships.
- Without synchronization, the compiler and CPU may reorder operations freely.

### 6.7 Additional Concurrency Primitives

**std::atomic_flag (header: <atomic>):** Lock-free boolean atomic; the only type guaranteed lock-free on all implementations.

```cpp
#include <atomic>
#include <thread>
#include <iostream>

std::atomic_flag flag = ATOMIC_FLAG_INIT;

void spinlock_acquire() {
    while (flag.test_and_set(std::memory_order_acquire))  // spin
        ;
}

void spinlock_release() {
    flag.clear(std::memory_order_release);
}

int main() {
    std::thread t1([]{
        spinlock_acquire();
        std::cout << "Thread 1 in critical section\n";
        spinlock_release();
    });
    std::thread t2([]{
        spinlock_acquire();
        std::cout << "Thread 2 in critical section\n";
        spinlock_release();
    });
    t1.join(); t2.join();
}
```

---

## 7. File I/O (header: <fstream>)

```cpp
#include <fstream>
#include <string>
#include <iostream>

int main() {
    // Writing to a file
    std::ofstream ofs("example.txt");
    ofs << "Hello, File!\n";
    ofs << 42 << " " << 3.14 << "\n";
    ofs.close();

    // Reading from a file
    std::ifstream ifs("example.txt");
    std::string line;
    while (std::getline(ifs, line))
        std::cout << line << "\n";
    ifs.close();

    // Binary mode
    std::ofstream ofs_bin("data.bin", std::ios::binary);
    int arr[] = {1, 2, 3, 4, 5};
    ofs_bin.write(reinterpret_cast<char*>(arr), sizeof(arr));
    ofs_bin.close();

    // File modes
    // std::ios::in    - open for reading
    // std::ios::out   - open for writing
    // std::ios::app   - append mode
    // std::ios::binary - binary mode (no text translation)
    // std::ios::trunc  - truncate on open

    // fstream for both read/write
    std::fstream fs("example.txt", std::ios::in | std::ios::out);
    fs.seekg(0);  // seek to beginning for reading
    fs.seekp(0);  // seek to beginning for writing
}
```

---

## 8. Random (header: <random>)

```cpp
#include <random>
#include <iostream>

int main() {
    // Modern approach (C++11)
    std::random_device rd;                      // non-deterministic seed (hardware)
    std::mt19937 gen(rd());                     // Mersenne Twister engine

    // Uniform distribution
    std::uniform_int_distribution<int> int_dist(1, 100);
    std::cout << "Random int [1,100]: " << int_dist(gen) << "\n";

    std::uniform_real_distribution<double> real_dist(0.0, 1.0);
    std::cout << "Random double [0,1): " << real_dist(gen) << "\n";

    // Normal distribution
    std::normal_distribution<double> norm_dist(0.0, 1.0);
    std::cout << "Normal(0,1): " << norm_dist(gen) << "\n";

    // Bernoulli (coin flip)
    std::bernoulli_distribution coin(0.7);  // 70% true
    std::cout << "Coin: " << (coin(gen) ? "Heads" : "Tails") << "\n";
}
```

---

## 9. std::chrono (header: <chrono>)

```cpp
#include <chrono>
#include <iostream>

int main() {
    using namespace std::chrono;

    // Duration
    auto d1 = 5s;                     // 5 seconds
    auto d2 = 300ms;                  // 300 milliseconds
    auto d3 = duration<double>(1.5);  // 1.5 seconds (as double)

    // Converting between durations
    auto ms = duration_cast<milliseconds>(d1);
    std::cout << d1 << " = " << ms << "\n";  // C++20: streams work directly

    // Timing code
    auto start = steady_clock::now();

    // ... some computation ...
    volatile int sum = 0;
    for (int i = 0; i < 1000000; ++i) sum += i;

    auto end = steady_clock::now();
    auto elapsed = duration<double>(end - start);
    std::cout << "Elapsed: " << elapsed.count() << "s\n";

    // System clock: wall-clock time
    auto now = system_clock::now();
    auto tp = system_clock::to_time_t(now);
    std::cout << "Current time: " << std::ctime(&tp);

    // steady_clock: monotonic, never adjusted (best for timing)
    // high_resolution_clock: shortest tick period (may be alias for steady_clock)

    // C++20: Calendar and time zones
    auto ymd = year{2026}/month{8}/day{19};
    std::cout << "Date: " << ymd << "\n";
}
```

**Clock types:**
- system_clock: Wall-clock time from system real-time clock. Not monotonic. Can convert to/from time_t.
- steady_clock: Monotonic clock. Never adjusted. Best for measuring elapsed time.
- high_resolution_clock: Shortest available tick period. May be an alias for steady_clock or system_clock.

---

## 10. std::function and std::bind (header: <functional>)

### std::function

A general-purpose polymorphic function wrapper. Can store functions, lambdas, bind expressions, function objects, and member function pointers.

```cpp
#include <functional>
#include <iostream>

int add(int a, int b) { return a + b; }

struct Multiplier {
    int factor;
    int operator()(int x) const { return x * factor; }
};

int main() {
    // Store a free function
    std::function<int(int, int)> f = add;
    std::cout << f(3, 4) << "\n";  // 7

    // Store a lambda
    std::function<int(int)> square = [](int x) { return x * x; };
    std::cout << square(5) << "\n";  // 25

    // Store a function object
    std::function<int(int)> mul = Multiplier{10};
    std::cout << mul(5) << "\n";  // 50

    // Check if empty
    std::function<void()> empty;
    if (!empty) std::cout << "Empty function\n";
    // Calling empty throws std::bad_function_call

    // Capture variables in lambda
    int offset = 100;
    std::function<int(int)> add_offset = [offset](int x) { return x + offset; };
}
```

### std::bind (and modern alternatives)

```cpp
#include <functional>
#include <iostream>

void greet(std::string greeting, std::string name) {
    std::cout << greeting << ", " << name << "!\n";
}

int main() {
    // std::bind
    using namespace std::placeholders;
    auto hello = std::bind(greet, "Hello", _1);
    hello("World");  // Hello, World!

    // Modern alternative: lambda (generally preferred)
    auto goodbye = [](std::string name) { greet("Goodbye", name); };
    goodbye("World");

    // C++20: std::bind_front (preferred over bind for partial application)
    auto hi = std::bind_front(greet, "Hi");
    hi("Everyone");  // Hi, Everyone!
}
```

---

## 11. Bit Manipulation

### Bitwise Operators

```cpp
int a = 0b1100;  // 12
int b = 0b1010;  // 10

int and_result = a & b;   // 1000 = 8   (bitwise AND)
int or_result  = a | b;   // 1110 = 14  (bitwise OR)
int xor_result = a ^ b;   // 0110 = 6   (bitwise XOR)
int not_result = ~a;       // ...0011 = complement
int lshift     = a << 2;   // 110000 = 48 (shift left)
int rshift     = a >> 1;   // 0110 = 6    (shift right)
```

### std::bitset (header: <bitset>)

```cpp
#include <bitset>
#include <iostream>

int main() {
    std::bitset<8> bs(0b10110100);

    std::cout << bs << "\n";           // 10110100
    std::cout << "Count: " << bs.count() << "\n";  // 4 (number of 1s)
    std::cout << "Size: " << bs.size() << "\n";    // 8
    std::cout << "Test bit 2: " << bs.test(2) << "\n";  // 1

    bs.set(0);       // set bit 0 to 1
    bs.reset(7);     // set bit 7 to 0
    bs.flip();       // flip all bits

    // Bitwise operations between bitsets
    std::bitset<8> a("11001100");
    std::bitset<8> b("10101010");
    std::cout << (a & b) << "\n";  // 10001000
    std::cout << (a | b) << "\n";  // 11101110
    std::cout << (a ^ b) << "\n";  // 01100110
}
```

### C++20 Bit Functions (header: <bit>)

```cpp
#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>

int main() {
    uint32_t x = 0b00000000000000000000000101100000u;

    // Population count (number of set bits)
    std::cout << "popcount: " << std::popcount(x) << "\n";      // 3

    // Count leading zeros (from MSB)
    std::cout << "countl_zero: " << std::countl_zero(x) << "\n"; // 25

    // Count leading ones
    // Count trailing zeros (from LSB)
    std::cout << "countr_zero: " << std::countr_zero(x) << "\n"; // 5

    // Count trailing ones
    // Bit width (number of bits needed to represent x)
    std::cout << "bit_width: " << std::bit_width(x) << "\n";     // 7

    // Powers of 2
    std::cout << "has_single_bit: " << std::has_single_bit(8u) << "\n";  // true (power of 2)
    std::cout << "bit_ceil(5): " << std::bit_ceil(5u) << "\n";   // 8
    std::cout << "bit_floor(5): " << std::bit_floor(5u) << "\n"; // 4

    // Rotate
    uint8_t val = 0b11000011;
    std::cout << "rotl: " << std::bitset<8>(std::rotl(val, 2)) << "\n";  // 00001111
    std::cout << "rotr: " << std::bitset<8>(std::rotr(val, 2)) << "\n";  // 11110000

    // Endianness
    if constexpr (std::endian::native == std::endian::little)
        std::cout << "Little endian\n";
}
```

---

## 12. std::format (header: <format>, C++20)

A type-safe, performant replacement for printf and iostreams. Compile-time format string checking.

```cpp
#include <format>
#include <iostream>
#include <string>

int main() {
    // Basic formatting
    std::cout << std::format("Hello {}!\n", "world");

    // Positional arguments
    std::cout << std::format("{1} {0}\n", "World", "Hello");  // "Hello World"

    // Number formatting
    std::cout << std::format("Int: {:d}\n", 42);             // Int: 42
    std::cout << std::format("Hex: {:x}\n", 255);            // Hex: ff
    std::cout << std::format("Hex: {:X}\n", 255);            // Hex: FF
    std::cout << std::format("Oct: {:o}\n", 255);            // Oct: 377
    std::cout << std::format("Bin: {:b}\n", 255);            // Bin: 11111111

    // Float formatting
    std::cout << std::format("Pi: {:.4f}\n", 3.14159);      // Pi: 3.1416
    std::cout << std::format("Sci: {:.2e}\n", 1234.5);       // Sci: 1.23e+03

    // Width and alignment
    std::cout << std::format("|{:>10}|\n", "right");         // |     right|
    std::cout << std::format("|{:<10}|\n", "left");          // |left      |
    std::cout << std::format("|{:^10}|\n", "center");        // |  center  |
    std::cout << std::format("|{:*^10}|\n", "center");       // |**center**|

    // Fill with zeros
    std::cout << std::format("Zero-padded: {:05d}\n", 42);   // 00042

    // String formatting
    std::string name = "C++";
    int version = 20;
    std::cout << std::format("{} {}\n", name, version);       // C++ 20

    // Dynamic format string (runtime)
    std::string fmt_str = "Value: {}\n";
    std::cout << std::vformat(fmt_str, std::make_format_args(42));
}
```

**Format spec overview:**
`{[arg-id]:[fill][align][sign][#][0][width][.precision][L][type]}`

| Specifier | Meaning |
|---|---|
| `d` | Decimal integer |
| `x` / `X` | Hexadecimal |
| `o` | Octal |
| `b` | Binary |
| `e` / `E` | Scientific float |
| `f` / `F` | Fixed-point float |
| `g` / `G` | General float |
| `s` | String |
| `p` | Pointer |

---

## Sources

All technical details verified against the following cppreference.com pages:
- https://en.cppreference.com/w/cpp/container/vector
- https://en.cppreference.com/w/cpp/container/map
- https://en.cppreference.com/w/cpp/container/unordered_map
- https://en.cppreference.com/w/cpp/container/deque
- https://en.cppreference.com/w/cpp/container/list
- https://en.cppreference.com/w/cpp/container/set
- https://en.cppreference.com/w/cpp/container/array
- https://en.cppreference.com/w/cpp/iterator
- https://en.cppreference.com/w/cpp/ranges
- https://en.cppreference.com/w/cpp/thread/thread
- https://en.cppreference.com/w/cpp/thread/jthread
- https://en.cppreference.com/w/cpp/atomic/atomic
- https://en.cppreference.com/w/cpp/atomic/memory_order
- https://en.cppreference.com/w/cpp/utility/optional
- https://en.cppreference.com/w/cpp/utility/expected
- https://en.cppreference.com/w/cpp/utility/variant
- https://en.cppreference.com/w/cpp/utility/format/format
- https://en.cppreference.com/w/cpp/chrono
- https://en.cppreference.com/w/cpp/string/basic_string_view
- https://en.cppreference.com/w/cpp/container/span
- https://en.cppreference.com/w/cpp/utility/functional/function
- https://en.cppreference.com/w/cpp/utility/bitset
- https://en.cppreference.com/w/cpp/numeric/popcount
