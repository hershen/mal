# `mal` in Python3

This project is an implementation of an interpreter for the lisp-like [mal](https://github.com/kanaka/mal) programming language in Python3.

[mal](https://github.com/kanaka/mal) is a lisp-like language. It provides a guide on how to go about writing a new interpreter implantation. 
This project follows that guide and implements an interpreter in the Python3 language.
Everything in this folder is written as part of this project. Other folders in this repository implement the test infrastructure, and were provided by the `mal` project.

As Python3 has a maximum recursion depth, the implementation incorporates [Tail Call Optimization](https://en.wikipedia.org/wiki/Tail_call) (TCO) which limits growth of the call stack by re-using the last stack frame, when possible. This prevents, for example, a recursion based Fibonacci calculator from exceeding the maximum recursion depth when calculating a large Fibonacci number.

The `mal` language is self-hosting, meaning a `mal` interpreter can run an implementation of a `mal` interpreter written in the `mal` language. All the functional tests can be run in self hosting mode.

## Examples
Some examples of what can be run with the interpreter.

### Calculate the Fibonacci numbers
`(def! fib (fn* (N) (if (= N 0) 0 (if (= N 1) 1 (+ (fib (- N 1)) (fib (- N 2)))))))`

Then:

`(fib 8)` &rArr; `21`

## Requirements
- A Python3 interpreter, version >= 3.6.

For running the tests:

- Ability to process MakeFiles.

## Installation
```
pip3 install mal_python
```

To run the interpreter, run `mal`.

Cross platform - tested on Linux and Windows.

## Running the test suite

- Clone this repository.
- `cd mal`
- `make MAL_IMPL=myPython "test^mal"`

This will run all the functional tests (provided as part of the [mal](https://github.com/kanaka/mal) guide) in self hosting mode (this Python3 interpreter runs an interpreter written in `mal` which runs the tests).

# Language reference

## Types

| Type | Explanation | Example |
| ---  | ---         | ---     |
| `int` | Integer number | `12` |
| `symobl` | Contains a string value | `sym` |
| `keyword` | Similar to `symbol` but instance names start with a `:`. Can be used as `hash-map` keys. | `:kw` |
| `string` | `mal`'s string type | `"str"` |
| `nil` | Similar to Python's `NoneType` | `nil` |
| `true` | `mal`'s true type | `true` |
| `false` | `mal`'s false type | `false` |
| `atom` | Holds a reference to a `mal` type. This is the only mutable `mal` type. | `(atom 2)` |
| `list` | A series of `mal` types, separated by spaces, delimited by brackets (`()`). | `("a" 1)` | 
| `vector` | Similar to `list`s, but use square brackets (`[]`) as delimiters. | `["a" 1]` |
| `hash-map` | Data structure that maps `string`s and `keywords` into other `mal` types. Delimited with curly braces (`{}`). The odd entries are the keys and the even entries are the values. | `{"a" 1 :k "str"}` |

## Comments
Comments are written with `;`. Anything after a `;` is ignored until the end of the line.

## Processing of `mal` types
When a `list` is processed, the first element is invoked or executed on the rest of the elements. For example:

- `(+ 1 2)` &rArr; `3`
- `(+ 2 (* 3 4))` &rArr; `14`

When a `vector` is evaluated, each individual element is evaluated.
When a `hash-map` is evaluated, all the values (odd elements) are evaluated.

| Function | Input | Output/Effects | Example |
|  ---     | ---   | ---    | ---     |
|  |  | | |
| `def!` | A new symbol name and an expression | Defines a new symbol name with the value of the evaluated expression | `(def! new (+ 1 2))` &rArr; `3` <br /> `new` &rArr; `3` |
| `let*` | A `list` with key value pairs, and an expression | The expression is evaluated using the additional symbols defined in the `list` | `(let* (c 2) c)` &rArr; `2` <br /> `(let* (z (+ 2 3)) (+ 1 z))` &rArr; `6` |
| `do` | A series of elements | Evaluate all the elements, returning the last evaluated element | `(do (def! a 6) 7 (+ a 8))` &rArr; `14` |
| `if` | a condition, an expression for true, and an optional expression for false | The evaluated expression for true if the condition evaluates to anything other than `nil` or `false`, or the evaluated expression for false, otherwise. If the condition evaluates to false and there is no expression for false, returns `nil`. | `(if true (+ 0 1) (+ 1 1))` &rArr; `1` <br /> `(if false (+ 0 1) (+ 1 1))` &rArr; `2` <br /> `(if false (+ 0 1))` &rArr; `nil` |
| `fn*` | A `list` of symbols and an expression | A function object that evaluates the expression with the symbols from the `list` as arguments. A function object is meant to be called with a series of expressions matching the arguments. | `( (fn* (a b) (+ b a)) 3 4)` &rArr; `7` <br /> `(def! fib (fn* (N) (if (= N 0) 0 (if (= N 1) 1 (+ (fib (- N 1)) (fib (- N 2)))))))` &rArr; `#<function>` <br /> `(fib 8)` &rArr; `21` |
| `slurp` | A string that represents a file name | The contents of the file as a string | `(slurp "hello-world.txt")` &rArr; `"hello world!\n"`|
| `read-string` |  | | |
| `eval` | A `mal` expression | The evaluated `mal` expression | `(def! expression (list + 1 2))` <br /> `(eval expression)` &rArr; `3` |
| `load-file` | A filename as a string | The `mal` code in the file is processed as if it was entered into the interpreter | `(load-file "increase4.mal")` <br /> `(increase4 1)` &rArr; `5` |
| `atom` | A `mal` value | An atom that references the `mal` value | `(def! a (atom 2))`|
| `atom?` | A `mal` value | Returns true if the value is an atom | `(def! a (atom 2))` <br /> `(atom? a)` &rArr; `true` |
| `deref` | An atom | The value referenced by the atom. The `@` macro has the same functionality. | `(def! a (atom 2))` <br /> `(deref a)` &rArr; `2` <br /> `@a` &rArr; `2` |
| `reset!` | An atom and a value | The atom is modified to reference the new value. The new value is returned. | `(def! a (atom 2))` <br /> `(reset! a 3)` &rArr; `3` <br /> `(deref a)` &rArr; `3` |
| `swap!` | An atom, a function, and zero or more function arguments | The atom's value is set to the result of calling function with the atom's value as the first argument and the optional function arguments as the rest of the arguments. The new value is returned. | `(def! a (atom 2))` <br /> `(swap! a (fn* (x) (+ 1 x)))` &rArr; `3` <br /> `(deref a)` &rArr; `3` |
| `cons` | A `mal` type and (a list or vector) | A new list composed of the `mal` type and the elements of the list or the vector | `(cons 1 (list 1 2 3))` &rArr; `(1 1 2 3)` |
| `concat` | 0 or more combinations of lists and vectors | A new list containing the elements of the input lists and vectors | `(concat (list 1 2) (list 3 4))` &rArr; `(1 2 3 4)` |
| `quote` | A `mal` type | The `mal` type. If the `mal` type is not defined, treats it like a symbol and returns the name of the symbol. | `(quote abc)` &rArr; `abc` |
| `quasiquote` | A `mal` type | The same as `quote`, unless `mal` type is a list starting with `unquote` or `splice-unquote`. These are detailed below. | `(quasiquote abc)` &rArr; `abc`  |
| `unquote` | A `mal` type | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the evaluated form of the argument. | `(def! lst (quote (b c)))` &rArr; `(b c)`, `(quasiquote (a (unquote lst) d))` &rArr; `(a (b c) d)` |
| `splice-unquote` | A list | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the contents of the list. | `(def! lst (quote (b c)))` &rArr; `(b c)`, `(quasiquote (a (splice-unquote lst) d))` &rArr; `(a b c d)` |
| `vec` | A list or a vector | A vector with the same elements as in the input | `(vec (list 1 2))` &rArr; `[1 2]` |
| `defmacro` | | A macro - a new piece of code. The arguments are evaluated lazily, when they are needed. So this can be never (for example, for the second argument of an `or`. A regular `def!` greedily evaluates all arguments. The arguments of a macro don't have to be valid expressions. They have to be valid only when the macro is called. | `(defmacro! twicem (fn* (e) (do ~e ~e)))` &rArr; `#<function>` <br /> `(twicem (prn "foo"))` &rArr; `foo foo nil`. <br /> A regular `def!`: `(def! twice (fn* (e) (do ~e ~e)))` &rArr; `#<function>` <br />  `(twice (prn "foo"))` &rArr; `foo (do nil nil)` |
| `nth` | A list or vector and an index number | The element in the list or vector at position index | `(nth (list 1 2) 1)` &rArr; `2` |
| `first` | A list or vector | The first element in the list or vector. If the list or vectors are empty, or are Nil, Nil is returned. | `(first (list 7 8 9))` &rArr; `7` <br /> `(first nil)` &rArr; `nil` |
| `rest` | A list or vector | A new list containing all the elements of the list or vector, except the first. If the list or vectors are empty, or are Nil, an empty list is returned. | `(rest (list 7 8 9))` &rArr; `(8 9)` <br /> `(rest nil)` &rArr; `()` |
| `cond` | A list containing an even number of elements | The elements are treated in pairs. The first element of a pair is a condition. The second is a value. `cond` returns the first value for which the condition is true. | `(cond false 7 (= 2 2) 8 "else" 9)` &rArr; `8` <br /> `(cond false 7 (= 2 5) 8 "else" 9)` &rArr; `9` |


## Reader macro

| Function | Explanation | Example |
|  ---     | ---         | ---     |
| `'` | Equivalent to `quote` | `'(list 1 2)` &rArr; `(list 1 2)` |
| ``` `` | Equivalent to `quasiquote` | `(1 2 (3 4))` &rArr; `(1 2 (3 4))` |
| `~` | Equivalent to `unquote` | `(def! a 8)` &rArr; `8` <br /> `(1 ~a 3)` &rArr; `(1 8 3)` |
| `@` | Equivalent to `deref` | `(def! a (atom 2))` <br /> `@a` &rArr; `2` |
| `~@` | Equivalent to `splice-unquote` | `(def! c (list 2))` &rArr; `(2)` <br /> `(1 ~@c 3)` &rArr; `(1 2 3)` |



