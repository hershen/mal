# mal - Make a Lisp

| Function | Input | Output | Example |
|  ---     | ---   | ---    | ---     |
| `cons` | A mal type and a list. | A new list composed of the mal type and the elements of the list | `(cons 1 (list 1 2 3))` -> `(1 1 2 3)` |
| `concat` | 0 or more lists. | A new list containg the elements of the lists. | `(concat (list 1 2) (list 3 4))` -> `(1 2 3 4)` |
| `quote` | A mal type. | The mal type. If the mal type is not defined, treats it like a Symbol and returns the name of the Symbol. | `(quote abc)` -> `abc` |
| `quasiquote` | A mal type. | The same as `quote`, unless mal type is a list starting with `unquote` or `splice-unquote`. These are detailed below. | `(quasiquote abc)` -> `abc`  |
| `unquote` | A mal type. | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the evaluated form of the argument. | `(def! lst (quote (b c)))` -> `(b c)`, `(quasiquote (a (unquote lst) d))` -> `(a (b c) d)` |
| `splice-unquote` | A List | Meant to be used inside a `quasiquote` evaluation. Replaces the call to itself with the contents of the List. | `(def! lst (quote (b c)))` -> `(b c)`, `(quasiquote (a (splice-unquote lst) d))` -> `(a b c d)` |


