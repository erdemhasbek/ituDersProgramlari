"""
CSV → JSON Dönüştürücü
-----------------------
csvCreator.py ile oluşturduktan sonra bu scripti çalıştırın.
data/<donem>/lisans.csv → data/<donem>/lisans.json

Kullanım:
    python csv_to_json.py
"""

import pandas as pd
import json
import os
import glob


def convert(csv_path):
    json_path = csv_path.replace('.csv', '.json')
    df = pd.read_csv(csv_path)
    records = df.fillna('-').to_dict(orient='records')
    for r in records:
        if isinstance(r.get('CRN'), float):
            r['CRN'] = int(r['CRN'])
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False)
    print(f"✓ {csv_path} → {json_path}  ({len(records)} kayıt)")


def main():
    csv_files = glob.glob('data/*/lisans.csv')
    if not csv_files:
        print("Hiç CSV bulunamadı. Önce csvCreator.py çalıştırın.")
        return
    for f in sorted(csv_files):
        convert(f)


if __name__ == '__main__':
    main()
