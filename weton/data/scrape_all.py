import urllib.request
import urllib.parse
import re
import json
import time
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor

PASARAN = ['Legi', 'Pahing', 'Pon', 'Wage', 'Kliwon']
HARI = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
DAFTAR_WUKU = [
    'Sinta', 'Landhep', 'Wukir', 'Kurantil', 'Tolu', 'Gumbreg', 
    'Warigalit', 'Warigagung', 'Julungwangi', 'Sungsang', 'Galungan', 
    'Kuningan', 'Langkir', 'Mandasiya', 'Julungpujud', 'Pahang', 
    'Kuruwelut', 'Marakeh', 'Tambir', 'Medangkungan', 'Maktal', 
    'Wuye', 'Manahil', 'Prangbakat', 'Bala', 'Wugu', 'Wayang', 
    'Kulawu', 'Dukut', 'Watugunung'
]

# 1. Scrape 35 Wetons from primbon.com
def get_weton_dates():
    anchor = date(1945, 8, 17) # Jumat Legi
    weton_dates = {}
    d = date(2024, 1, 1)
    while len(weton_dates) < 35:
        delta = (d - anchor).days
        h = HARI[d.weekday()]
        p = PASARAN[delta % 5]
        name = f"{h} {p}"
        if name not in weton_dates:
            weton_dates[name] = d
        d += timedelta(days=1)
    return weton_dates

def scrape_one_weton(item):
    name, dt = item
    url = 'https://www.primbon.com/weton_jawa.php'
    data = urllib.parse.urlencode({'tgl': str(dt.day), 'bln': str(dt.month), 'thn': str(dt.year), 'submit': ' Submit! '}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            clean = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
            clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL)
            clean = re.sub(r'<[^>]+>', '\n', clean)
            text = '\n'.join([l.strip() for l in clean.split('\n') if l.strip()])
            
            res = {'weton': name, 'tanggal_sampel': dt.strftime('%Y-%m-%d')}
            
            m = re.search(r'Watak Kelahiran\s*\n(.*?)(?=\nHari Naas|\nJodoh|\nPekerjaan|\nGambaran Rejeki)', text, re.DOTALL)
            if m: res['watak'] = m.group(1).strip()
            
            m = re.search(r'Hari Naas\s*\n(.*?)(?=\nJodoh|\nPekerjaan|\nArah Hadap)', text, re.DOTALL)
            if m: res['hari_naas'] = m.group(1).strip()
            
            m = re.search(r'Arah Hadap Rumah Yang Cocok\s*\n(.*?)(?=\nBatu|\nPekerjaan)', text, re.DOTALL)
            if m: res['arah_rumah'] = m.group(1).strip()
            
            m = re.search(r'Batu/Permata Yang Cocok\s*\n(.*?)(?=\nPekerjaan|\nSifat)', text, re.DOTALL)
            if m: res['batu_permata'] = m.group(1).strip()
            
            m = re.search(r'Pekerjaan Yang Cocok\s*\n(.*?)(?=\nSifat Berkaitan|\nGambaran Rejeki)', text, re.DOTALL)
            if m: res['pekerjaan'] = m.group(1).strip()
            
            m = re.search(r'Sifat Berkaitan Hubungan Bisnis\s*\n(.*?)(?=\nGambaran Rejeki|\nFluktuasi)', text, re.DOTALL)
            if m: res['bisnis'] = m.group(1).strip()
            
            m = re.search(r'Gambaran Rejeki \(Hoki\)\s*\n(.*?)(?=\nFluktuasi|< Hitung Kembali)', text, re.DOTALL)
            if m: res['rejeki'] = m.group(1).strip()
            
            print(f"Scraped weton: {name} ({len(res.get('watak', ''))} chars)")
            return name, res
        except Exception as e:
            time.sleep(1)
    print(f"Failed weton {name}: {e}")
    return name, {'weton': name}

# 2. Scrape 30 Wukus from ki-demang.com
def get_wuku_dates():
    # 1945-08-17 is Wuku Manahil (idx 22)
    # Start of Sinta is 22 wukus back = 22 * 7 = 154 days back
    # Let's find dates for all 30 wukus
    anchor_manahil = date(1945, 8, 17) # Friday in Manahil (idx 22)
    sinta_sunday = anchor_manahil - timedelta(days=22*7 + 5) # Sunday in Sinta (idx 0)
    wuku_dates = []
    for idx in range(30):
        w_date = sinta_sunday + timedelta(days=idx*7 + 2) # Tuesday in that wuku
        wuku_dates.append((idx, DAFTAR_WUKU[idx], w_date))
    return wuku_dates

def scrape_one_wuku(item):
    idx, name, dt = item
    url = 'https://ki-demang.com/almanak/?do=watak'
    data = urllib.parse.urlencode({'tg': str(dt.day), 'bl': str(dt.month), 'th': str(dt.year), 'masehi': 'Proses'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            clean = re.sub(r'<[^>]+>', ' ', html)
            clean = re.sub(r'\s+', ' ', clean)
            pos = clean.find('Watak berdasarkan wuku')
            if pos != -1:
                text = clean[pos:pos+2500]
                
                wuku_m = re.search(r'Wuku\s*:\s*([A-Za-z.]+)', text)
                dewa = re.search(r'Dewa Bumi\s*:\s*([^.]+?\.)', text)
                pohon = re.search(r'Pohonnya\s*([^:]+:\s*[^.]+?\.)', text)
                burung = re.search(r'Burungnya\s*([^:]+:\s*[^.]+?\.)', text)
                gedhong = re.search(r'Gedhongnya\s*([^:]+:\s*[^.]+?\.)', text)
                aral = re.search(r'Aralnya\s*:\s*([^.]+?\.)', text)
                sesaji = re.search(r'Sedekah\s*/\s*sesaji\s*:\s*([^.]+?\.)', text)
                doa = re.search(r'Do\'anya\s*:\s*([^.]+?\.)', text)
                kala = re.search(r'Kala Jaya Bumi\s*:\s*(.*?)(?=(?:Saat wukunya|Landep|\. &copy|Wuku|$))', text)
                
                # Ciri khas/perilaku wuku
                ciri_m = re.search(r'(?:Burungnya|Gedhongnya|Kakinya)[^.]*\.\s*(.*?)(?=\s*Aralnya)', text)
                ciri = ciri_m.group(1).strip() if ciri_m else ''
                
                # Baik / Tidak baik untuk
                baik_m = re.search(r'(Wuku\s+[A-Za-z.]+\s+baik untuk\s+.*?)(?=(?:\. &copy|\(adsbygoogle|$))', text)
                baik_text = baik_m.group(1).strip() if baik_m else ''

                res = {
                    'index': idx,
                    'nama': name,
                    'wuku_ki_demang': wuku_m.group(1) if wuku_m else name,
                    'dewa': dewa.group(1).strip() if dewa else '',
                    'pohon': pohon.group(1).strip() if pohon else '',
                    'burung': burung.group(1).strip() if burung else '',
                    'gedhong': gedhong.group(1).strip() if gedhong else '',
                    'ciri': ciri,
                    'aral': aral.group(1).strip() if aral else '',
                    'sesaji': sesaji.group(1).strip() if sesaji else '',
                    'doa': doa.group(1).strip() if doa else '',
                    'kala': kala.group(1).strip() if kala else '',
                    'anjuran': baik_text,
                    'tanggal_sampel': dt.strftime('%Y-%m-%d')
                }
                print(f"Scraped wuku: {name}")
                return name, res
        except Exception as e:
            time.sleep(1)
    print(f"Failed wuku {name}: {e}")
    return name, {'index': idx, 'nama': name}

def main():
    print("=== Scraping 35 Wetons from Primbon.com ===")
    weton_dates = get_weton_dates()
    weton_results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        for name, res in executor.map(scrape_one_weton, weton_dates.items()):
            weton_results[name] = res
            
    with open('data/primbon_weton.json', 'w', encoding='utf-8') as f:
        json.dump(weton_results, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(weton_results)} wetons to data/primbon_weton.json")

    print("\n=== Scraping 30 Wukus from Ki-Demang.com ===")
    wuku_dates = get_wuku_dates()
    wuku_results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        for name, res in executor.map(scrape_one_wuku, wuku_dates):
            wuku_results[name] = res

    with open('data/kidemang_wuku.json', 'w', encoding='utf-8') as f:
        json.dump(wuku_results, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(wuku_results)} wukus to data/kidemang_wuku.json")

if __name__ == '__main__':
    main()
