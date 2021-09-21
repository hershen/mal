# mal - Make a Lisp

- Tail Call Optimization

| Function | Input | Output | Example |
|  ---     | ---   | ---    | ---     |
| `cons` | A mal type and (a List or Vector). | A new List composed of the mal type and the elements of the List or the Vector. | `(cons 1 (list 1 2 3))` -> `(1 1 2 3)` |
| `concat` | 0 or combinations of Lists and Vectors. | A new List containg the elements of the input Lists and Vectors. | `(concat (list 1 2) (list 3 4))` -> `(1 2 3 4)` |
| `quote` | A mal type. | The mal type. If the mal type is not defined, treats it like a Symbol and returns the name of the Symbol. | `(quote abc)` -> `abc` |
| `quasiquote` | A mal type. | The same as `quote`, unless mal type is a list starting with `unquote` or `splice-unquote`. These are detailed below. | `(quasiquote abc)` -> `abc`  |
| `unquote` | A mal type. | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the evaluated form of the argument. | `(def! lst (quote (b c)))` -> `(b c)`, `(quasiquote (a (unquote lst) d))` -> `(a (b c) d)` |
| `splice-unquote` | A List. | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the contents of the List. | `(def! lst (quote (b c)))` -> `(b c)`, `(quasiquote (a (splice-unquote lst) d))` -> `(a b c d)` |
| `vec` | A List or a Vector. | A vector with the same elements as in the input. | `(vec (list 1 2))` -> `[1 2]` |
| `defmacro` | | A macro - a new piece of code. The arguments are evaluated lazily, when they are needed. So this can be never (for example, for the second argument of an `or`. A regular `def!` greedily evaluates all arguments. The arguments of a macro don't have to be valid expressions. They have to be valid only when the macro is called. | `(defmacro! twicem (fn* (e) ` ``(do ~e ~e)))` -> `#<function>`, `(twicem (prn "foo"))` -> `foo foo nil`. A regular `def!`: `(def! twice (fn* (e) ` ``(do ~e ~e)))` -> `#<function>`, `(twice (prn "foo"))` -> `foo (do nil nil)` |
| `nth` | A List or Vector and an index number. | The element in the List or Vector at position index. | `(nth (list 1 2) 1)` -> `2` |
| `first` | A List or Vector. | The first element in the List or Vector. If the List or Vectors are empty, or are Nil, Nil is returned. | `(first (list 7 8 9))` -> `7`, `(first nil)` -> `nil` |
| `rest` | A List or Vector. | A new List containing all the elements of the List or Vector, excpet the first. If the List or Vectors are empty, or are Nil, an empty List is returned. | `(rest (list 7 8 9))` -> `(8 9)`, `(rest nil)` -> `()` |
| `cond` | A List containing an even number of elements. | The elements are treated in pairs. The first element of a pair is a condition. The second is a value. `cond` returns the first value for which the condition is true. | `(cond false 7 (= 2 2) 8 "else" 9)` -> `8`, `(cond false 7 (= 2 5) 8 "else" 9)` -> `9` |


# Reader macro

| Function | Explanatoin | Example |
|  ---     | ---         | ---     |
| `'` | Equivalnt to `quote`. | `'(list 1 2)` -> `(list 1 2)` |
| ``` `` | Equivalnt to `quasiquote`. | ```(1 2 (3 4))`` -> `(1 2 (3 4))` |
| `~` | Equivalnt to `unquote`. | `(def! a 8)` -> `8`, ```(1 ~a 3)`` -> `(1 8 3)` |
| `~@` | Equivalnt to `splice-unquote`. | `(def! c (list 2))` -> `(2)`, ```(1 ~@c 3)`` -> `(1 2 3)` |



