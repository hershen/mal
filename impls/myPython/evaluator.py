import copy

import core
import env
import mal_types


def is_macro_call(mal_type, environment):
    if isinstance(mal_type, mal_types.List) and isinstance(
        mal_type[0], mal_types.Symbol
    ):
        try:
            function = environment.get(mal_type[0])
        except env.MissingKeyInEnvironment:
            return mal_types.FalseType()

        if isinstance(function, mal_types.FunctionState) and function.is_macro:
            return mal_types.TrueType()

    return mal_types.FalseType()


def eval_ast(mal_type, environment):
    """Evaluate each element of the ast (mal_type), given the environment.
    If it's a List type, evaluate each element of the list.
    """
    if isinstance(mal_type, mal_types.Symbol):
        try:
            return environment.get(mal_type)
        except KeyError:
            raise mal_types.UnrecognizedSymbol(f"Unrecognized symbol {mal_type}")

    elif isinstance(mal_type, mal_types.List):
        return mal_types.List(
            [Evaluator(item, environment).EVAL() for item in mal_type]
        )

    elif isinstance(mal_type, mal_types.Vector):
        return mal_types.Vector(
            [Evaluator(item, environment).EVAL() for item in mal_type]
        )

    elif isinstance(mal_type, mal_types.Hash_map):
        eval_only_values = (
            lambda index, item: item
            if index % 2 == 0
            else Evaluator(item, environment).EVAL()
        )
        return mal_types.Hash_map(
            [eval_only_values(index, item) for index, item in enumerate(mal_type)]
        )

    return mal_type


def expand_macro(mal_type, environment):
    while is_macro_call(mal_type, environment):
        function = environment.get(mal_type[0])
        args = mal_type[1:]
        mal_type = function(*args)

    return mal_type


class Evaluator:
    """Evaluate a mal expression.
    Intended use:
    ```
    Evaluator(mal_type, environment).EVAL()
    ```

    As some programming langauges have a limit on the recurssion depth, Evaluator implements
    Tail Call Optimization (TCO) to reduce the recurssion depth.
    """

    def __init__(self, mal_type, environment):
        self.mal_type = mal_type
        self.environment = environment

    def process_try(self):
        try:
            return Evaluator(self.mal_type[1], self.environment).EVAL()
        except Exception as exception:
            try:
                catch_block = self.mal_type[2]
            except IndexError:
                raise env.MissingKeyInEnvironment(f"{self.mal_type[1]} not found")

            bind = catch_block[1]
            exception_value = (
                exception.value
                if isinstance(exception, mal_types.MalException)
                else mal_types.String(str(exception))
            )
            new_environment = env.Env(
                outer=self.environment, binds=[bind], exprs=[exception_value]
            )

            new_eval = catch_block[2]
            return Evaluator(new_eval, new_environment).EVAL()

    def process_def(self):
        key = self.mal_type[1]
        value = Evaluator(self.mal_type[2], self.environment).EVAL()
        self.environment.set(key, value)
        return value

    def process_defmacro(self):
        key = self.mal_type[1]
        function = Evaluator(self.mal_type[2], self.environment).EVAL()
        function = copy.deepcopy(function)  # do not mutate orignal function
        function.is_macro = mal_types.TrueType()
        self.environment.set(key, function)
        return function

    def process_let(self):
        let_environment = env.Env(outer=self.environment)
        binding_list = self.mal_type[1]

        for key, unevaluated_value in zip(binding_list[::2], binding_list[1::2]):
            let_environment.set(
                key, Evaluator(unevaluated_value, let_environment).EVAL()
            )

        # Tail call optimization - instead of return EVAL(expression, let_environment)
        self.environment = let_environment
        expression = self.mal_type[2]
        self.mal_type = expression

    def process_do(self):
        evaluated_list = eval_ast(self.mal_type[1:-1], self.environment)
        self.mal_type = self.mal_type[-1]

    def process_if(self):
        """Return None in order to continue evaluation in the while loop,
        or something other than None to finilize the evaluation.
        """
        condition = Evaluator(self.mal_type[1], self.environment).EVAL()
        if isinstance(condition, mal_types.Nil) or isinstance(
            condition, mal_types.FalseType
        ):
            try:
                self.mal_type = self.mal_type[3]
            except IndexError:  # No false expression provided
                return mal_types.Nil()
        else:
            self.mal_type = self.mal_type[2]

    def process_fn(self):
        def closure(*args):
            binds = self.mal_type[1]
            exprs = mal_types.List([*args])
            new_environment = env.Env(self.environment, binds, exprs)
            function_body = self.mal_type[2]
            return Evaluator(function_body, new_environment).EVAL()

        params = self.mal_type[1]
        body = self.mal_type[2]
        fn = closure
        return mal_types.FunctionState(body, params, self.environment, fn)

    def process_quasiquote(self):
        quasiquote_returned = core.quasiquote(self.mal_type[1])
        self.mal_type = quasiquote_returned

    def process_regular_list(self):
        """Return None in order to continue evaluation in the while loop,
        or something other than None to finilize the evaluation.
        """
        evaluated_list = eval_ast(self.mal_type, self.environment)
        function = evaluated_list[0]
        operands = evaluated_list[1:]

        if isinstance(function, mal_types.FunctionState):
            self.mal_type = function.mal_type
            self.environment = env.Env(
                outer=function.env, binds=function.params, exprs=operands
            )
        else:
            return function(*operands)

    def EVAL(self):
        while True:
            if not isinstance(self.mal_type, mal_types.List):
                return eval_ast(self.mal_type, self.environment)

            if len(self.mal_type) > 0:
                self.mal_type = expand_macro(self.mal_type, self.environment)

                # Ensure result is still List
                if not isinstance(self.mal_type, mal_types.List):
                    return eval_ast(self.mal_type, self.environment)

                operation_type = self.mal_type[0]

                if operation_type == "try*":
                    return self.process_try()

                if operation_type == "def!":
                    return self.process_def()

                if operation_type == "defmacro!":
                    return self.process_defmacro()

                elif operation_type == "let*":
                    self.process_let()

                elif operation_type == "do":
                    self.process_do()

                elif operation_type == "if":
                    return_value = self.process_if()
                    if return_value is not None:
                        return return_value
                    # otherwise, continue while loop

                elif operation_type == "fn*":
                    return self.process_fn()

                elif operation_type == "quote":
                    return self.mal_type[1]

                # Supposed to be used for debugging - in practice used to pass all tests
                elif operation_type == "quasiquoteexpand":
                    return core.quasiquote(self.mal_type[1])

                elif operation_type == "quasiquote":
                    self.process_quasiquote()

                elif operation_type == "macroexpand":
                    return expand_macro(self.mal_type[1], self.environment)

                else:  # "regular" list
                    return_value = self.process_regular_list()
                    if return_value is not None:
                        return return_value
                    # otherwise, continue while loop

            else:  # mal_type is empty List
                return self.mal_type
