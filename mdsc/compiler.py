from .lark_loader import load_lark_tree
from .functions import generate_variable_name, get_game_object_class


class Compiler:
    def __init__(self):
        self.file_name = None

    def compile(self, file_name):
        self.context = []
        self.flags = []
        self.file_name = file_name
        self.tree = load_lark_tree(self.file_name)
        self.functions = []

        main_code = self.compile_code_block(self.tree)
        functions_code = self.compile_functions()
        return "\n".join(functions_code + main_code)

    def compile_functions(self):
        precode = []
        code = []

        function_line_idx = len(self.functions) + 1
        for function in self.functions:
            code += function['code'] + ["set @counter counter_return_addr"]
            precode.append(f"set {function['name']} {function_line_idx}")
            function_line_idx += len(function['code']) + 1

        precode.append(f"set @counter {len(precode) + len(code) + 1}")
        return precode + code

    def get_var(self, name):
        """ Get value from current context or global context """
        for idx in [0, -1]:
            if name in self.context[idx]:
                return self.context[idx][name]

    def compile_code_block(self, block_tree, context={}):
        print(f"\nCOMPILING BLOCK: {block_tree}")
        if "MACHINE" in self.flags:
            return self.compile_machine_code_block(block_tree)
        self.flags = []
        code = []

        current_context = context
        self.context.append(current_context)

        for item in block_tree.children:
            if item is None:
                continue

            if item.data == "code" or item.data == "code_block":
                code += self.compile_code_block(item)
            if item.data == "line":
                code += self.compile_line(item)

        del self.context[-1]
        return code

    def compile_line(self, line):
        print("\nLINE:", end=" ")
        precode = []
        code = []
        current_context = self.context[-1]
        for item in line.children:
            if item is None:
                continue
            print(item)

            if hasattr(item, "children"):
                while None in item.children:
                    item.children.remove(None)

            if item.data == "flag":
                self.flags.append(item.children[0].upper())
            if item.data == "code" or item.data == "code_block":
                code += self.compile_code_block(item)
            if item.data == 'define':
                set_tree = item.children[0]
                define_name = set_tree.children[0]
                define_object = set_tree.children[1].children[0].children[0]
                current_context[define_name] = {
                    "name": generate_variable_name(define_name),
                    "type": "class",
                    "class": get_game_object_class(define_object),
                }
                code.append(f"set {current_context[define_name]['name']} {define_object}")
            if item.data == "function":
                new_context = {}
                function_info = {}

                function_name = item.children[0]
                parameter_list = item.children[1]
                code_block = item.children[2]

                function_info['name'] = generate_variable_name(function_name)
                function_info['type'] = 'function'
                function_info['args'] = {}
                function_info['kwargs'] = {}
                for argument in parameter_list.children:
                    if argument.data == 'arg_def':
                        function_info['args'][argument.children[0]] = {"name": generate_variable_name(argument.children[0])}
                    elif argument.data == 'kwarg_def':
                        function_info['kwargs'][argument.children[0]] = {
                            "name": generate_variable_name(argument.children[0]),
                            "value": argument.children[1].children[0],
                        }

                current_context[function_name] = function_info

                for arg in function_info['args']:
                    new_context[arg] = function_info['args'][arg]
                for kwarg in function_info['kwargs']:
                    new_context[kwarg] = function_info['kwargs'][kwarg]
                self.context.append(new_context)
                self.functions.append(function_info)
                function_info['code'] = self.compile_code_block(code_block)
            if item.data == "function_call":
                print(item)

                function_name = item.children[0]
                parameter_list = item.children[1]

                function = self.get_var(function_name)
                print(function)
                arguments = {}
                arg_idx = 0
                kwarg_idx = 0
                for parameter in parameter_list.children:
                    if parameter.data == 'arg':
                        arguments[list(function['args'])[arg_idx]] = parameter.children[0].children[0].children[0]
                        arg_idx += 1
                    if parameter.data == 'kwarg':
                        arguments[list(function['kwargs'])[kwarg_idx]] = parameter.children[1].children[0].children[0]
                        kwarg_idx += 1

                for kwarg in function['kwargs']:
                    if kwarg not in arguments:
                        arguments[kwarg] = function['kwargs'][kwarg]['value']

                for argument in arguments:
                    precode.append(f"set {function['kwargs'][argument]['name']} {arguments[argument]}")

                code += [
                    "op add counter_return_addr @counter 1",
                    f"set @counter {function['name']}"
                ]

        return precode + code

    def compile_machine_code_block(self, block):
        print("\nCOMPILING MACHINE CODE")

        context = self.context[-1]

        code = []

        for line in block.children:
            code_line = []
            for item in line.children:
                if item is None:
                    continue
                if item.data == "value":
                    code_line.append(item.children[0])
                if item.data == "machine_code_get_var":
                    code_line.append(self.get_var(item.children[0])['name'])
            code.append(" ".join(code_line))

        del self.context[-1]
        return code
