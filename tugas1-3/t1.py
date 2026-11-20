import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"""
class Anjing:
    def bersuara(self):
        return "guk"
"""
tree = parser.parse(kode)
print(tree.root_node)