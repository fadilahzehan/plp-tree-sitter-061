import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"def sapa(nama)\n    return nama\n"  # titik dua dihapus
tree = parser.parse(kode)
print(tree.root_node)

fn = tree.root_node.children[0]
for i, c in enumerate(fn.children):
    print(i, repr(c.type), "named" if c.is_named else "anonim")