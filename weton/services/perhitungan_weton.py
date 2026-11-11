from abc import ABC, abstractmethod
from datetime import date

from models import KatalogPasaran, ProfilWeton
from utils.validasi import valid_tanggal
from utils.javanese_date import JavaneseDate

# Kamus normalisasi nama hari Jawa -> Masehi/Standar
MAP_HARI_JAWA = {
    "Akad": "Minggu",
    "Senen": "Senin",
    "Selasa": "Selasa",
    "Rebo": "Rabu",
    "Kemis": "Kamis",
    "Jemah": "Jumat",
    "Sebtu": "Sabtu"
}


class PerhitunganWeton(ABC):
    """Kelas induk abstrak (realization lewat ABC).

    - profil  : ASSOCIATION (referensi disimpan sebagai atribut)
    - katalog : AGGREGATION (diterima lewat parameter, hidup mandiri)
    - j_date  : COMPOSITION (objek konversi kalender Jawa internal)
    """

    def __init__(self, id_kalkulasi: str, tanggal_lahir: date,
                 profil: ProfilWeton, katalog: KatalogPasaran):
        if not id_kalkulasi:
            raise ValueError("id_kalkulasi wajib diisi.")
        if not valid_tanggal(tanggal_lahir):
            raise ValueError("Tanggal lahir tidak valid.")
        if not isinstance(profil, ProfilWeton):
            raise TypeError("profil harus bertipe ProfilWeton.")
        if not isinstance(katalog, KatalogPasaran):
            raise TypeError("katalog harus bertipe KatalogPasaran.")

        self._id_kalkulasi = id_kalkulasi
        self._tanggal_lahir = tanggal_lahir
        self._profil = profil
        self._katalog = katalog

        # Konversi tanggal lahir masehi ke kalender Jawa secara otomatis
        self._j_date = JavaneseDate().fromDate(
            tanggal_lahir.year,
            tanggal_lahir.month,
            tanggal_lahir.day
        )

        # Sinkronisasi hasil konversi JavaneseDate ke atribut profil weton
        self._singkronkan_profil()

    def _set_attr_profil(self, attr_public: str, attr_private: str, val):
        """Helper aman untuk mengupdate atribut ProfilWeton baik via setter/property murni."""
        try:
            setattr(self._profil, attr_public, val)
        except AttributeError:
            if hasattr(self._profil, attr_private):
                setattr(self._profil, attr_private, val)
            else:
                object.__setattr__(self._profil, attr_public, val)

    def _singkronkan_profil(self):
        """Memperbarui data profil weton berdasarkan hasil konversi JavaneseDate."""
        dina_nama_raw = self._j_date.dina.name
        pasaran_nama = self._j_date.pasaran.name

        # Normalisasi nama hari (misal "Rebo" -> "Rabu", "Jemah" -> "Jumat")
        dina_nama = MAP_HARI_JAWA.get(dina_nama_raw, dina_nama_raw)

        # Mengambil angka neptu dengan fleksibilitas nama method KatalogPasaran
        neptu_dina = self._ambil_neptu(self._katalog, dina_nama, dina_nama_raw, jenis='hari')
        neptu_pasaran = self._ambil_neptu(self._katalog, pasaran_nama, pasaran_nama, jenis='pasaran')

        # Update atribut ProfilWeton secara aman
        self._set_attr_profil('hari', '_hari', dina_nama)
        self._set_attr_profil('pasaran', '_pasaran', pasaran_nama)
        self._set_attr_profil('neptu_hari', '_neptu_hari', neptu_dina)
        self._set_attr_profil('neptu_pasaran', '_neptu_pasaran', neptu_pasaran)

    def _ambil_neptu(self, katalog, nama_std: str, nama_raw: str, jenis: str) -> int:
        """Helper fleksibel untuk mengambil neptu dari KatalogPasaran tanpa pemicu KeyError."""
        nama_method_list = (
            ['cari_neptu_hari', 'neptu_hari', 'get_neptu_hari']
            if jenis == 'hari'
            else ['cari_neptu_pasaran', 'neptu_pasaran', 'get_neptu_pasaran']
        )
        for attr in nama_method_list:
            if hasattr(katalog, attr):
                method = getattr(katalog, attr)
                if callable(method):
                    try:
                        return method(nama_std)
                    except KeyError:
                        try:
                            return method(nama_raw)
                        except KeyError:
                            pass
                elif isinstance(method, dict):
                    return method.get(nama_std, method.get(nama_raw, 0))
        return 0

    @property
    def id_kalkulasi(self) -> str:
        return self._id_kalkulasi

    @property
    def profil(self) -> ProfilWeton:
        return self._profil

    @property
    def j_date(self) -> JavaneseDate:
        """Mengembalikan objek JavaneseDate untuk akses info kalender Jawa lengkap."""
        return self._j_date

    @abstractmethod
    def hitung_neptu(self) -> int:
        """Neptu yang relevan untuk jenis kalkulator ini."""

    @abstractmethod
    def analisis_karakter(self) -> str:
        """Teks analisis karakter sesuai jenis kalkulator."""

    def ringkasan(self) -> str:
        """Memakai method abstrak: hasilnya berbeda tiap subclass."""
        weton_str = self._j_date.format("%D %P, %d %M %Y")
        return (f"[{self._id_kalkulasi}] Weton: {weton_str} | "
                f"neptu={self.hitung_neptu()} | "
                f"{self.analisis_karakter()}")

    def __str__(self):
        return f"{type(self).__name__}({self._id_kalkulasi})"