import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for c in node.children:
        hasil = cari_error(c)
        if hasil:
            return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode(errors='replace').strip()}")

    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fn = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        panjang = fn.end_point[0] - fn.start_point[0] + 1
        if panjang > 30:
            print(f"{path}:{fn.start_point[0] + 1}: fungsi '{nama}' panjang {panjang} baris")

    if tree.root_node.has_error:
        node = cari_error(tree.root_node)
        if node:
            print(f"{path}:{node.start_point[0] + 1}: ERROR/MISSING pada tipe '{node.type}'")

def main():
    root = Path(sys.argv[1])
    for path in root.rglob("*.py"):
        if any(p in {"venv", ".git", "node_modules", "__pycache__"} for p in path.parts):
            continue
        cek_file(path)

if __name__ == "__main__":
    main()