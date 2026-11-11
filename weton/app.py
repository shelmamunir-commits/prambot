"""Prambot: aplikasi web perhitungan weton Jawa.

Jalankan:  python app.py          (development server, port 5001)
"""

import os
from datetime import date
from typing import Optional

from flask import (Flask, flash, redirect, render_template, request,
                   send_file, session, url_for)

from models import KatalogPasaran, Pengguna, ProfilWeton
from services import (CetakLaporanPrimbon, KalkulatorHariBaik,
                      KalkulatorJodoh, PrimbonLengkap)
from utils.konstanta import WATAK_HARI, WATAK_PASARAN
from utils.validasi import parse_tanggal, valid_nama

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "prambot-dev-secret")

katalog = KatalogPasaran()


def _profil_dari_form() -> Optional[tuple[str, date, ProfilWeton]]:
    """Ambil & validasi data profil dari form. Kembalikan None jika gagal."""
    nama = request.form.get("nama", "").strip()
    tgl_teks = request.form.get("tanggal_lahir", "").strip()

    if not valid_nama(nama):
        flash("Nama hanya huruf/spasi, maksimal 50 karakter.", "error")
        return None
    try:
        tgl = parse_tanggal(tgl_teks)
    except ValueError as err:
        flash(str(err), "error")
        return None

    pengguna = Pengguna(nama, tgl)
    profil = pengguna.buat_profil(katalog)
    # Simpan ke session untuk laporan PDF
    session["last_profil"] = {
        "nama": profil.nama_pengguna,
        "hari": profil.hari,
        "pasaran": profil.pasaran,
        "tanggal": tgl.strftime("%Y-%m-%d"),
    }
    return nama, tgl, profil

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/dashboard")
def index():
    return render_template("index.html")


@app.route("/hitung", methods=["GET", "POST"])
def hitung():
    if request.method == "POST":
        result = _profil_dari_form()
        if result is None:
            return redirect(url_for("hitung"))
        nama, tgl, profil = result
        
        # Data primbon komprehensif setara Ki-Demang & Primbon.com
        data_lengkap = PrimbonLengkap.profil_weton_lengkap(nama, tgl)

        return render_template(
            "hasil_weton.html",
            nama=nama,
            tanggal=tgl.strftime("%d-%m-%Y"),
            profil=profil,
            neptu=profil.neptu.total_neptu(),
            watak_hari=WATAK_HARI.get(profil.hari, ""),
            watak_pasaran=WATAK_PASARAN.get(profil.pasaran, ""),
            primbon=data_lengkap,
        )
    return render_template("hitung.html")


@app.route("/jodoh", methods=["GET", "POST"])
def jodoh():
    if request.method == "POST":
        nama_a = request.form.get("nama_a", "").strip()
        tgl_a = request.form.get("tanggal_a", "").strip()
        nama_b = request.form.get("nama_b", "").strip()
        tgl_b = request.form.get("tanggal_b", "").strip()

        if not valid_nama(nama_a) or not valid_nama(nama_b):
            flash("Nama kedua belah pihak hanya huruf/spasi, maksimal 50 karakter.", "error")
            return redirect(url_for("jodoh"))
        try:
            tgl_a_parsed = parse_tanggal(tgl_a)
            tgl_b_parsed = parse_tanggal(tgl_b)
        except ValueError as err:
            flash(str(err), "error")
            return redirect(url_for("jodoh"))

        pengguna_a = Pengguna(nama_a, tgl_a_parsed)
        profil_a = pengguna_a.buat_profil(katalog)

        k = KalkulatorJodoh("KJ-WEB", tgl_a_parsed, profil_a, katalog,
                            tgl_b_parsed, nama_b)

        # Analisis multimetode komprehensif
        analisis_lengkap = PrimbonLengkap.analisis_jodoh_komprehensif(
            nama_a, tgl_a_parsed, nama_b, tgl_b_parsed
        )

        return render_template(
            "jodoh.html",
            nama_a=nama_a,
            nama_b=nama_b,
            tanggal_a=tgl_a_parsed.strftime("%d-%m-%Y"),
            tanggal_b=tgl_b_parsed.strftime("%d-%m-%Y"),
            profil_a=profil_a,
            profil_b=k.profil_pasangan,
            neptu_gabungan=k.hitung_neptu(),
            sisa=k.sisa_pancasuda(),
            keselarasan=k.analisis_keselarasan(),
            watak_a=analisis_lengkap['watak_a'],
            watak_b=analisis_lengkap['watak_b'],
            jodoh_lengkap=analisis_lengkap,
        )
    return render_template("jodoh.html")


@app.route("/hari-baik", methods=["GET", "POST"])
def hari_baik():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        tgl_lahir = request.form.get("tanggal_lahir", "").strip()
        tujuan = request.form.get("tujuan_acara", "").strip()
        tgl_acara = request.form.get("tanggal_acara", "").strip()

        if not valid_nama(nama):
            flash("Nama hanya huruf/spasi, maksimal 50 karakter.", "error")
            return redirect(url_for("hari_baik"))
        if not tujuan:
            flash("Tujuan acara wajib diisi.", "error")
            return redirect(url_for("hari_baik"))
        try:
            tgl_lahir_parsed = parse_tanggal(tgl_lahir)
            tgl_acara_parsed = parse_tanggal(tgl_acara) if tgl_acara else date.today()
        except ValueError as err:
            flash(str(err), "error")
            return redirect(url_for("hari_baik"))

        pengguna = Pengguna(nama, tgl_lahir_parsed)
        profil = pengguna.buat_profil(katalog)

        # Analisis hari baik 30 hari komprehensif
        evaluasi_lengkap = PrimbonLengkap.rekomendasi_hari_baik_30(
            nama, tgl_lahir_parsed, tgl_acara_parsed, tujuan
        )

        return render_template(
            "hari_baik.html",
            nama=nama,
            tanggal_lahir=tgl_lahir_parsed.strftime("%d-%m-%Y"),
            tujuan=tujuan,
            tanggal_acara=tgl_acara_parsed.strftime("%d-%m-%Y"),
            profil=profil,
            profil_acara=evaluasi_lengkap['profil_acara'],
            analisis=evaluasi_lengkap['analisis'],
            rekomendasi=[(h['tanggal'], h['weton'], h['kategori']) for h in evaluasi_lengkap['daftar_terbaik']],
            evaluasi_lengkap=evaluasi_lengkap,
        )
    return render_template("hari_baik.html")


@app.route("/laporan")
def laporan():
    """Generate PDF laporan primbon dari profil terakhir yang disimpan session."""
    data = session.get("last_profil")
    if not data:
        flash("Belum ada profil yang dihitung. Silakan hitung weton terlebih dahulu.", "error")
        return redirect(url_for("hitung"))

    profil = ProfilWeton(data["nama"], data["hari"], data["pasaran"])
    tgl_str = data.get("tanggal")
    data_lengkap = None
    if tgl_str:
        try:
            tgl = date.fromisoformat(tgl_str)
            data_lengkap = PrimbonLengkap.profil_weton_lengkap(data["nama"], tgl)
        except Exception:
            data_lengkap = None

    path = f"/tmp/laporan_{profil.nama_pengguna.replace(' ', '_')}.pdf"
    CetakLaporanPrimbon().render_pdf(profil, path, data_lengkap=data_lengkap)
    return send_file(path, as_attachment=True,
                     download_name=f"laporan_primbon_{profil.nama_pengguna.replace(' ', '_')}.pdf")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
