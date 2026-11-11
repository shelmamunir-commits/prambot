import os
from typing import Optional
from models import ProfilWeton
from utils.konstanta import WATAK_HARI, WATAK_PASARAN

try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ImportError as err:
    raise RuntimeError(
        "Paket fpdf2 belum terpasang. Jalankan: pip install -r requirements.txt"
    ) from err


def _latin1(teks: str) -> str:
    """Font bawaan PDF (Helvetica) hanya mendukung Latin-1. Bersihkan karakter tak didukung."""
    if not teks:
        return ""
    replacements = {
        "–": "-", "—": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "•": "*", "…": "...", "é": "e", "è": "e", "ê": "e", "ë": "e",
        "<": "<", ">": ">", "&amp;": "&"
    }
    for k, v in replacements.items():
        teks = teks.replace(k, v)
    return teks.encode("latin-1", "replace").decode("latin-1")


class CetakLaporanPrimbon:
    """DEPENDENCY («use»): profil dan data primbon lengkap dirender ke dokumen PDF."""

    def render_pdf(self, profil: ProfilWeton, path: str, data_lengkap: Optional[dict] = None) -> None:
        # Pastikan direktori tujuan sudah ada sebelum menulis file
        output_dir = os.path.dirname(path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(15, 15, 15)
        pdf.add_page()

        # Header Banner
        pdf.set_fill_color(61, 35, 20)
        pdf.rect(15, 15, 180, 24, "F")

        pdf.set_text_color(201, 162, 39)
        pdf.set_font("Helvetica", "B", 15)
        pdf.set_xy(15, 18)
        pdf.cell(180, 8, _latin1("KITAB PRIMBON JAWA LENGKAP"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_text_color(245, 235, 220)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_xy(15, 27)
        pdf.cell(180, 6, _latin1("Prambot Digital - Kompilasi Rujukan Ki-Demang & Primbon.com"), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_xy(15, 43)

        # 1. Identitas Weton & Neptu
        self._section_title(pdf, "1. IDENTITAS KELAHIRAN & NEPTU")
        n = profil.neptu
        
        pdf.set_fill_color(250, 246, 240)
        pdf.rect(15, pdf.get_y(), 180, 22, "F")
        pdf.set_draw_color(196, 138, 78)
        pdf.rect(15, pdf.get_y(), 180, 22, "D")

        curr_y = pdf.get_y() + 2
        pdf.set_xy(18, curr_y)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(61, 35, 20)
        pdf.cell(35, 6, _latin1("Nama Lengkap:"))
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(55, 6, _latin1(profil.nama_pengguna))

        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(35, 6, _latin1("Weton Kelahiran:"))
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(142, 90, 46)
        pdf.cell(55, 6, _latin1(f"{profil.hari} {profil.pasaran}"))

        curr_y += 7
        pdf.set_xy(18, curr_y)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(61, 35, 20)
        pdf.cell(35, 6, _latin1("Neptu Hari:"))
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(55, 6, _latin1(f"{profil.hari} = {n.nilai_hari}"))

        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(35, 6, _latin1("Neptu Pasaran:"))
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(55, 6, _latin1(f"{profil.pasaran} = {n.nilai_pasaran}"))

        curr_y += 7
        pdf.set_xy(18, curr_y)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(35, 6, _latin1("Total Neptu:"))
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(142, 90, 46)
        pdf.cell(55, 6, _latin1(f"{n.total_neptu()} (Kategori Petung Tradisional)"))

        pdf.set_xy(15, curr_y + 11)

        # Jika ada data lengkap dari PrimbonLengkap
        if data_lengkap and "pawukon" in data_lengkap:
            pw = data_lengkap["pawukon"]
            wuku_info = pw.get("wuku_detail", {})
            pal_srigati = data_lengkap.get("pal_srigati", [])

            # 2. Wewaran Ki-Demang
            self._section_title(pdf, "2. SIKLUS WEWARAN LENGKAP (Rujukan Ki-Demang)")
            
            wewaran_items = [
                ("Sadwara (Paringkelan)", f"{pw['sadwara']['nama']} - {pw['sadwara']['arti']}"),
                ("Hastawara (Padewan)", f"{pw['hastawara']['nama']} - {pw['hastawara']['arti']}"),
                ("Sangawara (Padangon)", f"{pw['sangawara']['nama']} - {pw['sangawara']['arti']}"),
                ("Paarasan (Karakter Jiwa)", f"{pw['paarasan']['nama']} - {pw['paarasan']['arti']}"),
                ("Rakam (Karakter Perilaku)", f"{pw['rakam']['nama']} - {pw['rakam']['arti']}"),
                ("Pancasuda (Kiprah Hidup)", f"{pw['pancasuda']['nama']} - {pw['pancasuda']['arti']}"),
            ]
            for label, val in wewaran_items:
                self._print_row(pdf, label, val, label_w=48)

            pdf.ln(2)

            # 3. Wuku Pawukon
            self._section_title(pdf, f"3. BUTIR PAWUKON: WUKU {pw['wuku'].upper()}")
            
            if wuku_info:
                if wuku_info.get("dewa"):
                    self._print_row(pdf, "Dewa Pelindung", wuku_info.get("dewa"))
                if wuku_info.get("pohon"):
                    self._print_row(pdf, "Pohon", wuku_info.get("pohon"))
                if wuku_info.get("burung"):
                    self._print_row(pdf, "Burung", wuku_info.get("burung"))
                if wuku_info.get("gedhong"):
                    self._print_row(pdf, "Gedhong", wuku_info.get("gedhong"))
                if wuku_info.get("ciri_khas"):
                    self._print_row(pdf, "Ciri Khas", wuku_info.get("ciri_khas"))
                if wuku_info.get("aral"):
                    self._print_row(pdf, "Aral / Bahaya", wuku_info.get("aral"))
                if wuku_info.get("sesaji"):
                    self._print_row(pdf, "Sesaji Tolak Bala", wuku_info.get("sesaji"))
                if wuku_info.get("kala_jaya_bumi"):
                    self._print_row(pdf, "Kala Jaya Bumi", wuku_info.get("kala_jaya_bumi"))

            pdf.ln(2)

            # 4. Watak & Karakteristik (Primbon.com)
            self._section_title(pdf, "4. WATAK DAN KARAKTER KELAHIRAN (Rujukan Primbon.com)")
            
            watak_teks = data_lengkap.get("watak_lengkap", "")
            if watak_teks:
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(40, 40, 40)
                pdf.multi_cell(180, 5, _latin1(watak_teks), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(2)

            # 5. Panduan Karier, Rezeki & Hari Naas
            self._section_title(pdf, "5. PANDUAN HIDUP, KARIER, BISNIS & REZEKI")
            
            panduan_items = [
                ("Karier / Pekerjaan", data_lengkap.get("karier", "-")),
                ("Hubungan Bisnis", data_lengkap.get("bisnis", "-")),
                ("Gambaran Rezeki", data_lengkap.get("rezeki", "-")),
                ("Hari Naas / Pantangan", data_lengkap.get("hari_naas", "-")),
                ("Arah Hadap Rumah", data_lengkap.get("arah_rumah", "-")),
                ("Batu Permata Cocok", data_lengkap.get("batu_permata", "-")),
                ("Naga Dina (Arah Hari)", data_lengkap.get("naga_dina", "-")),
            ]
            for label, isi in panduan_items:
                self._print_row(pdf, label, isi, label_w=45)

            pdf.ln(2)

            # 6. Pal Srigati (Pasang Surut Rejeki)
            if pal_srigati:
                self._section_title(pdf, "6. PAL SRIGATI - PERJALANAN PASANG SURUT REZEKI (1 - 96 TAHUN)")
                pdf.set_font("Helvetica", "I", 8.5)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(180, 4.5, _latin1("Siklus 6 tahunan pasang surut nasib dan rejeki menurut Kitab Primbon Jawa:"),
                               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(1)

                for item in pal_srigati:
                    item_str = str(item)
                    if ":" in item_str:
                        usia_lbl, makna_txt = item_str.split(":", 1)
                    else:
                        usia_lbl, makna_txt = "Fase Usia", item_str

                    pdf.set_font("Helvetica", "B", 8.5)
                    pdf.set_text_color(142, 90, 46)
                    pdf.cell(35, 4.5, _latin1(usia_lbl.strip() + ":"))
                    pdf.set_font("Helvetica", "", 8.5)
                    pdf.set_text_color(50, 50, 50)
                    pdf.multi_cell(145, 4.5, _latin1(makna_txt.strip()), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.ln(0.8)

        else:
            # Fallback ringkas bila hanya ada profil standar
            self._section_title(pdf, "2. GAMBARAN WATAK DASAR")
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(180, 5.5, _latin1(
                f"Hari Kelahiran {profil.hari}: {WATAK_HARI.get(profil.hari, '')}.\n"
                f"Pasaran Kelahiran {profil.pasaran}: {WATAK_PASARAN.get(profil.pasaran, '')}."
            ), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Footer Catatan Budaya
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.multi_cell(180, 4, _latin1(
            "Catatan: Laporan primbon ini disusun berdasarkan rujukan pustaka Ki-Demang Sokowaten "
            "dan Primbon Jawa tradisional. Nilai ramalan bersifat kearifan budaya dan wawasan refleksi diri, "
            "segala takdir dan rezeki sepenuhnya berserah kepada Tuhan Yang Maha Esa."
        ), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output(path)

    def _print_row(self, pdf, label: str, val: str, label_w: float = 40.0) -> None:
        """Cetak satu baris pasangan label dan nilai multiline yang rapi."""
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(61, 35, 20)
        pdf.cell(label_w, 5, _latin1(label + ":"))
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(180 - label_w, 5, _latin1(val or "-"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.5)

    def _section_title(self, pdf, title: str) -> None:
        """Render judul section dengan garis bawah khas."""
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.set_text_color(142, 90, 46)
        pdf.cell(180, 6.5, _latin1(title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_draw_color(196, 138, 78)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 180, pdf.get_y())
        pdf.ln(2)