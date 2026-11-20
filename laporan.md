# Laporan Tugas Tree-sitter

## 1. Tugas 1 - Membaca Pohon
Pada tugas ini, saya mempelajari bagaimana sebuah kode Python diterjemahkan menjadi Concrete Syntax Tree (CST). Saya menguji beberapa potongan kode: assignment (`x = 1`), fungsi, `if/else`, dan kelas. 
- Saya dapat membedakan **Named Node** (seperti `identifier`, `function_definition`) yang muncul di output default, dengan **Anonymous Node** (seperti `def`, `:`, `(`, `)`) yang tersembunyi.
- Saya juga menguji kode yang sengaja dirusak (menghapus titik dua `:`). Tree-sitter tetap menghasilkan pohon dan menandai bagian yang rusak dengan node `MISSING ":"` atau `ERROR`. Hal ini membuktikan fitur *error recovery* pada tree-sitter.

## 2. Tugas 2 - Penjelajah Node
Saya membuat file `jelajah.py` yang berfungsi untuk mencetak struktur pohon secara rekursif dengan indentasi yang rapi. Skrip ini mencetak tipe node, posisi `[baris:kolom]`, dan nama `field` (seperti `name:`, `left:`, `right:`).
- **Kendala & Solusi:** Saat pertama kali membuat skrip, semua node tidak menampilkan nama `field`. Setelah saya telusuri, ternyata saya menggunakan indeks dari `named_children`, padahal `field_name_for_child(i)` harus menggunakan indeks dari `node.children` (yang mencakup node anonim). Setelah diperbaiki, output menjadi sempurna.
- Skrip ini saya uji pada file Python buatan saya yang berukuran lebih dari 100 baris dan hasilnya sesuai.

## 3. Tugas 3 - Query Pertama
Saya membuat file `q.py` sebagai runner untuk mengeksekusi file `.scm`. Saya berhasil membuat beberapa query menggunakan S-expression:
- Mencari nama fungsi dan jumlah parameternya menggunakan `QueryCursor(...).matches`.
- Mencari pemanggilan fungsi `print` dengan menyertakan child `argument_list`.
- Mencari statement `import` dan `from ... import`. Saya sempat kesulitan di query import, namun setelah melihat pohon aslinya dengan `jelajah.py`, saya menemukan bahwa node yang tepat adalah `dotted_name`, bukan `identifier`.

## 4. Tugas 4 - Grammar DSL Filter
Saya membangun grammar untuk DSL filter menggunakan `grammar.js`.
- Saya mengikuti langkah 4a hingga 4f secara bertahap.
- Pada langkah 4c (menambahkan `or` dan `and`), saya mengalami `Unresolved conflict` saat menjalankan `tree-sitter generate`. Hal ini terjadi karena parser bingung dengan prioritas. Saya memperbaikinya dengan menambahkan `prec.left(1, ...)` untuk `or` dan `prec.left(2, ...)` untuk `and`.
- Saya juga menambahkan fitur `in` dan `contains` serta menuliskan minimal 5 test case di `test/corpus/dasar.txt`. Semua test lulus (`tree-sitter test`).

## 5. Tugas 5 - Highlight DSL Filter
Saya membuat file `queries/highlights.scm` untuk memberikan warna pada grammar filter yang sudah dibuat.
- Saya memberi capture seperti `@keyword` untuk `and`, `or`, `not`, `in`, `contains`.
- `@operator` untuk tanda `=`, `!=`, `>`, `<`, dll.
- `@string`, `@number`, `@constant.builtin`, dan `@property` untuk field identifier.
- Proses ini berhasil setelah saya memperbaiki file konfigurasi `config.json` agar path direktori parser dikenali oleh CLI.

## 6. Tugas 6 - Mini Proyek `cek.py`
Saya membuat CLI `cek.py` untuk mendeteksi TODO, fungsi panjang (> 30 baris), dan file yang memiliki error sintaks.
- **Fitur 1 (TODO):** Berjalan lancar menggunakan `#match?`.
- **Fitur 2 (Fungsi Panjang):** Saya menghitung selisih `end_point[0]` dan `start_point[0]` dari node `function_definition`.
- **Fitur 3 (Error):** Menggunakan `tree.root_node.has_error` dan mencari node pertama yang `is_error` atau `is_missing`.
- Saya mengujinya pada repository open-source `requests`. Hasil pendeteksian TODO dan fungsi panjang berjalan sesuai dengan pengecekan manual saya pada beberapa file.

## 7. Kendala Utama dan Penyelesaian
Kendala terbesar dalam pengerjaan tugas ini bukanlah pada logika Python atau grammar-nya, melainkan pada **konfigurasi environment di Windows**. 
1. PowerShell memblokir eksekusi `npm.ps1` (diperbaiki dengan mengubah Execution Policy).
2. File `grammar.js` terbaca sebagai ES Module (diperbaiki dengan menghapus `"type": "module"` di `package.json`).
3. Git menolak commit karena folder hasil clone (`tugas6/requests`) memiliki repository Git sendiri (diperbaiki dengan menambahkan file `.gitignore`).