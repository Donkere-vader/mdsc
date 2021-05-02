from .lark_loader import load_lark_tree


class Compiler:
    def __init__(self):
        self.file_name = None

    def compile(self, file_name):
        self.context = []
        self.flags = []
        self.file_name = file_name
        self.tree = load_lark_tree(self.file_name)

        return self.compile_code_block(self.tree)

    def compile_code_block(self, block_tree, context={}):
        print(f"\nCOMPILING BLOCK: {block_tree}")
        if "MACHINE" in self.flags:
            return self.compile_machine_code_block(block_tree)
        self.flags = []

        current_context = context
        self.context.append(current_context)

        for item in block_tree.children:
            if item is None:
                continue

            # print(item)
            # if hasattr(item, "data"):
            #     print(item.data)
            if item.data == "code" or item.data == "code_block":
                self.compile_code_block(item)
            if item.data == "line":
                self.compile_line(item)

        print(self.flags)

        del self.context[-1]

    def compile_line(self, line):
        print("\nLINE:", end=" ")
        for item in line.children:
            if item is None:
                continue
            print(item)

            if item.data == "flag":
                self.flags.append(item.children[0].upper())
            if item.data == "code" or item.data == "code_block":
                self.compile_code_block(item)
            if item.data == "function":
                new_context = {}

                while None in item.children:
                    item.children.remove(None)

                function_name = item.children[0]
                parameter_list = item.children[1]

                for argument in item.children:
                    pass

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
                    code_line.append(context[item.children[0]])

        print("\n".join(code))
