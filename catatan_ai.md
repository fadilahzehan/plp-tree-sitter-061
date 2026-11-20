# Catatan Penggunaan AI (AI Coding Agent)

Sesuai dengan aturan tugas, AI (dalam hal ini digunakan melalui asisten *chat* AI) digunakan **hanya sebagai teman *debugging*** ketika saya menemui jalan buntu terkait *environment* di Windows. AI **tidak** digunakan untuk menulis kode inti (`grammar.js`, query `.scm`, `jelajah.py`, atau `cek.py`) maupun untuk membuat tutorial dari nol, karena saya ingin memahami alurnya sendiri.

Berikut adalah catatan kendala yang saya alami dan bagaimana AI membantu, beserta kelemahan/keterbatasan dari saran AI tersebut:

### Kasus 1: Error `npm.ps1 cannot be loaded` (Tugas 4 setup)
- **Masalah:** Saat akan menginstal `tree-sitter-cli`, terminal PowerShell menolak menjalankan perintah `npm` dengan alasan *running scripts is disabled*.
- **Saran AI:** AI menyarankan untuk mengubah *Execution Policy* menggunakan perintah `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.
- **Kesalahan/Keterbatasan AI:** AI awalnya menyarankan untuk menjalankan PowerShell sebagai *Administrator*. Namun, setelah saya coba, perintah tersebut tetap gagal atau malah meminta konfirmasi yang membingungkan. Saya menemukan solusi bahwa menjalankannya di terminal *biasa* (tanpa Administrator) dengan scope `CurrentUser` justru berhasil.
- **Bukti Verifikasi:** Screenshot terminal (terlampir) menunjukkan perintah `node --version` dan `npm --version` berhasil setelah policy diubah.

### Kasus 2: Error `module is not defined in ES module scope` (Tugas 4 setup)
- **Masalah:** Saat menjalankan `tree-sitter generate`, Node.js gagal memproses `grammar.js` karena menganggapnya sebagai ES Module.
- **Saran AI:** AI menyarankan untuk mengubah nama file `grammar.js` menjadi `grammar.cjs`.
- **Kesalahan/Keterbatasan AI:** Mengganti nama file adalah solusi yang merepotkan karena tree-sitter secara bawaan mencari `grammar.js`. Saya memeriksa pesan error lebih teliti dan menemukan bahwa akar masalahnya ada di baris `"type": "module"` di dalam `package.json`. Saya mengabaikan saran rename AI dan langsung menghapus baris tersebut di `package.json`. Generate langsung berhasil.
- **Bukti Verifikasi:** Terminal bersih dari error setelah `package.json` diedit.

### Kasus 3: Error `invalid type: sequence, expected path string` (Tugas 5 setup)
- **Masalah:** Perintah `tree-sitter highlight` gagal karena konfigurasi `parser-directories` di `config.json` tidak valid.
- **Saran AI:** AI menyarankan format JSON dengan *double backslash* (`C:\\Users\\...`).
- **Kesalahan/Keterbatasan AI:** Saat saya menyalin kode dari AI, format JSON-nya menjadi rusak karena ada kurung siku ganda `[[ ... ]]` yang membuat CLI bingung (terbaca sebagai *sequence*). AI gagal memprediksi bahwa saya akan memformat JSON-nya secara berlebihan. Saya harus membetulkan kurung sikunya secara manual menjadi satu array saja.
- **Bukti Verifikasi:** Perintah highlight berhasil mengeluarkan warna setelah struktur JSON diperbaiki.

### Kasus 4: Commit Failed di GitHub Desktop (Tugas 6)
- **Masalah:** Git menolak commit dengan pesan *"nothing added to commit but untracked files present"* karena saya mencoba memasukkan folder `tugas6/requests` (hasil `git clone`).
- **Saran AI:** AI menyarankan untuk membuat file `.gitignore` dan mengabaikan folder tersebut.
- **Kesalahan/Keterbatasan AI:** AI tidak langsung memberi tahu bahwa jika folder tersebut sudah terlanjur masuk ke *staging area*, maka perintah `git rm -r --cached` harus dijalankan. Saya harus mencari tahu sendiri cara mengeluarkan folder tersebut dari antrean commit lewat UI GitHub Desktop agar file `.gitignore` bisa bekerja maksimal.
- **Bukti Verifikasi:** Commit berhasil dan GitHub Desktop menunjukkan hanya file `cek.py` serta `README.md` yang masuk.

**Kesimpulan:**
AI sangat membantu dalam mempercepat identifikasi pesan error terminal, namun saran yang diberikan seringkali bersifat umum dan tidak memperhitungkan konteks UI (seperti GitHub Desktop) atau konfigurasi spesifik OS Windows. Verifikasi manual dan pembacaan pesan error secara teliti tetap menjadi kunci utama.