# ITU Course Schedule Archive

A searchable, filterable archive of Istanbul Technical University undergraduate course schedules. Data is fetched from ITU OBS.

**🌐 Live site:** [erdemhasbek.github.io/ituDersProgramlari](https://erdemhasbek.github.io/ituDersProgramlari)

---

## Features

- Browse all departments in one place
- Filter by semester, department, day, building, and instructor
- Search by course name or code
- Quota fill-rate indicator
- Download filtered results as CSV
- Historical archive — old semesters are preserved

---

## Adding a New Semester

**1. Fetch the data:**
```bash
pip install requests pandas lxml
python csvCreator.py
# Enter semester name when prompted, e.g: 2025-2026-guz
```

**2. Convert to JSON:**
```bash
python csv_to_json.py
```

**3. Register the semester in `index.html`:**
```javascript
const DONEMLER = [
  { label: "2025-2026 Bahar", path: "data/2025-2026-bahar/lisans.json" },
  { label: "2025-2026 Güz",   path: "data/2025-2026-guz/lisans.json" }  // ← add here
];
```

**4. Push to GitHub.** Old semester data stays untouched.

---

## Project Structure

```
ituDersProgramlari/
├── index.html          # Web interface
├── csvCreator.py       # Fetches data from ITU OBS
├── csv_to_json.py      # Converts CSV to JSON for the site
├── data/
│   ├── 2025-2026-bahar/
│   │   ├── lisans.csv
│   │   └── lisans.json
│   └── ...             # Past semesters stay here
└── README.md
```

---

## Deploying to GitHub Pages

1. Push all files to the `main` branch
2. Go to **Settings → Pages → Branch: main**
3. Site will be live at [erdemhasbek.github.io/ituDersProgramlari](https://erdemhasbek.github.io/ituDersProgramlari)

---

## Data Source

All data is fetched from the official ITU OBS:  
[obs.itu.edu.tr](https://obs.itu.edu.tr/public/DersProgram/DersProgramSemesterSearch)

This project is not affiliated with ITU.
