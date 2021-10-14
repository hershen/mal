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
| `def!` | A new `symbol` name and an expression | Defines a new `symbol` name with the value of the evaluated expression | `(def! new (+ 1 2))` &rArr; `3` <br /> `new` &rArr; `3` |
| `let*` | A `list` with key value pairs, and an expression | The expression is evaluated using the additional `symbol`s defined in the `list` | `(let* (c 2) c)` &rArr; `2` <br /> `(let* (z (+ 2 3)) (+ 1 z))` &rArr; `6` |
| `do` | A series of elements | Evaluate all the elements, returning the last evaluated element | `(do (def! a 6) 7 (+ a 8))` &rArr; `14` |
| `if` | a condition, an expression for true, and an optional expression for false | The evaluated expression for true if the condition evaluates to anything other than `nil` or `false`, or the evaluated expression for false, otherwise. If the condition evaluates to false and there is no expression for false, returns `nil`. | `(if true (+ 0 1) (+ 1 1))` &rArr; `1` <br /> `(if false (+ 0 1) (+ 1 1))` &rArr; `2` <br /> `(if false (+ 0 1))` &rArr; `nil` |
| `fn*` | A `list` of `symbol`s and an expression | A function object that evaluates the expression with the symbols from the `list` as arguments. A function object is meant to be called with a series of expressions matching the arguments. | `( (fn* (a b) (+ b a)) 3 4)` &rArr; `7` <br /> `(def! fib (fn* (N) (if (= N 0) 1 (if (= N 1) 1 (+ (fib (- N 1)) (fib (- N 2)))))))` &rArr; `#<function>` <br /> `(fib 5)` &rArr; `8` |
| `slurp` | A string that represents a file name | The contents of the file as a string | `(slurp "hello-world.txt")` &rArr; `"hello world!\n"`|
| `read-string` |  | | |
| `eval` | A `mal` expression | The evaluated `mal` expression | `(def! expression (list + 1 2))` <br /> `(eval expression)` &rArr; `3` |
| `load-file` | A filename as a string | The `mal` code in the file is processed as if it was entered into the interpreter | `(load-file "increase4.mal")` <br /> `(increase4 1)` &rArr; `5` |
| `atom` | A `mal` value | An atom that references the `mal` value | `(def! a (atom 2))`|
| `atom?` | A `mal` value | Returns true if the value is an atom | `(def! a (atom 2))` <br /> `(atom? a)` &rArr; `true` |
| `deref` | An atom | The value referenced by the atom. The `@` macro has the same functionality. | `(def! a (atom 2))` <br /> `(deref a)` &rArr; `2` <br /> `@a` &rArr; `2` |
| `cons` | A `mal` type and (a List or Vector) | A new List composed of the `mal` type and the elements of the List or the Vector | `(cons 1 (list 1 2 3))` &rArr; `(1 1 2 3)` |
| `concat` | 0 or combinations of Lists and Vectors | A new list containing the elements of the input Lists and Vectors | `(concat (list 1 2) (list 3 4))` &rArr; `(1 2 3 4)` |
| `quote` | A `mal` type | The `mal` type. If the `mal` type is not defined, treats it like a `symbol` and returns the name of the `symbol`. | `(quote abc)` &rArr; `abc` |
| `quasiquote` | A `mal` type | The same as `quote`, unless `mal` type is a list starting with `unquote` or `splice-unquote`. These are detailed below. | `(quasiquote abc)` &rArr; `abc`  |
| `unquote` | A `mal` type | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the evaluated form of the argument. | `(def! lst (quote (b c)))` &rArr; `(b c)`, `(quasiquote (a (unquote lst) d))` &rArr; `(a (b c) d)` |
| `splice-unquote` | A List | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the contents of the List. | `(def! lst (quote (b c)))` &rArr; `(b c)`, `(quasiquote (a (splice-unquote lst) d))` &rArr; `(a b c d)` |
| `vec` | A list or a vector | A vector with the same elements as in the input | `(vec (list 1 2))` &rArr; `[1 2]` |
| `defmacro` | A new `symbol` name and an expression | A macro - a new piece of code. The arguments are evaluated lazily, when they are needed. So this can be never (for example, for the second argument of an `or`. A regular `def!` greedily evaluates all arguments. The arguments of a macro don't have to be valid expressions. They have to be valid only when the macro is called. | ``(defmacro! twicem (fn* (e) `(do ~e ~e)))`` &rArr; `#<function>` <br /> `(twicem (prn "foo"))` &rArr; `foo foo nil`. <br /> A regular `def!`: ``(def! twice (fn* (e) `(do ~e ~e)))`` &rArr; `#<function>` <br />  `(twice (prn "foo"))` &rArr; `foo (do nil nil)` |
| `(try* A (catch* B C))` | Expression `A`, `B`, and `C` | Expression `A` is evaluated. If an exception is thrown, expression `C` is evaluated with `B` bound to the value of the thrown exception. | `(try* abc (catch* exc (prn "exc is:" exc)))` &rArr; `"exc is:" "'abc' not found"` |
| `throw` | A value | Raises the value as an exception | `(try* (throw "my exception") (catch* exc (prn "exc:" exc)))` &rArr; `"exc:" "my exception"` |
| `apply` | A function and one or more arguments | The last argument is a list or vector. The arguments are concatenated and passed as arguments to the function. | `(apply (fn* (a b c) (+ a (+ b c))) 1 (list 2 3))` &rArr; `6` |
| `map` | A function and a list or vector | Applies the function to each element of the input. Returns a list of the results. | `(map (fn* (a) (* 2 a)) [1 2 3])` &rArr; `(2 4 6)` |
| `nth` | A List or Vector and an index number | The element in the List or Vector at position index | `(nth (list 1 2) 1)` &rArr; `2` |
| `first` | A List or Vector | The first element in the List or Vector. If the List or Vectors are empty, or are Nil, Nil is returned. | `(first (list 7 8 9))` &rArr; `7` <br /> `(first nil)` &rArr; `nil` |
| `rest` | A List or Vector | A new List containing all the elements of the List or Vector, except the first. If the List or Vectors are empty, or are Nil, an empty List is returned. | `(rest (list 7 8 9))` &rArr; `(8 9)` <br /> `(rest nil)` &rArr; `()` |
| `cond` | A List containing an even number of elements | The elements are treated in pairs. The first element of a pair is a condition. The second is a value. `cond` returns the first value for which the condition is true. | `(cond false 7 (= 2 2) 8 "else" 9)` &rArr; `8` <br /> `(cond false 7 (= 2 5) 8 "else" 9)` &rArr; `9` |
| `assoc` | A `hash-map` and another even number of arguments | A new `hash-map` where the arguments are interpreted as key-value pairs and merged into the `hash-map` | `(assoc {1 2} 3 4)` &rArr; `{3 4 1 2}` |
| `dissoc` | A `hash-map` and 0 or more keys | A new `hash-map` where the given keys are removed from the `hash-map`. Missing keys are ignored. | `(dissoc {1 2 3 4} 3 5)` &rArr; `{1 2}` |
| `get` | A `hash-map` and a key | The value associated with the key in the `hash-map`. If the key is not in the `hash-map`, `nil` is returned. | `(get {1 2 3 4} 3)` &rArr; `4` |
| `keys` | A `hash-map` | A `list` of all the keys in the `hash-map`. | `(keys {1 2 3 4})` &rArr; `(1 3)` |
| `vals` | A `hash-map` | A `list` of all the values in the `hash-map`. | `(vals {1 2 3 4})` &rArr; `(2 4)` |
| `vec` | A List or a Vector | A vector with the same elements as in the input | `(vec (list 1 2))` &rArr; `[1 2]` |
| `list` | 0 or more arguments | A `list` with the arguments as its elements | `(list 1 2 3)` &rArr; `(1 2 3)` |
| `vector` | 0 or more arguments | A `vector` with the arguments as its elements | `(vector 1 2 3)` &rArr; `[1 2 3]` |
| `hash-map` | An even number of arguments | A `hash-map` where the keys are the odd arguments and the values are the even elements | `(hash-map 1 2 3 4)` &rArr; `{1 2 3 4}` |
| `symbol` | A string | A `symbol` with the string as its name | `(symbol "abc")` &rArr; `abc` |
| `keyword` | A string | A `keyword` with the string as its name | `(keyword "abc")` &rArr; `:abc` |
| `nil?` | A value | `true` if the value is `nil` | `(nil? nil)` &rArr; `true` |
| `string?` | A value | `true` if the value is a `string` | `(string? "abc")` &rArr; `true` |
| `number?` | A value | `true` if the value is a `number` | `(number? 123)` &rArr; `true` |
| `fn?` | A value | `true` if the value is a `function` | `(fn? +)` &rArr; `true` |
| `macro?` | A value | `true` if the value is a `macro` | `(defmacro! a (fn* () ()))` <br/ > `(macro? a)` &rArr; `true` |
| `true?` | A value | `true` if the value is `true` | `(true? false)` &rArr; `false` |
| `false?` | A value | `true` if the value is `false` | `(false? false)` &rArr; `true` |
| `symbol?` | A value | `true` if the value is a `symbol` | `(symbol? "abc")` &rArr; `false` |
| `keyword?` | A value | `true` if the value is a `keyword` | `(keyword? (keyword "abc"))` &rArr; `true` |
| `vector?` | A value | `true` if the value is a `vector` | `(vector? (list 1 2 3))` &rArr; `false` |
| `sequential?` | A value | `true` if the value is a `list` or a `vector` | `(sequential? (list 1 2 3))` &rArr; `true` |
| `map?` | A value | `true` if the value is a `hash-map` | `(map? (hash-map 1 2))` &rArr; `true` |
| `contains?` | A `hash-map` and a key | `true` if the key is a in the `hash-map` | `(contains? {1 2 3 4} 3)` &rArr; `true` |
| `readline` | A `string` | Prints the `string`, reads text from the user and prints it back | |

## Reader macro

| Function | Explanation | Example |
|  ---     | ---         | ---     |
| `'` | Equivalent to `quote` | `'(list 1 2)` &rArr; `(list 1 2)` |
| ``` `` | Equivalent to `quasiquote` | `(1 2 (3 4))` &rArr; `(1 2 (3 4))` |
| `~` | Equivalent to `unquote` | `(def! a 8)` &rArr; `8` <br /> `` `(1 ~a 3)`` &rArr; `(1 8 3)` |
| `@` | Equivalent to `deref` | `(def! a (atom 2))` <br /> `@a` &rArr; `2` |
| `~@` | Equivalent to `splice-unquote` | `(def! c (list 2))` &rArr; `(2)` <br /> `` `(1 ~@c 3)`` &rArr; `(1 2 3)` |



