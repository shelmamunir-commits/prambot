from datetime import date
from typing import Optional

from utils.validasi import valid_nama, valid_tanggal

from .katalog_pasaran import KatalogPasaran
from .profil_weton import ProfilWeton


class Pengguna:
    """Pemilik data. ASSOCIATION 1 -> 1..* ke ProfilWeton."""

    def __init__(self, nama: str, tanggal_lahir: date):
        if not valid_nama(nama):
            raise ValueError(f"Nama tidak valid: {nama!r}")
        if not valid_tanggal(tanggal_lahir):
            raise ValueError("Tanggal lahir tidak valid.")
        self._nama = nama.strip()
        self._tanggal_lahir = tanggal_lahir
        self._daftar_profil: list[ProfilWeton] = []

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def tanggal_lahir(self) -> date:
        return self._tanggal_lahir

    @property
    def daftar_profil(self) -> list[ProfilWeton]:
        return list(self._daftar_profil)

    def tambah_profil(self, profil: ProfilWeton) -> None:
        self._daftar_profil.append(profil)

    def buat_profil(self, katalog: Optional[KatalogPasaran] = None) -> ProfilWeton:
        """Buat profil weton dari tanggal lahir dan simpan di pengguna ini."""
        profil = ProfilWeton.dari_tanggal(self._nama, self._tanggal_lahir, katalog)
        self.tambah_profil(profil)
        return profil
