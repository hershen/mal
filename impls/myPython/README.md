# mal - Make a Lisp

This project implements an interpreter for the list-like [mal programming language](https://github.com/kanaka/mal) in Python3.
Everything in this folder is written as part of this project. Other folders in this repository implement the test infrastructure, and were provided by the `mal` project.

##Features

- Tail Call Optimization.
- Comments - anything after a `;` is ignored until the end of the line.


##Types

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

## Processing of `mal` types
When a `list` is processed, the first element is invoked or exeuted on the rest of the elements. For example:

- `(+ 1 2)` -> `3`
- `(+ 2 (* 3 4))` -> `14`

When a `vector` is evaluated, each individual element is evaluated.
When a `hash-map` is evaluated, all the values (odd elements) are evaluated.

| Function | Input | Output | Example |
|  ---     | ---   | ---    | ---     |
|  |  | | |
| `def!` | A new symbol name and an expression | Sets a new symbol name with the value of the evaluated expression | `(def! new (+ 1 2))` -> `3`, `new` -> `3` |
| `let*` | A `list` with key value pairs, and an expression to evaluate | The expression is evaluated with taking into account the key-value pairs defined in the list | `(let* (c 2) c)` -> `2` |
| `cons` | A `mal` type and (a List or Vector). | A new List composed of the `mal` type and the elements of the List or the Vector. | `(cons 1 (list 1 2 3))` -> `(1 1 2 3)` |
| `concat` | 0 or combinations of Lists and Vectors. | A new list containing the elements of the input Lists and Vectors. | `(concat (list 1 2) (list 3 4))` -> `(1 2 3 4)` |
| `quote` | A `mal` type. | The `mal` type. If the `mal` type is not defined, treats it like a Symbol and returns the name of the Symbol. | `(quote abc)` -> `abc` |
| `quasiquote` | A `mal` type. | The same as `quote`, unless `mal` type is a list starting with `unquote` or `splice-unquote`. These are detailed below. | `(quasiquote abc)` -> `abc`  |
| `unquote` | A `mal` type. | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the evaluated form of the argument. | `(def! lst (quote (b c)))` -> `(b c)`, `(quasiquote (a (unquote lst) d))` -> `(a (b c) d)` |
| `splice-unquote` | A List. | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the contents of the List. | `(def! lst (quote (b c)))` -> `(b c)`, `(quasiquote (a (splice-unquote lst) d))` -> `(a b c d)` |
| `vec` | A List or a Vector. | A vector with the same elements as in the input. | `(vec (list 1 2))` -> `[1 2]` |
| `defmacro` | | A macro - a new piece of code. The arguments are evaluated lazily, when they are needed. So this can be never (for example, for the second argument of an `or`. A regular `def!` greedily evaluates all arguments. The arguments of a macro don't have to be valid expressions. They have to be valid only when the macro is called. | `(defmacro! twicem (fn* (e) ` ``(do ~e ~e)))` -> `#<function>`, `(twicem (prn "foo"))` -> `foo foo nil`. A regular `def!`: `(def! twice (fn* (e) ` ``(do ~e ~e)))` -> `#<function>`, `(twice (prn "foo"))` -> `foo (do nil nil)` |
| `nth` | A List or Vector and an index number. | The element in the List or Vector at position index. | `(nth (list 1 2) 1)` -> `2` |
| `first` | A List or Vector. | The first element in the List or Vector. If the List or Vectors are empty, or are Nil, Nil is returned. | `(first (list 7 8 9))` -> `7`, `(first nil)` -> `nil` |
| `rest` | A List or Vector. | A new List containing all the elements of the List or Vector, excpet the first. If the List or Vectors are empty, or are Nil, an empty List is returned. | `(rest (list 7 8 9))` -> `(8 9)`, `(rest nil)` -> `()` |
| `cond` | A List containing an even number of elements. | The elements are treated in pairs. The first element of a pair is a condition. The second is a value. `cond` returns the first value for which the condition is true. | `(cond false 7 (= 2 2) 8 "else" 9)` -> `8`, `(cond false 7 (= 2 5) 8 "else" 9)` -> `9` |


## Reader macro

| Function | Explanatoin | Example |
|  ---     | ---         | ---     |
| `'` | Equivalnt to `quote`. | `'(list 1 2)` -> `(list 1 2)` |
| ``` `` | Equivalnt to `quasiquote`. | ```(1 2 (3 4))`` -> `(1 2 (3 4))` |
| `~` | Equivalnt to `unquote`. | `(def! a 8)` -> `8`, ```(1 ~a 3)`` -> `(1 8 3)` |
| `~@` | Equivalnt to `splice-unquote`. | `(def! c (list 2))` -> `(2)`, ```(1 ~@c 3)`` -> `(1 2 3)` |



