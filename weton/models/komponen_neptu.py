from functools import total_ordering


@total_ordering
class KomponenNeptu:
    """Nilai hari + nilai pasaran. Dimiliki ProfilWeton (composition)."""

    def __init__(self, nilai_hari: int, nilai_pasaran: int):
        for nilai in (nilai_hari, nilai_pasaran):
            if not isinstance(nilai, int) or nilai <= 0:
                raise ValueError("Nilai hari/pasaran harus bilangan bulat positif.")
        self._nilai_hari = nilai_hari
        self._nilai_pasaran = nilai_pasaran

    @property
    def nilai_hari(self) -> int:
        return self._nilai_hari

    @property
    def nilai_pasaran(self) -> int:
        return self._nilai_pasaran

    def total_neptu(self) -> int:
        return self._nilai_hari + self._nilai_pasaran

    # --- operator overloading ---
    def __add__(self, other):
        """neptu(A) + neptu(B) -> int (total gabungan untuk Pancasuda)."""
        if isinstance(other, KomponenNeptu):
            return self.total_neptu() + other.total_neptu()
        if isinstance(other, int):
            return self.total_neptu() + other
        return NotImplemented

    def __radd__(self, other):
        # Agar sum([a, b]) bekerja (sum memulai dari 0)
        if isinstance(other, int):
            return other + self.total_neptu()
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, KomponenNeptu):
            return NotImplemented
        return self.total_neptu() == other.total_neptu()

    def __lt__(self, other):
        if not isinstance(other, KomponenNeptu):
            return NotImplemented
        return self.total_neptu() < other.total_neptu()

    def __hash__(self):
        return hash(self.total_neptu())

    def __str__(self):
        return (f"Neptu {self.total_neptu()} "
                f"(hari {self._nilai_hari} + pasaran {self._nilai_pasaran})")

    def __repr__(self):
        return f"KomponenNeptu({self._nilai_hari}, {self._nilai_pasaran})"
