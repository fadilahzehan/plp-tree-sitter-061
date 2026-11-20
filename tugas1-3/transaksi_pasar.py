"""
==========================================================
 PROGRAM SIMULASI TRANSAKSI PASAR
 Fitur  : Manajemen barang, pembeli, transaksi, dan laporan
==========================================================
"""

import os
import datetime

# ------------------- DATA MASTER -------------------
DAFTAR_BARANG = {
    "B001": {"nama": "Beras",        "harga": 12000, "stok": 100},
    "B002": {"nama": "Gula",         "harga": 14000, "stok": 80},
    "B003": {"nama": "Minyak Goreng","harga": 18000, "stok": 60},
    "B004": {"nama": "Telur",        "harga": 2500,  "stok": 200},
    "B005": {"nama": "Tepung",       "harga": 10000, "stok": 70},
    "B006": {"nama": "Garam",        "harga": 5000,  "stok": 90},
    "B007": {"nama": "Kecap",        "harga": 8000,  "stok": 50},
    "B008": {"nama": "Sambal",       "harga": 9000,  "stok": 40},
}

DAFTAR_PEMBELI = ["Andi", "Budi", "Citra", "Dewi", "Eko",
                  "Fajar", "Gita", "Hadi", "Indah", "Joko"]

RIWAYAT_TRANSAKSI = []


# ------------------- FUNGSI BANTU -------------------
def garis(panjang=60, karakter="="):
    """Mencetak garis pemisah."""
    print(karakter * panjang)


def tampilkan_daftar_barang():
    """Menampilkan semua barang yang dijual."""
    garis()
    print("DAFTAR BARANG DI PASAR".center(60))
    garis()
    print(f"{'Kode':<6}{'Nama':<15}{'Harga':>10}{'Stok':>8}")
    garis("-", 60)
    for kode, data in DAFTAR_BARANG.items():
        print(f"{kode:<6}{data['nama']:<15}{data['harga']:>10,}{data['stok']:>8}")
    garis()


def cari_barang(kode):
    """Mencari barang berdasarkan kode."""
    return DAFTAR_BARANG.get(kode)


def hitung_total(keranjang):
    """Menghitung total harga dari keranjang belanja."""
    total = 0
    for item in keranjang:
        total += item["harga"] * item["jumlah"]
    return total


def validasi_stok(kode, jumlah):
    """Memvalidasi stok sebelum transaksi."""
    barang = cari_barang(kode)
    if barang is None:
        return False, "Kode barang tidak ditemukan."
    if jumlah <= 0:
        return False, "Jumlah harus lebih dari 0."
    if barang["stok"] < jumlah:
        return False, f"Stok tidak cukup. Tersedia: {barang['stok']}"
    return True, "OK"


def kurangi_stok(kode, jumlah):
    """Mengurangi stok setelah transaksi berhasil."""
    DAFTAR_BARANG[kode]["stok"] -= jumlah


# ------------------- PROSES TRANSAKSI -------------------
def proses_transaksi(nama_pembeli, keranjang):
    """Memproses transaksi dan menyimpan ke riwayat."""
    total = hitung_total(keranjang)
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaksi = {
        "id": f"TRX{len(RIWAYAT_TRANSAKSI) + 1:04d}",
        "waktu": waktu,
        "pembeli": nama_pembeli,
        "items": keranjang,
        "total": total,
    }
    RIWAYAT_TRANSAKSI.append(transaksi)
    return transaksi


def cetak_struk(transaksi):
    """Mencetak struk transaksi."""
    garis()
    print("STRUK PEMBELIAN".center(60))
    garis()
    print(f"ID Transaksi : {transaksi['id']}")
    print(f"Waktu        : {transaksi['waktu']}")
    print(f"Pembeli      : {transaksi['pembeli']}")
    garis("-", 60)
    print(f"{'Nama':<15}{'Harga':>10}{'Qty':>6}{'Subtotal':>15}")
    garis("-", 60)
    for item in transaksi["items"]:
        subtotal = item["harga"] * item["jumlah"]
        print(f"{item['nama']:<15}{item['harga']:>10,}{item['jumlah']:>6}{subtotal:>15,}")
    garis("-", 60)
    print(f"{'TOTAL':<15}{'':>10}{'':>6}{transaksi['total']:>15,}")
    garis()


# ------------------- SIMULASI PEMBELI -------------------
def simulasi_pembeli(nama, pilihan_belanja):
    """
    Mensimulasikan seorang pembeli berbelanja.
    pilihan_belanja: list tuple (kode_barang, jumlah)
    """
    keranjang = []
    for kode, jumlah in pilihan_belanja:
        valid, pesan = validasi_stok(kode, jumlah)
        if not valid:
            print(f"  [SKIP] {nama} - {kode}: {pesan}")
            continue
        barang = cari_barang(kode)
        keranjang.append({
            "kode": kode,
            "nama": barang["nama"],
            "harga": barang["harga"],
            "jumlah": jumlah,
        })
        kurangi_stok(kode, jumlah)

    if not keranjang:
        print(f"  [X] {nama} tidak jadi membeli apa-apa.")
        return None

    transaksi = proses_transaksi(nama, keranjang)
    cetak_struk(transaksi)
    return transaksi


# ------------------- LAPORAN -------------------
def laporan_pendapatan():
    """Menghitung total pendapatan dari seluruh transaksi."""
    total = sum(t["total"] for t in RIWAYAT_TRANSAKSI)
    garis()
    print("LAPORAN PENDAPATAN PASAR".center(60))
    garis()
    print(f"Jumlah transaksi : {len(RIWAYAT_TRANSAKSI)}")
    print(f"Total pendapatan : Rp {total:,}")
    garis()


def laporan_barang_terjual():
    """Menampilkan barang yang paling banyak terjual."""
    rekap = {}
    for t in RIWAYAT_TRANSAKSI:
        for item in t["items"]:
            rekap[item["nama"]] = rekap.get(item["nama"], 0) + item["jumlah"]

    garis()
    print("REKAP BARANG TERJUAL".center(60))
    garis()
    print(f"{'Nama Barang':<20}{'Jumlah Terjual':>20}")
    garis("-", 60)
    for nama, jumlah in sorted(rekap.items(), key=lambda x: -x[1]):
        print(f"{nama:<20}{jumlah:>20}")
    garis()


def laporan_stok_akhir():
    """Menampilkan sisa stok barang setelah transaksi."""
    garis()
    print("SISA STOK BARANG".center(60))
    garis()
    print(f"{'Kode':<6}{'Nama':<15}{'Stok Akhir':>15}")
    garis("-", 60)
    for kode, data in DAFTAR_BARANG.items():
        print(f"{kode:<6}{data['nama']:<15}{data['stok']:>15}")
    garis()


# ------------------- PROGRAM UTAMA -------------------
def main():
    print()
    garis()
    print("SELAMAT DATANG DI PASAR TRADISIONAL".center(60))
    garis()

    tampilkan_daftar_barang()

    # Simulasi data transaksi
    simulasi = [
        ("Andi",  [("B001", 5), ("B004", 10)]),
        ("Budi",  [("B002", 3), ("B003", 2), ("B007", 1)]),
        ("Citra", [("B005", 4), ("B006", 2)]),
        ("Dewi",  [("B001", 2), ("B002", 1)]),
        ("Eko",   [("B003", 5), ("B008", 3)]),
        ("Fajar", [("B004", 20), ("B005", 2)]),
        ("Gita",  [("B001", 10)]),
        ("Hadi",  [("B002", 5), ("B003", 5), ("B004", 15)]),
        ("Indah", [("B006", 4), ("B007", 2), ("B008", 2)]),
        ("Joko",  [("B001", 3), ("B005", 1)]),
    ]

    print("\n>>> MEMULAI SIMULASI TRANSAKSI PASAR <<<\n")
    for nama, belanja in simulasi:
        print(f"\n--- Pembeli: {nama} ---")
        simulasi_pembeli(nama, belanja)

    # Tampilkan laporan
    print("\n\n>>> LAPORAN AKHIR HARI <<<\n")
    laporan_pendapatan()
    laporan_barang_terjual()
    laporan_stok_akhir()

    print("\nTerima kasih telah berbelanja di pasar kami!\n")


if __name__ == "__main__":
    main()