"""Data tetap primbon yang dipakai bersama oleh models dan services.

Semua tabel ada di satu tempat supaya mudah dicocokkan dengan sumber primbon
yang dipakai dosen/penulis dan mudah diganti tanpa menyentuh logika kelas.
"""
from datetime import date

# Urutan sesuai date.weekday(): 0 = Senin ... 6 = Minggu
HARI = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")
NILAI_HARI = {
    "Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7,
    "Kamis": 8, "Jumat": 6, "Sabtu": 9,
}

# Urutan siklus pasaran (5 hari)
PASARAN = ("Legi", "Pahing", "Pon", "Wage", "Kliwon")
NILAI_PASARAN = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}

# Jangkar siklus pasaran: 17 Agustus 1945 = Jumat Legi
JANGKAR_TANGGAL = date(1945, 8, 17)
JANGKAR_INDEKS = 0  # indeks "Legi" pada PASARAN

# Pancasuda jodoh: (neptu A + neptu B) dibagi 7, sisa 0 dihitung 7.
# Format: sisa -> (nama, baik?, makna)
PANCASUDA = {
    1: ("Wasesa Segara", True,
        "Pemaaf, berbudi luhur, berwibawa, dan lapang dada."),
    2: ("Tunggak Semi", True,
        "Rezeki mudah datang dan terus berkembang; jaga kesehatan."),
    3: ("Satria Wibawa", True,
        "Mulia dan dihormati lingkungan."),
    4: ("Sumur Sinaba", True,
        "Disegani, menjadi panutan, dan suka menolong sesama."),
    5: ("Satria Wirang", False,
        "Banyak ujian dan rasa malu, terutama soal finansial."),
    6: ("Bumi Kapetak", False,
        "Sering menghadapi cobaan dan rintangan."),
    7: ("Lebu Katiup Angin", False,
        "Banyak halangan, cita-cita sulit terwujud, hidup kurang pasti."),
}
PEMBAGI_JODOH = 7

# Pembagian lima untuk menilai hari acara:
# (neptu profil + neptu hari acara) dibagi 5.
# Model ini disederhanakan untuk keperluan tugas; sesuaikan dengan sumber Anda.
HARI_BAIK_LIMA = {
    1: ("Sri", True, "Membawa rezeki dan kelancaran."),
    2: ("Lungguh", True, "Membawa kedudukan dan kehormatan."),
    3: ("Gedhong", True, "Membawa kemakmuran dan kecukupan."),
    4: ("Lara", False, "Rawan hambatan atau sakit; sebaiknya dihindari."),
    0: ("Pati", False, "Rawan kegagalan; sebaiknya dihindari."),
}
PEMBAGI_HARI_BAIK = 5

# Gambaran watak umum (ringkasan populer, bukan kajian ilmiah)
WATAK_HARI = {
    "Senin": "tenang, perasa, dan setia",
    "Selasa": "tegas, berani, dan bersemangat",
    "Rabu": "bijak, tertutup, dan penuh perhitungan",
    "Kamis": "ramah, berwibawa, dan murah hati",
    "Jumat": "luwes, penyayang, dan mudah bergaul",
    "Sabtu": "ulet, kuat pendirian, dan pekerja keras",
    "Minggu": "berjiwa pemimpin, ceria, dan penuh percaya diri",
}
WATAK_PASARAN = {
    "Legi": "berhati bersih, dermawan, dan mudah memaafkan",
    "Pahing": "ambisius, mandiri, dan gigih",
    "Pon": "tekun, pandai menyimpan perasaan, dan berhati-hati",
    "Wage": "pendiam, teguh, dan setia pada prinsip",
    "Kliwon": "peka, intuitif, dan punya sisi spiritual kuat",
}
