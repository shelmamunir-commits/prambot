"""Prambot: aplikasi perhitungan weton (CLI).

Jalankan:  python main.py          (menu interaktif)
           python main.py --demo   (demo otomatis tanpa input)
"""
import sys
from datetime import date, timedelta

from models import KatalogPasaran, Pengguna
from services import (CetakLaporanPrimbon, KalkulatorHariBaik, KalkulatorJodoh,
                      PerhitunganWeton)
from utils.validasi import parse_tanggal, valid_nama


def minta(prompt: str, parser):
    """Ulangi input sampai parser tidak melempar ValueError."""
    while True:
        try:
            return parser(input(prompt))
        except ValueError as err:
            print(f"  ! {err}")


def _nama(teks: str) -> str:
    if not valid_nama(teks):
        raise ValueError("Nama hanya huruf/spasi, maksimal 50 karakter.")
    return teks.strip()


def demo_polimorfisme(pengguna: Pengguna, katalog: KatalogPasaran,
                      tgl_pasangan: date, tgl_acara: date) -> None:
    """Satu loop, perilaku berbeda tiap objek (polymorphism)."""
    profil = pengguna.daftar_profil[0]
    kalkulator: list[PerhitunganWeton] = [
        KalkulatorJodoh("KJ-001", pengguna.tanggal_lahir, profil, katalog,
                        tgl_pasangan),
        KalkulatorHariBaik("KH-001", pengguna.tanggal_lahir, profil, katalog,
                           tgl_acara, "pernikahan"),
    ]
    for k in kalkulator:
        print(f"\n{k}")
        print("  hitung_neptu()     :", k.hitung_neptu())
        print("  analisis_karakter():", k.analisis_karakter())
        print("  ringkasan()        :", k.ringkasan()[:90], "...")
    print("\nKhusus subclass:")
    print(" ", kalkulator[0].analisis_keselarasan())
    print(" ", kalkulator[1].analisis_hari_baik())


def menu_buat_profil(state: dict) -> None:
    nama = minta("Nama            : ", _nama)
    tgl = minta("Tanggal lahir   : ", parse_tanggal)
    pengguna = Pengguna(nama, tgl)
    profil = pengguna.buat_profil(state["katalog"])
    state["pengguna"] = pengguna
    print("  ->", profil)


def menu_jodoh(state: dict) -> None:
    pengguna = state["pengguna"]
    nama = minta("Nama pasangan   : ", _nama)
    tgl = minta("Tgl lahir pasangan: ", parse_tanggal)
    k = KalkulatorJodoh("KJ-CLI", pengguna.tanggal_lahir,
                        pengguna.daftar_profil[0], state["katalog"], tgl, nama)
    print("  Pasangan:", k.profil_pasangan)
    print(" ", k.analisis_keselarasan())


def menu_hari_baik(state: dict) -> None:
    pengguna = state["pengguna"]
    tujuan = minta("Tujuan acara    : ", lambda t: t.strip() or (_ for _ in ()).throw(
        ValueError("Tujuan wajib diisi.")))
    tgl = minta("Tanggal acara   : ", parse_tanggal)
    k = KalkulatorHariBaik("KH-CLI", pengguna.tanggal_lahir,
                           pengguna.daftar_profil[0], state["katalog"], tgl, tujuan)
    print(" ", k.analisis_hari_baik())
    print("  Rekomendasi 30 hari dari tanggal tersebut:")
    for t, weton, nama in k.rekomendasi(tgl, 30)[:8]:
        print(f"    {t:%d-%m-%Y}  {weton:<14} {nama}")


def menu_pdf(state: dict) -> None:
    profil = state["pengguna"].daftar_profil[0]
    path = f"laporan_{profil.nama_pengguna.replace(' ', '_')}.pdf"
    CetakLaporanPrimbon().render_pdf(profil, path)
    print(f"  Laporan disimpan: {path}")


def main() -> None:
    katalog = KatalogPasaran()

    if "--demo" in sys.argv:
        pengguna = Pengguna("Rina", date(2003, 5, 17))
        print(pengguna.buat_profil(katalog))
        demo_polimorfisme(pengguna, katalog, date(2002, 11, 3),
                          date.today() + timedelta(days=30))
        return

    state = {"katalog": katalog, "pengguna": None}
    aksi = {"1": menu_buat_profil, "2": None, "3": menu_jodoh,
            "4": menu_hari_baik, "5": menu_pdf}
    while True:
        print("\n=== Prambot ===")
        print("1 Buat profil weton   2 Lihat profil   3 Cek jodoh")
        print("4 Hari baik           5 Cetak PDF      0 Keluar")
        pilih = input("Pilih: ").strip()
        if pilih == "0":
            break
        if pilih not in aksi:
            print("  ! Pilihan tidak dikenal.")
            continue
        if pilih != "1" and state["pengguna"] is None:
            print("  ! Buat profil dulu (menu 1).")
            continue
        if pilih == "2":
            for p in state["pengguna"].daftar_profil:
                print(" ", p, "|", p.neptu)
        else:
            try:
                aksi[pilih](state)
            except (ValueError, RuntimeError) as err:
                print(f"  ! {err}")


if __name__ == "__main__":
    main()
