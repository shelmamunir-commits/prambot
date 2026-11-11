from datetime import date
from functools import singledispatchmethod

from models import KatalogPasaran, ProfilWeton
from utils.konstanta import PANCASUDA, PEMBAGI_JODOH, WATAK_HARI, WATAK_PASARAN

from .perhitungan_weton import PerhitunganWeton


class KalkulatorJodoh(PerhitunganWeton):
    """Neptu(A) + neptu(B) -> Pancasuda."""

    def __init__(self, id_kalkulasi: str, tanggal_lahir: date,
                 profil: ProfilWeton, katalog: KatalogPasaran,
                 tanggal_pasangan: date, nama_pasangan: str = "Pasangan"):
        super().__init__(id_kalkulasi, tanggal_lahir, profil, katalog)
        self._tanggal_pasangan = tanggal_pasangan
        self._profil_pasangan = ProfilWeton.dari_tanggal(
            nama_pasangan, tanggal_pasangan, katalog)

    @property
    def profil_pasangan(self) -> ProfilWeton:
        return self._profil_pasangan

    # --- method overloading (berdasarkan tipe argumen) ---
    @singledispatchmethod
    def hitung_dengan(self, pasangan) -> int:
        raise TypeError(f"Tidak didukung: {type(pasangan).__name__}")

    @hitung_dengan.register
    def _(self, pasangan: ProfilWeton) -> int:
        return self._profil.neptu + pasangan.neptu  # operator overloading

    @hitung_dengan.register
    def _(self, pasangan: date) -> int:
        profil = ProfilWeton.dari_tanggal("Pasangan", pasangan, self._katalog)
        return self.hitung_dengan(profil)

    # --- override method abstrak ---
    def hitung_neptu(self) -> int:
        return self.hitung_dengan(self._profil_pasangan)

    def analisis_karakter(self) -> str:
        bagian = []
        for p in (self._profil, self._profil_pasangan):
            bagian.append(f"{p.nama_pengguna} ({p.hari} {p.pasaran}): "
                          f"{WATAK_HARI[p.hari]}; {WATAK_PASARAN[p.pasaran]}")
        return " || ".join(bagian)

    def sisa_pancasuda(self) -> int:
        return self.hitung_neptu() % PEMBAGI_JODOH or PEMBAGI_JODOH

    def analisis_keselarasan(self) -> str:
        sisa = self.sisa_pancasuda()
        nama, baik, makna = PANCASUDA[sisa]
        penilaian = "cenderung baik" if baik else "perlu kehati-hatian"
        return (f"Neptu gabungan {self.hitung_neptu()} dibagi {PEMBAGI_JODOH} "
                f"sisa {sisa}: {nama} ({penilaian}). {makna}")
