import streamlit as st
import pandas as pd
import re
import sys, subprocess
from typing import Optional, List

# -------------------------
# Page + styles
# -------------------------
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        .stDataFrame { height: 90vh !important; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("BLO Database")


# -------------------------
# Translator (deep-translator preferred; googletrans fallback)
# -------------------------
@st.cache_resource(show_spinner=False)
def init_translators():
    primary = None
    fallback = None
    try:
        from deep_translator import GoogleTranslator  # type: ignore

        primary = GoogleTranslator(source="auto", target="gu")
    except Exception:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "deep-translator==1.11.4"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            from deep_translator import GoogleTranslator  # type: ignore

            primary = GoogleTranslator(source="auto", target="gu")
        except Exception:
            primary = None
    try:
        from googletrans import Translator  # type: ignore

        fallback = Translator()
    except Exception:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "googletrans==4.0.0-rc1"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            from googletrans import Translator  # type: ignore

            fallback = Translator()
        except Exception:
            fallback = None
    return primary, fallback


primary_tr, fallback_tr = init_translators()


def is_gujarati(text: str) -> bool:
    return any(0x0A80 <= ord(ch) <= 0x0AFF for ch in text or "")


def to_gujarati(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if is_gujarati(text):
        return text
    if primary_tr is not None:
        try:
            return (primary_tr.translate(text) or "").strip()
        except Exception:
            pass
    if fallback_tr is not None:
        try:
            res = fallback_tr.translate(text, dest="gu")
            return (res.text or "").strip()
        except Exception:
            pass
    return text


if primary_tr is None and fallback_tr is None:
    st.caption("⚠️ Translation unavailable. Using typed text for search.")


# -------------------------
# Helpers
# -------------------------
def detect_col(
    df: pd.DataFrame, candidates: List[str], fallback_idx: Optional[int] = None
) -> Optional[str]:
    lowered = {c.lower(): c for c in df.columns}
    for cand in candidates:
        key = cand.lower().strip()
        if key in lowered:
            return lowered[key]
    if fallback_idx is not None and 0 <= fallback_idx < len(df.columns):
        return df.columns[fallback_idx]
    return None


def filter_df(
    df: pd.DataFrame,
    name1_gu: str,
    name2_gu: str,
    rel_gu: str,
    serial_from: Optional[float],
    serial_to: Optional[float],
    epic: str,
    ac: str,
) -> pd.DataFrame:

    serial_col = detect_col(
        df, ["serial_no", "serial no", "srno", "sr_no"], fallback_idx=0
    )
    name_col = detect_col(df, ["name", "નામ"], fallback_idx=1)
    rel_col = detect_col(
        df, ["relative_name", "relative name", "સંબંધિત નામ"], fallback_idx=3
    )
    epic_col = detect_col(df, ["epic_no", "epic no", "epic"], None)
    ac_col = detect_col(df, ["ac_no", "ac no", "ac"], None)

    mask = pd.Series(True, index=df.index)

    if name_col:
        if name1_gu.strip():
            mask &= (
                df[name_col]
                .astype(str)
                .str.contains(
                    re.escape(name1_gu.strip()),
                    regex=True,
                    flags=re.IGNORECASE,
                    na=False,
                )
            )
        if name2_gu.strip():
            mask &= (
                df[name_col]
                .astype(str)
                .str.contains(
                    re.escape(name2_gu.strip()),
                    regex=True,
                    flags=re.IGNORECASE,
                    na=False,
                )
            )
    if rel_col and rel_gu.strip():
        mask &= (
            df[rel_col]
            .astype(str)
            .str.contains(
                re.escape(rel_gu.strip()), regex=True, flags=re.IGNORECASE, na=False
            )
        )

    if serial_col:
        serial_numeric = pd.to_numeric(df[serial_col], errors="coerce")
        if serial_from is not None:
            mask &= serial_numeric >= serial_from
        if serial_to is not None:
            mask &= serial_numeric <= serial_to

    if epic_col and epic.strip():
        mask &= (
            df[epic_col]
            .astype(str)
            .str.contains(
                re.escape(epic.strip()), regex=True, flags=re.IGNORECASE, na=False
            )
        )
    if ac_col and ac.strip():
        mask &= (
            df[ac_col]
            .astype(str)
            .str.contains(
                re.escape(ac.strip()), regex=True, flags=re.IGNORECASE, na=False
            )
        )

    return df[mask]


# -------------------------
# DATA LOAD + MERGE USING ID
# -------------------------

st.subheader("Upload 2 files to merge using ID")

file1 = st.file_uploader("Upload File 1", type=["csv"], key="f1")
file2 = st.file_uploader("Upload File 2", type=["csv"], key="f2")

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    if "ID" not in df1.columns or "ID" not in df2.columns:
        st.error("❌ Both files must contain an 'ID' column.")
        st.stop()

    # 1) Merge on ID
    df_active = pd.merge(df1, df2, on="ID", how="inner")

    # 2) Drop the ID field
    df_active = df_active.drop(columns=["ID"])

    st.success(
        f"✔ Merge successful. Final rows: {len(df_active)} ; Columns: {len(df_active.columns)}"
    )

else:
    st.warning("Please upload both files to generate the merged dataset.")
    st.stop()

st.markdown("---")

# -------------------------
# Filters UI (Apply + Reset, no rerun in callback)
# -------------------------
# Serial bounds from data
serial_col = detect_col(df_active, ["serial_no", "srno"], fallback_idx=0)
min_serial = max_serial = None
if serial_col:
    sn = pd.to_numeric(df_active[serial_col], errors="coerce")
    if sn.notna().any():
        min_serial = float(sn.min())
        max_serial = float(sn.max())

st.subheader("Search Filters")

# Initialize state once (defaults here)
ss = st.session_state
ss.setdefault("name1", "")
ss.setdefault("name2", "")
ss.setdefault("rel", "")
ss.setdefault("epic", "")
ss.setdefault("ac", "")
ss.setdefault("serial_from", min_serial if min_serial is not None else 0.0)
ss.setdefault("serial_to", max_serial if max_serial is not None else 0.0)


def reset_filters():
    ss.name1 = ""
    ss.name2 = ""
    ss.rel = ""
    ss.epic = ""
    ss.ac = ""
    ss.serial_from = min_serial if min_serial is not None else 0.0
    ss.serial_to = max_serial if max_serial is not None else 0.0
    # DO NOT call st.rerun() here — button press will rerun automatically.


# Row 1: names
r1c1, r1c2, r1c3 = st.columns([1.4, 1.4, 1.4])
with r1c1:
    st.text_input("Name 1 (English or Gujarati)", key="name1")
    n1_gu = to_gujarati(ss.name1)
    if ss.name1:
        st.caption(f"→ Gujarati: **{n1_gu}**")
with r1c2:
    st.text_input("Name 2 (English or Gujarati)", key="name2")
    n2_gu = to_gujarati(ss.name2)
    if ss.name2:
        st.caption(f"→ Gujarati: **{n2_gu}**")
with r1c3:
    st.text_input("Relative_Name (English or Gujarati)", key="rel")
    rel_gu = to_gujarati(ss.rel)
    if ss.rel:
        st.caption(f"→ Gujarati: **{rel_gu}**")

# Row 2: serial/epic/ac
r2c1, r2c2, r2c3, r2c4 = st.columns([1, 1, 1.2, 1.2])
with r2c1:
    if min_serial is not None and max_serial is not None:
        st.number_input(
            "Serial From",
            key="serial_from",
            step=1.0,
            format="%.0f",
            min_value=float(min_serial),
            max_value=float(max_serial),
        )
    else:
        st.number_input("Serial From", key="serial_from", step=1.0, format="%.0f")
with r2c2:
    if min_serial is not None and max_serial is not None:
        st.number_input(
            "Serial To",
            key="serial_to",
            step=1.0,
            format="%.0f",
            min_value=float(min_serial),
            max_value=float(max_serial),
        )
    else:
        st.number_input("Serial To", key="serial_to", step=1.0, format="%.0f")
with r2c3:
    st.text_input("EPIC No (partial)", key="epic")
with r2c4:
    st.text_input("AC No (partial)", key="ac")

# Row 3: Reset + Apply
r3c1, r3c2, r3c3 = st.columns([5, 1, 1])
with r3c2:
    st.button("Reset", type="secondary", on_click=reset_filters)
with r3c3:
    apply = st.button("Apply", type="primary")

# Guard: keep 'To' ≥ 'From'
if ss.serial_to < ss.serial_from:
    ss.serial_to = ss.serial_from

# Display
ignore_range = (
    min_serial is None
    and max_serial is None
    and ss.serial_from == 0
    and ss.serial_to == 0
)

if apply:
    sf = None if ignore_range else ss.serial_from
    stv = None if ignore_range else ss.serial_to
    filtered = filter_df(
        df_active,
        to_gujarati(ss.name1),
        to_gujarati(ss.name2),
        to_gujarati(ss.rel),
        sf,
        stv,
        ss.epic,
        ss.ac,
    )
    st.info(f"Showing {len(filtered)} records out of {len(df_active)}")
    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True,
        column_config={
            col: st.column_config.Column(width="auto") for col in filtered.columns
        },
    )


else:
    st.info(f"Showing all {len(df_active)} records")
    st.dataframe(
        df_active,
        hide_index=True,
        use_container_width=True,
        column_config={
            col: st.column_config.Column(width="auto") for col in df_active.columns
        },
    )
