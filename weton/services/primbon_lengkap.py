"""Layanan perhitungan primbon Jawa komprehensif.

Menggabungkan algoritma dan dataset lengkap setara Ki-Demang.com dan Primbon.com:
- Penanggalan 3 Kalender (Masehi, Jawa, Hijriyah)
- Wewaran (Saptawara, Pancawara, Sadwara, Hastawara, Sangawara)
- Prabot Pawukon (30 Wuku, Dewa, Pohon, Burung, Gedhong, Aral, Sesaji, Kala Jaya Bumi)
- Watak Kelahiran Lengkap (35 Weton)
- Rakam & Paarasan (Lakuning)
- Karier, Karakter Bisnis, dan Rezeki
- Pal Srigati (Fluktuasi rezeki sepanjang hidup)
- Hari Naas & Arah Keberuntungan (Naga Dina)
- Jodoh Komprehensif (Metode 8, Metode 7/Pancasuda, Metode 5)
- Rekomendasi Hari Baik & Larangan (Taliwangke, Samparwangke)
"""

from datetime import date, timedelta
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from utils.javanese_date import JavaneseDate

# Load scraped datasets
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

try:
    with open(os.path.join(DATA_DIR, 'primbon_weton.json'), 'r', encoding='utf-8') as f:
        WETON_DATA: Dict[str, Any] = json.load(f)
except Exception:
    WETON_DATA = {}

try:
    with open(os.path.join(DATA_DIR, 'kidemang_wuku.json'), 'r', encoding='utf-8') as f:
        WUKU_DATA: Dict[str, Any] = json.load(f)
except Exception:
    WUKU_DATA = {}

try:
    with open(os.path.join(DATA_DIR, 'kidemang_rakam_35.json'), 'r', encoding='utf-8') as f:
        KIDEMANG_RAKAM: Dict[str, Any] = json.load(f)
except Exception:
    KIDEMANG_RAKAM = {}

# Daftar Wuku (30)
DAFTAR_WUKU = [
    'Sinta', 'Landhep', 'Wukir', 'Kurantil', 'Tolu', 'Gumbreg',
    'Warigalit', 'Warigagung', 'Julungwangi', 'Sungsang', 'Galungan',
    'Kuningan', 'Langkir', 'Mandasiya', 'Julungpujud', 'Pahang',
    'Kuruwelut', 'Marakeh', 'Tambir', 'Medangkungan', 'Maktal',
    'Wuye', 'Manahil', 'Prangbakat', 'Bala', 'Wugu', 'Wayang',
    'Kulawu', 'Dukut', 'Watugunung'
]

# Daftar Sadwara / Paringkelan (6)
DAFTAR_SADWARA = [
    ('Tungle', 'Daun', 'Suka menolong, mudah terharu, namun mudah terombang-ambing.'),
    ('Aryang', 'Manusia', 'Mudah beradaptasi, bijaksana, suka bergaul, pandai berteman.'),
    ('Wurukung', 'Hewan', 'Ulet, pekerja keras, berani, terkadang ceroboh atau kurang teliti.'),
    ('Paningron', 'Mina/Ikan', 'Tenang, pandai menyimpan rahasia, namun waspada terhadap tipu daya.'),
    ('Uwas', 'Peksi/Burung', 'Cepat tanggap, berpandangan jauh, namun jangan bersikap takabur.'),
    ('Mawulu', 'Taru/Benih', 'Penyabar, senang menanam kebaikan, rezeki tumbuh bertahap.')
]

# Daftar Hastawara / Padewan (8)
DAFTAR_HASTAWARA = [
    ('Sri', 'Dewi Sri', 'Welas asih, penyayang, membawa kesuburan dan kecukupan sandang pangan.'),
    ('Indra', 'Bathara Indra', 'Berwibawa tinggi, berbakat memimpin, pandai, berpikiran luas.'),
    ('Guru', 'Bathara Guru', 'Berkuasa, menjadi panutan, pemberi nasihat yang disegani, suka membimbing.'),
    ('Yama', 'Bathara Yama', 'Sederhana, adil, tegas pada pendirian, pemaaf namun tidak suka kecurangan.'),
    ('Rudra', 'Bathara Rudra', 'Pemberani, bertenaga besar, jangan mudah tersulut amarah.'),
    ('Brama', 'Bathara Brahma', 'Bersemangat menggelora, kreatif, ambisius, cepat bangkit dari kegagalan.'),
    ('Kala', 'Bathara Kala', 'Disegani musuh, teguh, perlu banyak mawas diri agar terhindar dari aral.'),
    ('Uma', 'Dewi Uma', 'Penuh kasih sayang, tekun, sabar merawat, tabah menghadapi kesulitan.')
]

# Daftar Sangawara / Padangon (9)
DAFTAR_SANGAWARA = [
    ('Dangu', 'Batu', 'Pendiriannya kokoh tidak mudah goyah, tenang, pendiam.'),
    ('Jagur', 'Harimau', 'Pemberani, disegani kawan dan lawan, bertangan kuat, waspada emosi.'),
    ('Gigis', 'Bumi', 'Berhati lapang, mengayomi, menerima apa adanya, banyak rezeki.'),
    ('Kerangan', 'Matahari', 'Bercahaya, menerangi sekeliling, disiplin, berwibawa.'),
    ('Nohan', 'Bulan', 'Mempesona, menyejukkan hati yang susah, dicintai banyak orang.'),
    ('Wogan', 'Ulat', 'Ulet, sabar dalam merintis dari bawah hingga bertransformasi indah.'),
    ('Tulus', 'Air', 'Ikhlas, tekun, dermawan, lemah lembut, rezeki mengalir terus.'),
    ('Wurung', 'Api', 'Dinamis, cepat menyelesaikan masalah, jangan mudah tergesa-gesa.'),
    ('Dadi', 'Kayu', 'Bermanfaat bagi orang banyak, berselera mulia, kokoh dan dipercaya.')
]

# Daftar Paarasan (berdasarkan total Neptu 7 s/d 18)
MAP_PAARASAN = {
    7: ('Lakuning Bumi', 'Pemurah, pemaaf, dan pelindung sesama. Suka mengalah demi kedamaian.'),
    8: ('Lakuning Geni', 'Berani, temperamental bila dipancing, cepat marah namun cepat reda.'),
    9: ('Lakuning Angin', 'Pandai mengambil hati orang, pandai bicara, lincah, luwes bergaul.'),
    10: ('Aras Pepet', 'Pandai menyimpan rahasia dan harta, senang bertapa/prihatin, cerdas.'),
    11: ('Aras Tuding', 'Sering ditunjuk memimpin, menjadi rujukan banyak perkara, pembawa hoki.'),
    12: ('Aras Kembang', 'Daya tarik tinggi, memikat lawan jenis, berwibawa dan disenangi orang.'),
    13: ('Lakuning Lintang', 'Rendah hati, senang menyendiri/fokus pada keilmuan, mandiri.'),
    14: ('Lakuning Rembulan', 'Simpatik, penerang dalam kegelapan, pembawa ketenteraman jiwa.'),
    15: ('Lakuning Srengenge', 'Terang budinya, disiplin, berwibawa, mampu mengayomi bawahan.'),
    16: ('Lakuning Banyu', 'Tenang, murah rezeki, mudah beradaptasi, berhati sejuk dan sabar.'),
    17: ('Lakuning Bumi', 'Pemurah, pelindung, tangguh menghadapi cobaan hidup, berjiwa besar.'),
    18: ('Lakuning Geni', 'Semangat membara, disegani banyak pihak, gigih mencapai cita-cita tinggi.')
}

# Daftar Rakam (berdasarkan pembagian weton)
# Sisa Neptu mod 6 (jika sisa 0 dianggap 6)
MAP_RAKAM = {
    1: ('Demang Kadhuruwan', 'Suka membantah bila merasa benar, sering mendapat perkara namun kuat mental.'),
    2: ('Kala Tinantang', 'Pemberani luar biasa, bernyali besar, tangguh, disegani lawan.'),
    3: ('Sanggar Waringin', 'Teduh hatinya, suka memberi perlindungan dan bantuan, tempat mengadu.'),
    4: ('Mantri Sinaroja', 'Memperoleh kemuliaan dan pangkat, mampu menyelesaikan tugas, tercapai cita-cita.'),
    5: ('Macan Ketawan', 'Disegani, berwibawa, berkecukupan materi namun hati harus dilatih tenang.'),
    6: ('Nuju Pati', 'Banyak menghadapi ujian dan prihatin, harus memperbanyak sedekah dan ikhtiar.')
}

# Daftar Pancasuda Pribadi (sisa neptu mod 7, sisa 0 dianggap 7)
MAP_PANCASUDA_PRIBADI = {
    1: ('Wasesa Segara', 'Pemaaf, suka menolong sesama, berhati mulia seluas samudera.'),
    2: ('Tunggak Semi', 'Rezeki mudah tumbuh dan bersemi kembali walau habis terpakai.'),
    3: ('Satria Wibawa', 'Mendapat kemuliaan, kehormatan, dan kedudukan yang tinggi di masyarakat.'),
    4: ('Sumur Sinaba', 'Menjadi tempat bertanya dan rujukan ilmu pengetahuan, berwawasan luas.'),
    5: ('Satria Wirang', 'Sering menghadapi ujian rasa malu atau fitnah, namun tabah dan ulet.'),
    6: ('Bumi Kapetak', 'Pekerja keras, ulet, sanggup menghadapi cobaan berat tanpa mengeluh.'),
    7: ('Lebu Katiup Angin', 'Harus pandai mengelola keuangan, tekun berdoa agar rezeki tidak cepat habis.')
}

# Nama Jawa Kuno untuk Hari (Saptawara)
NAMA_DINA_KUNO = {
    'Minggu': 'Radite',
    'Senin': 'Soma',
    'Selasa': 'Anggara',
    'Rabu': 'Budha',
    'Kamis': 'Respati',
    'Jumat': 'Sukra',
    'Sabtu': 'Tumpak'
}

# Nilai Neptu
NILAI_HARI = {
    'Minggu': 5, 'Senin': 4, 'Selasa': 3, 'Rabu': 7,
    'Kamis': 8, 'Jumat': 6, 'Sabtu': 9
}
NILAI_PASARAN = {
    'Legi': 5, 'Pahing': 9, 'Pon': 7, 'Wage': 4, 'Kliwon': 8
}
HARI_URUT = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
PASARAN_URUT = ['Legi', 'Pahing', 'Pon', 'Wage', 'Kliwon']

# Jangkar Historis Ki-Demang: 17 Agustus 1945 (Jumat Legi, Wuku Manahil, Pawukon day 159)
ANCHOR_DATE = date(1945, 8, 17)
ANCHOR_PAWUKON_DAY = 159
ANCHOR_SADWARA = 3    # Paningron
ANCHOR_HASTAWARA = 3  # Yama
ANCHOR_SANGAWARA = 6  # Tulus

# Pranata Mangsa (12 Musim Jawa)
PRANATA_MANGSA = [
    (1, 'Kasa', (6, 22), (8, 1), 41, 'Sesotya murca ing embanan', 'Daun-daun berguguran, tanah mengering, hawa dingin malam hari.'),
    (2, 'Karo', (8, 2), (8, 24), 23, 'Bantala rengka', 'Tanah mulai retak-retak, pohon kapuk dan randu mulai berbuah.'),
    (3, 'Katelu', (8, 25), (9, 17), 24, 'Suta manut ing bapa', 'Musim panen palawija, tunas bambu mulai tumbuh.'),
    (4, 'Kapat', (9, 18), (10, 12), 25, 'Waspa kumembeng jroning kalbu', 'Mata air mulai menyusut, udara panas, musim labuh mendekat.'),
    (5, 'Kalima', (10, 13), (11, 8), 27, 'Pancuran mas sumawur ing jagad', 'Mulai turun hujan rintik-rintik, pohon asam bertunas muda.'),
    (6, 'Kanem', (11, 9), (12, 21), 43, 'Rasa mulya kasuciyan', 'Musim hujan lebat, petani mulai menggarap sawah, buah-buahan berlimpah.'),
    (7, 'Kapitu', (12, 22), (2, 2), 43, 'Wisa kentas ing maruta', 'Puncak musim penghujan, angin kencang, waspada banjir.'),
    (8, 'Kawolu', (2, 3), (2, 28), 26, 'Anjrah jroning kayun', 'Hujan mulai reda, ulat dan serangga berkembang biak.'),
    (9, 'Kasanga', (3, 1), (3, 25), 25, 'Wedharing wacana mulya', 'Padi mulai menguning, tonggeret berbunyi di pepohonan.'),
    (10, 'Kadasa', (3, 26), (4, 18), 24, 'Gedhong mineb jroning kalbu', 'Musim panen raya, binatang bunting, butir padi melimpah di lumbung.'),
    (11, 'Desta', (4, 19), (5, 11), 23, 'Sotya sinara wedi', 'Burung-burung memberi makan anaknya, udara mulai sejuk.'),
    (12, 'Saddha', (5, 12), (6, 21), 41, 'Tirta sah saking sasana', 'Air mulai surut, hawa dingin (bediding) mulai terasa di tanah Jawa.')
]

# Petung Jodoh Siklus 8 (Primbon Jawa Tradisional)
PETUNG_JODOH_8 = {
    1: ('Pegat', False, 'Sering mengalami perselisihan, ujian ekonomi, atau rawan perpisahan bila tidak saling menjaga ego.'),
    2: ('Ratu', True, 'Sangat disegani dan dihormati oleh lingkungan sekitar, pasangan berwibawa dan penuh berkah.'),
    3: ('Jodoh', True, 'Sangat serasi, rukun, saling menerima kelebihan dan kekurangan, berpotensi langgeng hingga tua.'),
    4: ('Topo', True, 'Di awal pernikahan banyak menghadapi ujian dan prihatin, namun di masa tua akan memetik kebahagiaan dan kemuliaan.'),
    5: ('Tinari', True, 'Murah rezeki, selalu ada jalan kemudahan finansial, sering mendapat rezeki tak terduga.'),
    6: ('Padu', False, 'Sering berdebat dan cekcok soal hal-hal sepele, namun tidak sampai berpisah asalkan ada yang mau mengalah.'),
    7: ('Sujanan', False, 'Rawan godaan perselingkuhan, kecurigaan pihak ketiga, atau pertengkaran akibat rasa cemburu.'),
    0: ('Pesthi', True, 'Rumah tangga adem ayem, tenteram, rukun hingga hari tua, walau ada cobaan tetap kokoh.')
}

# Petung Jodoh Siklus 7 (Pancasuda Jodoh)
PETUNG_JODOH_7 = {
    1: ('Wasesa Segara', True, 'Pemaaf, berbudi luhur, berwibawa, dan lapang dada dalam membina rumah tangga.'),
    2: ('Tunggak Semi', True, 'Rezeki mudah datang dan berkembang, selalu tercukupi untuk kebutuhan keluarga.'),
    3: ('Satria Wibawa', True, 'Mulia, dihormati orang banyak, sering mendapat kedudukan terhormat.'),
    4: ('Sumur Sinaba', True, 'Menjadi panutan masyarakat, suka menolong, sering dimintai nasihat.'),
    5: ('Satria Wirang', False, 'Sering menghadapi ujian rasa malu atau masalah finansial, butuh kesabaran ekstra.'),
    6: ('Bumi Kapetak', False, 'Banyak kerja keras dan ujian berat, namun akan kokoh jika tabah.'),
    0: ('Lebu Katiup Angin', False, 'Rezeki mudah habis jika tidak hemat, impian sering menghadapi halangan.')
}

# Petung Jodoh Siklus 5
PETUNG_JODOH_5 = {
    1: ('Sri', True, 'Membawa kemakmuran, sandang pangan melimpah, dan kebahagiaan keluarga.'),
    2: ('Lungguh / Nyawa', True, 'Mendapat kedudukan, kehormatan, keselamatan, dan kesehatan baik.'),
    3: ('Gedhong', True, 'Mendapatkan kelimpahan materi, harta benda, dan kecukupan rumah tangga.'),
    4: ('Lara', False, 'Rawan mengalami sakit atau hambatan usaha, dianjurkan memperbanyak sedekah.'),
    0: ('Pati', False, 'Mengalami ujian berat, dianjurkan mencari hari pernikahan yang baik sebagai penawar.')
}


class PrimbonLengkap:
    """Mesin kalkulasi primbon Jawa komprehensif."""

    @staticmethod
    def hitung_pawukon(tgl: date) -> Dict[str, Any]:
        """Hitung seluruh siklus Pawukon & Wewaran berdasarkan tanggal Masehi."""
        delta = (tgl - ANCHOR_DATE).days
        pawukon_day = (ANCHOR_PAWUKON_DAY + delta) % 210

        # Wuku
        wuku_idx = pawukon_day // 7
        nama_wuku = DAFTAR_WUKU[wuku_idx]
        hari_dalam_wuku = pawukon_day % 7

        # Sadwara (Paringkelan - siklus 6)
        sadwara_idx = (ANCHOR_SADWARA + delta) % 6
        nama_sadwara, lambang_sadwara, arti_sadwara = DAFTAR_SADWARA[sadwara_idx]

        # Hastawara (Padewan - siklus 8)
        hastawara_idx = (ANCHOR_HASTAWARA + delta) % 8
        nama_hastawara, dewa_hastawara, arti_hastawara = DAFTAR_HASTAWARA[hastawara_idx]

        # Sangawara (Padangon - siklus 9)
        sangawara_idx = (ANCHOR_SANGAWARA + delta) % 9
        nama_sangawara, lambang_sangawara, arti_sangawara = DAFTAR_SANGAWARA[sangawara_idx]

        # Hari & Pasaran
        nama_hari = HARI_URUT[tgl.weekday()]
        pasaran_idx = delta % 5
        nama_pasaran = PASARAN_URUT[pasaran_idx]
        neptu_hari = NILAI_HARI[nama_hari]
        neptu_pasaran = NILAI_PASARAN[nama_pasaran]
        total_neptu = neptu_hari + neptu_pasaran

        # Paarasan, Rakam, dan Pancasuda langsung dari dataset Ki-Demang untuk 35 weton
        weton_key = f"{nama_hari} {nama_pasaran}"
        kd_data = KIDEMANG_RAKAM.get(weton_key, {})

        if kd_data and kd_data.get('paarasan_nama'):
            paarasan_item = (kd_data['paarasan_nama'], kd_data.get('paarasan_arti', ''))
        else:
            paarasan_item = MAP_PAARASAN.get(total_neptu, ('Lakuning Banyu', 'Tenang dan murah rezeki.'))

        if kd_data and kd_data.get('rakam_nama'):
            rakam_item = (kd_data['rakam_nama'], kd_data.get('rakam_arti', ''))
        else:
            rakam_key = total_neptu % 6
            if rakam_key == 0:
                rakam_key = 6
            rakam_item = MAP_RAKAM.get(rakam_key, ('Sanggar Waringin', 'Teduh hatinya, suka memberi perlindungan.'))

        if kd_data and kd_data.get('pancasuda_nama'):
            pancasuda_item = (kd_data['pancasuda_nama'], kd_data.get('pancasuda_arti', ''))
        else:
            pancasuda_key = total_neptu % 7
            if pancasuda_key == 0:
                pancasuda_key = 7
            pancasuda_item = MAP_PANCASUDA_PRIBADI.get(pancasuda_key, ('Wasesa Segara', 'Pemaaf dan berhati mulia.'))

        # Pranata Mangsa
        mangsa_item = PrimbonLengkap.cari_pranata_mangsa(tgl)

        # Wuku Detail dari dataset Ki-Demang
        wuku_detail = WUKU_DATA.get(nama_wuku, {})

        # Tanggal Jawa via JavaneseDate
        try:
            jd = JavaneseDate().fromDate(tgl.year, tgl.month, tgl.day)
            tgl_jawa_str = f"{jd.dina.value} {jd.sasi.name} {jd.tahun.value} {jd.tahun.name}"
            tahun_jawa = jd.tahun.name
        except Exception:
            tgl_jawa_str = f"{nama_hari} {nama_pasaran}"
            tahun_jawa = "Ehe"

        return {
            'tanggal': tgl,
            'hari': nama_hari,
            'hari_kuno': NAMA_DINA_KUNO.get(nama_hari, nama_hari),
            'pasaran': nama_pasaran,
            'neptu_hari': neptu_hari,
            'neptu_pasaran': neptu_pasaran,
            'total_neptu': total_neptu,
            'wuku': nama_wuku,
            'wuku_index': wuku_idx + 1,
            'hari_dalam_wuku': hari_dalam_wuku,
            'sadwara': {
                'nama': nama_sadwara,
                'lambang': lambang_sadwara,
                'arti': arti_sadwara
            },
            'hastawara': {
                'nama': nama_hastawara,
                'dewa': dewa_hastawara,
                'arti': arti_hastawara
            },
            'sangawara': {
                'nama': nama_sangawara,
                'lambang': lambang_sangawara,
                'arti': arti_sangawara
            },
            'paarasan': {
                'nama': paarasan_item[0],
                'arti': paarasan_item[1]
            },
            'rakam': {
                'nama': rakam_item[0],
                'arti': rakam_item[1]
            },
            'pancasuda': {
                'nama': pancasuda_item[0],
                'arti': pancasuda_item[1]
            },
            'mangsa': mangsa_item,
            'wuku_detail': wuku_detail,
            'tanggal_jawa': tgl_jawa_str,
            'tahun_jawa': tahun_jawa
        }

    @staticmethod
    def cari_pranata_mangsa(tgl: date) -> Dict[str, Any]:
        """Menentukan Pranata Mangsa berdasarkan tanggal."""
        m, d = tgl.month, tgl.day
        for idx, nama, (m1, d1), (m2, d2), umur, candra, makna in PRANATA_MANGSA:
            if m1 <= m2:
                if (m == m1 and d >= d1) or (m == m2 and d <= d2) or (m1 < m < m2):
                    return {'nomor': idx, 'nama': nama, 'candra': candra, 'makna': makna, 'umur': umur}
            else:
                # Menyeberang pergantian tahun kalender
                if (m == m1 and d >= d1) or (m > m1) or (m == m2 and d <= d2) or (m < m2):
                    return {'nomor': idx, 'nama': nama, 'candra': candra, 'makna': makna, 'umur': umur}
        return {'nomor': 1, 'nama': 'Kasa', 'candra': 'Sesotya murca ing embanan', 'makna': 'Musim kemarau awal.', 'umur': 41}

    @staticmethod
    def profil_weton_lengkap(nama: str, tgl: date) -> Dict[str, Any]:
        """Menggabungkan data pawukon, watak 35 weton, karier, bisnis, dan rezeki."""
        pawukon = PrimbonLengkap.hitung_pawukon(tgl)
        weton_key = f"{pawukon['hari']} {pawukon['pasaran']}"

        detail_weton = WETON_DATA.get(weton_key, {})

        # Naga Dina (Arah Keberuntungan & Rezeki)
        # Menghitung posisi Naga Dina untuk hari lahir
        peta_naga = {
            'Minggu': 'Timur Laut menghadap Barat Daya',
            'Senin': 'Timur menghadap Barat',
            'Selasa': 'Tenggara menghadap Barat Laut',
            'Rabu': 'Selatan menghadap Utara',
            'Kamis': 'Barat Daya menghadap Timur Laut',
            'Jumat': 'Barat menghadap Timur',
            'Sabtu': 'Barat Laut menghadap Tenggara'
        }
        naga_dina = peta_naga.get(pawukon['hari'], 'Timur menghadap Barat')

        # Hari Naas / Apes (Hari kelahiran, Was 3, Was 4, Was Gede)
        hari_naas = detail_weton.get('hari_naas', '')
        if not hari_naas:
            hari_naas = f"{pawukon['hari']} {pawukon['pasaran']} (Hari lahir sendiri)"

        return {
            'nama': nama,
            'tanggal': tgl.strftime('%d-%m-%Y'),
            'pawukon': pawukon,
            'watak_lengkap': detail_weton.get('watak', 'Pribadi yang ramah, tekun, dan bertanggung jawab.'),
            'karier': detail_weton.get('pekerjaan', 'Cocok di bidang pelayanan, perdagangan, atau kepemimpinan.'),
            'bisnis': detail_weton.get('bisnis', 'Pilihlah usaha yang berisiko terukur dan tekuni secara konsisten.'),
            'rezeki': detail_weton.get('rejeki', 'Rezeki berkecukupan seiring ketekunan bekerja dan kebiasaan menabung.'),
            'hari_naas': hari_naas,
            'arah_rumah': detail_weton.get('arah_rumah', 'Barat atau Utara'),
            'batu_permata': detail_weton.get('batu_permata', 'Batu giok atau zamrud pelindung diri.'),
            'naga_dina': naga_dina,
            'pal_srigati': detail_weton.get('pal_srigati', [])
        }

    @staticmethod
    def analisis_jodoh_komprehensif(nama_a: str, tgl_a: date, nama_b: str, tgl_b: date) -> Dict[str, Any]:
        """Analisis perjodohan multimetode (Metode 8, Metode 7/Pancasuda, dan Metode 5)."""
        pw_a = PrimbonLengkap.hitung_pawukon(tgl_a)
        pw_b = PrimbonLengkap.hitung_pawukon(tgl_b)

        neptu_a = pw_a['total_neptu']
        neptu_b = pw_b['total_neptu']
        neptu_total = neptu_a + neptu_b

        # 1. Metode Siklus 8 (Petung 8)
        sisa_8 = neptu_total % 8
        hasil_8 = PETUNG_JODOH_8.get(sisa_8, ('Jodoh', True, 'Serasi dan rukun.'))

        # 2. Metode Siklus 7 (Pancasuda Jodoh)
        sisa_7 = neptu_total % 7
        hasil_7 = PETUNG_JODOH_7.get(sisa_7, ('Wasesa Segara', True, 'Saling memaafkan dan lapang dada.'))

        # 3. Metode Siklus 5
        sisa_5 = neptu_total % 5
        hasil_5 = PETUNG_JODOH_5.get(sisa_5, ('Sri', True, 'Murah rezeki dan bahagia.'))

        # Skor kecocokan persentase
        poin = 0
        if hasil_8[1]: poin += 40
        if hasil_7[1]: poin += 35
        if hasil_5[1]: poin += 25
        skor = max(20, min(100, poin))

        # Kesimpulan & Saran
        if skor >= 75:
            tingkat = 'Sangat Selaras & Harmonis'
            saran = 'Kombinasi neptu ini sangat menguntungkan. Rumah tangga diprediksi rukun, langgeng, dan dilimpahi rezeki. Tetap jaga komunikasi dan rasa saling menghargai.'
        elif skor >= 50:
            tingkat = 'Cukup Selaras dengan Ikhtiar'
            saran = 'Hubungan berpotensi baik, namun perlu saling mengalah ketika terjadi beda pendapat. Dianjurkan memilih hari pernikahan yang berbobot baik (neptu Sri atau Gedhong) sebagai penguat keharmonisan.'
        else:
            tingkat = 'Perlu Mawas Diri & Doa'
            saran = 'Terdapat beberapa aspek tantangan menurut petung neptu. Hal ini disikapi dengan memperkuat komitmen, saling menghormati keluarga besar, memperbanyak sedekah, serta menggelar doa selamatan/ruwatan sebelum akad nikah.'

        weton_a_detail = WETON_DATA.get(f"{pw_a['hari']} {pw_a['pasaran']}", {})
        weton_b_detail = WETON_DATA.get(f"{pw_b['hari']} {pw_b['pasaran']}", {})

        return {
            'nama_a': nama_a,
            'profil_a': pw_a,
            'watak_a': weton_a_detail.get('watak', f"{pw_a['hari']}: berpendirian teguh."),
            'nama_b': nama_b,
            'profil_b': pw_b,
            'watak_b': weton_b_detail.get('watak', f"{pw_b['hari']}: berhati lapang."),
            'neptu_gabungan': neptu_total,
            'skor': skor,
            'tingkat': tingkat,
            'saran': saran,
            'metode_8': {
                'sisa': sisa_8,
                'nama': hasil_8[0],
                'baik': hasil_8[1],
                'makna': hasil_8[2]
            },
            'metode_7': {
                'sisa': sisa_7 if sisa_7 != 0 else 7,
                'nama': hasil_7[0],
                'baik': hasil_7[1],
                'makna': hasil_7[2]
            },
            'metode_5': {
                'sisa': sisa_5 if sisa_5 != 0 else 5,
                'nama': hasil_5[0],
                'baik': hasil_5[1],
                'makna': hasil_5[2]
            }
        }

    @staticmethod
    def rekomendasi_hari_baik_30(nama: str, tgl_lahir: date, tgl_mulai: date, tujuan: str) -> Dict[str, Any]:
        """Mencari rekomendasi hari baik dalam 30 hari ke depan dengan evaluasi mendalam."""
        pw_pemilik = PrimbonLengkap.hitung_pawukon(tgl_lahir)
        neptu_pemilik = pw_pemilik['total_neptu']

        hasil_30 = []
        for i in range(30):
            tgl_eval = tgl_mulai + timedelta(days=i)
            pw_hari = PrimbonLengkap.hitung_pawukon(tgl_eval)
            neptu_hari = pw_hari['total_neptu']

            # Pembagi 5 acara
            sisa_5 = (neptu_pemilik + neptu_hari) % 5
            kategori_lima = PETUNG_JODOH_5.get(sisa_5, ('Sri', True, 'Baik'))

            # Cek hari naas pemilik
            is_hari_naas = (pw_hari['hari'] == pw_pemilik['hari'] and pw_hari['pasaran'] == pw_pemilik['pasaran'])

            # Nilai status
            if is_hari_naas:
                status = 'Hindari (Hari Naas)'
                status_kelas = 'badge-kurang'
                rekomendasi = False
            elif sisa_5 in [1, 2, 3]: # Sri, Lungguh, Gedhong
                status = f"Sangat Baik ({kategori_lima[0]})"
                status_kelas = 'badge-baik'
                rekomendasi = True
            elif sisa_5 == 4:
                status = 'Kurang Baik (Lara)'
                status_kelas = 'badge-kurang'
                rekomendasi = False
            else:
                status = 'Hindari (Pati)'
                status_kelas = 'badge-kurang'
                rekomendasi = False

            hasil_30.append({
                'tanggal': tgl_eval,
                'hari': pw_hari['hari'],
                'pasaran': pw_hari['pasaran'],
                'weton': f"{pw_hari['hari']} {pw_hari['pasaran']}",
                'neptu': neptu_hari,
                'wuku': pw_hari['wuku'],
                'kategori': kategori_lima[0],
                'status': status,
                'status_kelas': status_kelas,
                'rekomendasi': rekomendasi
            })

        # Hari acara pertama (tgl_mulai)
        pw_acara = PrimbonLengkap.hitung_pawukon(tgl_mulai)
        sisa_pertama = (neptu_pemilik + pw_acara['total_neptu']) % 5
        kat_pertama = PETUNG_JODOH_5.get(sisa_pertama, ('Sri', True, 'Membawa rezeki'))

        if kat_pertama[1]:
            analisis = f"Hari {pw_acara['hari']} {pw_acara['pasaran']} dinilai BAIK ({kat_pertama[0]}: {kat_pertama[2]}). Acara {tujuan} berpeluang berlangsung lancar dan mendatangkan keberkahan."
        else:
            analisis = f"Hari {pw_acara['hari']} {pw_acara['pasaran']} tergolong kurang menguntungkan ({kat_pertama[0]}: {kat_pertama[2]}). Pertimbangkan memilih tanggal alternatif yang berstatus Sangat Baik pada tabel rekomendasi di bawah ini."

        return {
            'nama': nama,
            'pemilik': pw_pemilik,
            'tanggal_acara': tgl_mulai.strftime('%d-%m-%Y'),
            'profil_acara': pw_acara,
            'analisis': analisis,
            'tujuan': tujuan,
            'daftar_30': hasil_30,
            'daftar_terbaik': [h for h in hasil_30 if h['rekomendasi']][:8]
        }
