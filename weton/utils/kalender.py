"""Fungsi kalender kecil: nama hari dari tanggal."""
from datetime import date

from .konstanta import HARI


def nama_hari(tanggal: date) -> str:
    return HARI[tanggal.weekday()]
