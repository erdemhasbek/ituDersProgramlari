"""
İTÜ Ders Programı CSV Oluşturucu
---------------------------------
Kullanım:
    python csvCreator.py

Çıktı:
    data/<donem>/lisans.csv

Gereksinimler:
    pip install requests pandas lxml
"""

import requests
import pandas as pd
import time
import os
from datetime import datetime

BASE_URL = "https://obs.itu.edu.tr/public/DersProgram"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://obs.itu.edu.tr/public/DersProgram/DersProgramSemesterSearch"
}


def get_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.get("https://obs.itu.edu.tr/public/DersProgram/DersProgramSemesterSearch")
    return session


def get_branslar(session, seviye="LS"):
    r = session.get(
        f"{BASE_URL}/SearchBransKoduByProgramSeviye",
        params={"programSeviyeTipiAnahtari": seviye}
    )
    return r.json()


def get_ders_programi(session, brans_id, seviye="LS"):
    from io import StringIO
    r = session.get(
        f"{BASE_URL}/DersProgramSearch",
        params={
            "programSeviyeTipiAnahtari": seviye,
            "dersBransKoduId": brans_id
        }
    )
    tablolar = pd.read_html(StringIO(r.text))
    return tablolar[0] if tablolar else None


def main():
    print("İTÜ Ders Programı çekiliyor...\n")

    # Dönem adını kullanıcıdan al
    donem = input("Dönem adı girin (örn: 2025-2026-bahar): ").strip()
    if not donem:
        donem = datetime.now().strftime("%Y-%m-%d")

    output_dir = os.path.join("data", donem)
    os.makedirs(output_dir, exist_ok=True)

    session = get_session()
    branslar = get_branslar(session)
    print(f"Toplam {len(branslar)} brans bulundu.\n")

    tum_dersler = []

    for i, brans in enumerate(branslar):
        brans_id = brans["bransKoduId"]
        brans_kodu = brans["dersBransKodu"]

        try:
            df = get_ders_programi(session, brans_id)
            if df is not None and len(df) > 0:
                df["bransKodu"] = brans_kodu
                tum_dersler.append(df)
                print(f"[{i+1}/{len(branslar)}] ✓ {brans_kodu}: {len(df)} ders")
            else:
                print(f"[{i+1}/{len(branslar)}] - {brans_kodu}: boş")
        except Exception as e:
            print(f"[{i+1}/{len(branslar)}] ✗ {brans_kodu}: {e}")

        time.sleep(0.4)

    if tum_dersler:
        sonuc = pd.concat(tum_dersler, ignore_index=True)
        output_path = os.path.join(output_dir, "lisans.csv")
        sonuc.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"\n✅ Toplam {len(sonuc)} ders kaydedildi → {output_path}")
    else:
        print("\n❌ Hiç veri çekilemedi.")


if __name__ == "__main__":
    main()
