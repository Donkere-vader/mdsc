from lark import Lark, Tree
from lark import Transformer
import pathlib


class MyTransformer(Transformer):
    def LETTER(self, items):
        return str(items[0])

    def char(self, items):
        return str(items[0])

    def DIGIT(self, items):
        return int(items[0])

    def int(self, items):
        return int("".join([str(i) for i in items]))

    def float(self, items):
        value = items[0] if type(items[0]) == int else 0
        decimals = items[-1] if type(items[-1]) == int else 0
        return float(str(value) + "." + str(decimals))

    def UNDERSCORE(self, items):
        return "_"

    def variable(self, items):
        return "".join([str(i) for i in items])

    def code_block(self, items):
        return Tree('code_block', items[0].children)

    # def STRING(self, items):
    #     return str(items)

    def WS(self, items):
        return None

    def LINE_SEPERATOR(self, token):
        return None


def load_lark_tree(file):
    path_to_this_file = pathlib.Path(__file__).parent.absolute()

    gramar = open(f'{path_to_this_file}/grammar.lark').read()
    code = open(file).read()
    lark = Lark(gramar)

    tree = lark.parse(code)
    return MyTransformer().transform(tree)


if __name__ == "__main__":
    print(load_lark_tree().pretty())
