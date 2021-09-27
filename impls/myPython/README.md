# `mal` in Python3

This project is an implementation of an interpreter for the lisp-like [mal](https://github.com/kanaka/mal) programming language in Python3.

`mal` is a lisp-like language. It's also a project that encourages implementations of interpreters in different programming languages. It provides an outline of how to go about writing an interpreter implantation.

This project follows that guide and implements an interpreter in the Python3 language.
Everything in this folder is written as part of this project. Other folders in this repository implement the test infrastructure, and were provided by the `mal` project.

The implementation incorporates [Tail Call Optimization]() (TCO) to reduce the recursion depth.
## Features

- Tail Call Optimization.

# Language reference

## Types

| Type | Explanation | Example |
| ---  | ---         | ---     |
| `int` | Integer number | `12` |
| `symobl` | Contains a string value | `sym` |
| `keyword` | Similar to `symbol` but instance names start with a `:`. Can be used as `hash-map` keys.
| `string` | `mal`'s string type | `"str"` |
| `nil` | Similar to Python's `NoneType` | `nil` |
| `true` | `mal`'s true type | `true` |
| `false` | `mal`'s false type | `false` |
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

| Function | Input | Output | Example |
|  ---     | ---   | ---    | ---     |
|  |  | | |
| `def!` | A new symbol name and an expression | Defines a new symbol name with the value of the evaluated expression | `(def! new (+ 1 2))` &rArr; `3` <br /> `new` &rArr; `3` |
| `let*` | A `list` with key value pairs, and an expression | The expression is evaluated using the additional symbols defined in the `list` | `(let* (c 2) c)` &rArr; `2` <br /> `(let* (z (+ 2 3)) (+ 1 z))` &rArr; `6` |
| `do` | A series of elements | Evaluate all the elements, returning the last evaluated element | `(do (def! a 6) 7 (+ a 8))` &rArr; `14` |
| `if` | a condition, an expression for true, and an optional expression for false | The evaluated expression for true if the condition evaluates to anything other than `nil` or `false`, or the evalauted expression for false, otherwise. If the condition evaluates to false and there is no expression for false, returns `nil`. | `(if true (+ 0 1) (+ 1 1))` &rArr; `1` <br /> `(if false (+ 0 1) (+ 1 1))` &rArr; `2` <br /> `(if false (+ 0 1))` &rArr; `nil` |
| `fn*` | A `list` of symbols and an expression | A function object that evaluates the expression with the symbols from the `list` as arguments. A function object is meant to be called with a series of expressions matching the arguments. | `( (fn* (a b) (+ b a)) 3 4)` &rArr; `7` <br /> `(def! fib (fn* (N) (if (= N 0) 1 (if (= N 1) 1 (+ (fib (- N 1)) (fib (- N 2)))))))` &rArr; `#<function>` <br /> `(fib 5)` &rArr; `8` |
| `cons` | A `mal` type and (a List or Vector) | A new List composed of the `mal` type and the elements of the List or the Vector | `(cons 1 (list 1 2 3))` &rArr; `(1 1 2 3)` |
| `concat` | 0 or combinations of Lists and Vectors | A new list containing the elements of the input Lists and Vectors | `(concat (list 1 2) (list 3 4))` &rArr; `(1 2 3 4)` |
| `quote` | A `mal` type | The `mal` type. If the `mal` type is not defined, treats it like a Symbol and returns the name of the Symbol. | `(quote abc)` &rArr; `abc` |
| `quasiquote` | A `mal` type | The same as `quote`, unless `mal` type is a list starting with `unquote` or `splice-unquote`. These are detailed below. | `(quasiquote abc)` &rArr; `abc`  |
| `unquote` | A `mal` type | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the evaluated form of the argument. | `(def! lst (quote (b c)))` &rArr; `(b c)`, `(quasiquote (a (unquote lst) d))` &rArr; `(a (b c) d)` |
| `splice-unquote` | A List | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the contents of the List. | `(def! lst (quote (b c)))` &rArr; `(b c)`, `(quasiquote (a (splice-unquote lst) d))` &rArr; `(a b c d)` |
| `vec` | A List or a Vector | A vector with the same elements as in the input | `(vec (list 1 2))` &rArr; `[1 2]` |
| `defmacro` | | A macro - a new piece of code. The arguments are evaluated lazily, when they are needed. So this can be never (for example, for the second argument of an `or`. A regular `def!` greedily evaluates all arguments. The arguments of a macro don't have to be valid expressions. They have to be valid only when the macro is called. | `(defmacro! twicem (fn* (e) (do ~e ~e)))` &rArr; `#<function>` <br /> `(twicem (prn "foo"))` &rArr; `foo foo nil`. <br /> A regular `def!`: `(def! twice (fn* (e) (do ~e ~e)))` &rArr; `#<function>` <br />  `(twice (prn "foo"))` &rArr; `foo (do nil nil)` |
| `nth` | A List or Vector and an index number | The element in the List or Vector at position index | `(nth (list 1 2) 1)` &rArr; `2` |
| `first` | A List or Vector | The first element in the List or Vector. If the List or Vectors are empty, or are Nil, Nil is returned. | `(first (list 7 8 9))` &rArr; `7` <br /> `(first nil)` &rArr; `nil` |
| `rest` | A List or Vector | A new List containing all the elements of the List or Vector, excpet the first. If the List or Vectors are empty, or are Nil, an empty List is returned. | `(rest (list 7 8 9))` &rArr; `(8 9)` <br /> `(rest nil)` &rArr; `()` |
| `cond` | A List containing an even number of elements | The elements are treated in pairs. The first element of a pair is a condition. The second is a value. `cond` returns the first value for which the condition is true. | `(cond false 7 (= 2 2) 8 "else" 9)` &rArr; `8` <br /> `(cond false 7 (= 2 5) 8 "else" 9)` &rArr; `9` |


## Reader macro

| Function | Explanatoin | Example |
|  ---     | ---         | ---     |
| `'` | Equivalnt to `quote` | `'(list 1 2)` &rArr; `(list 1 2)` |
| ``` `` | Equivalnt to `quasiquote` | `(1 2 (3 4))` &rArr; `(1 2 (3 4))` |
| `~` | Equivalnt to `unquote` | `(def! a 8)` &rArr; `8` <br /> `(1 ~a 3)` &rArr; `(1 8 3)` |
| `~@` | Equivalnt to `splice-unquote` | `(def! c (list 2))` &rArr; `(2)` <br /> `(1 ~@c 3)` &rArr; `(1 2 3)` |



