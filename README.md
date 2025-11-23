# 🗂️ BLO Database Finder — Python + Streamlit Web App

## 📘 Mobile-Friendly Solution for BLO Record Search

### Mobile View

<!-- markdownlint-disable MD033 -->
<img src="res/mobile_view.gif" alt="Mobile View" height="500">
<!-- markdownlint-enable MD033 -->

### PC View

![PC View](res/pc_video.gif)

---

## 🔍 Project Overview

This project is a **Python + Streamlit** web application designed to help **BLOs (Booth Level Officers)** quickly search through **lakh-plus voter records** from large CSV files.

The app:

- Works on **any device** (mobile / tablet / laptop)  
- Supports **Gujarati search** as well as **English → Gujarati translation**  
- Handles **split datasets** (because of GitHub’s 100 MB limit)  
- Provides a **fast, responsive table** for real-time search  

The live app is hosted on **Streamlit Community Cloud**:

🔗 <https://blo-db.streamlit.app/>

---

## 🌱 Problem Statement

My mother works in a government job and was assigned the role of a **BLO (Booth Level Officer)**. BLOs are responsible for:

- Verifying citizen details on the electoral roll  
- Searching, checking, and correcting entries  
- Working with **huge CSV files containing lakhs of records**

## ❌ Old Workflow

- Data opened in **Excel**  
- BLOs used **Ctrl + F** and manual filters  
- Excel became **slow / unresponsive** with such large files  
- Searching by name (especially in **Gujarati**) was difficult  

## ⚠️ Intermediate Google Sheets Solution

My father built a **Google Sheets dashboard using Regex**:

- Allowed flexible text search  
- But became **slow** with big datasets  
- Every user needed the **entire dataset on their own device**  
- Not feasible or secure for all BLOs  

## ✅ Power BI Solution (Desktop Only)

To fix performance, I built a **Power BI dashboard** that handled large data smoothly.  
But Power BI mobile usage requires:

- Power BI Premium account  
- Cannot be used by BLOs on field phones  

## 🧩 Final Python Solution (Accessible Anywhere)

To make the solution **fully mobile-friendly**, I built this **Python Streamlit web app**:

- Runs in any browser  
- Works on any device  
- No installation  
- Handles large datasets  
- Supports Gujarati text and translations  

---

## 🏗️ System Architecture & Flow

```text
User Browser
    ↓
Streamlit Web App (Python)
    - Load CSV Part 1 (data1.csv)
    - Load CSV Part 2 (data2.csv)
    - Merge on primary key (ID)
    - Drop ID column
    - Normalise column names
    - Translate English → Gujarati (for search terms)
    - Apply regex-based filters
    - Generate filtered DataFrame
    ↓
Merged & Filtered Dataset (df_active)
    - In-memory Pandas DataFrame
    - Auto-sized columns
    - Responsive table view
    ↓
Final Output to User
    - Records count
    - Gujarati highlighting
    - Filtered table view
```

---

## 📂 Dataset & Pre-Processing

The dataset was split into **two CSV files** due to GitHub’s 100 MB size limit:

- `data1.csv`  
- `data2.csv`

## 🔑 Key Columns

- `ID` (join key)  
- `serial_no`  
- `name`  
- `relation`  
- `relative_name`  
- `gender`  
- `age`  
- `epic_no`  
- `ac_no`  
- `booth_no`  

## 🧮 Merge Logic

On app start:

1. Load both CSVs using Pandas  
2. Merge using `ID`  
3. Drop `ID` column  
4. Clean column names  
5. Use merged DataFrame (`df_active`) for all filtering  

---

## 🤖 Tech Stack

- **Python 3.x**  
- **Streamlit** (UI)  
- **Pandas** (data processing)  
- **deep-translator** (English → Gujarati translation)  
- **googletrans** (fallback translator)  
- **Regex (re)** (advanced text search)  

All dependencies are listed in:

```text
requirements.txt
```

---

## 🧠 Core Features

## 1️⃣ English → Gujarati Translation

- User types English names  
- App auto-translates them to Gujarati  
- If input is already Gujarati → translation is skipped  
- If deep-translator fails → googletrans fallback is used  

Ensures **accurate Gujarati match filtering**.

---

## 2️⃣ Advanced Multi-Field Filtering

You can filter by:

- **Name 1**  
- **Name 2** (surname)  
- **Relative Name**  
- **Partial EPIC No**  
- **AC Number**  
- **Booth Number**  
- **Serial No Range**  

Uses **Pandas regex filters** to support Gujarati script.

---

## 3️⃣ Responsive Table View

- Scrollable  
- Auto column width  
- Gujarati rendering supported  
- Filtered results count displayed at top  

---

## 4️⃣ Clean Apply / Reset UX

- **Apply** → filters based on all fields  
- **Reset** → clears all fields and restores full dataset  

All filter states are maintained via **st.session_state**.

---

## 🧪 Example Usage

1. Enter `"Amit"` → auto translated to `"અમિત"`  
2. Enter surname in `Name 2`  
3. Enter father’s name in `Relative Name`  
4. Optionally filter by EPIC No, AC, Booth  
5. Click **Apply**  
6. View instantly filtered results  

---

## 🚀 Deployment

Hosted on **Streamlit Community Cloud**:

🔗 <https://blo-db.streamlit.app/>

## Benefits

- No installation  
- Mobile-friendly  
- Very fast  
- Works for any BLO with a phone  

---

## 🛠️ Run Locally

## 1️⃣ Clone Repo

```bash
git clone https://github.com/your-username/BLO-Database-Finder.git
cd BLO-Database-Finder
```

## 2️⃣ Install Packages

```bash
pip install -r requirements.txt
```

## 3️⃣ Run App

```bash
streamlit run app.py
```

---

## 📦 Project Structure

```text
.
├── app.py
├── data1.csv
├── data2.csv
├── requirements.txt
└── README.md
```

---

## 💡 Problems Solved

- Works on **mobile + laptop + tablet**  
- Supports **English to Gujarati translation**  
- Fast filtering for **lakhs of records**  
- No need for Excel or Power BI  
- Dataset split to bypass GitHub limits  

---

## 🔮 Future Enhancements

- Export results to PDF / Excel  
- Fuzzy matching for Gujarati spelling mistakes  
- Hindi + English UI  
- Offline desktop EXE version  

---

## ⭐ Thank You

If this project helped you,  
please ⭐ **star the repository** and share with others!
