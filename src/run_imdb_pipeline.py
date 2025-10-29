import ast, os, re, sqlite3
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "imdb.sqlite"
DATA_DIR = ROOT / "data"
EXPORTS_DIR = ROOT / "exports"

print("DB path:", DB_PATH)
print("DB exists?", DB_PATH.exists())

df = pd.DataFrame(columns=["title","content_type","year","certificate","duration","genre","rating","votes"])

data_path = DATA_DIR / "IMDB.csv"
df_raw = pd.read_csv(data_path)

print(df_raw.shape)
print(df_raw.head())
print(df_raw.columns.tolist())


KEEP = ["title","year","certificate","duration","genre","rating","votes"]
df = df_raw[[c for c in KEEP if c in df_raw.columns]].copy()

def derive_content_type_from_certificate(cert):
    ser = pd.Series(cert, dtype="object").astype(str).str.strip()
    out = pd.Series("Movie", index=ser.index)
    out[ser.str.upper().str.startswith("TV")] = "TV Show"
    out[ser.eq("") | ser.str.lower().isin(["nan","none","null"])] = "Unknown"
    return out.astype("string")

df["content_type"] = derive_content_type_from_certificate(df["certificate"])


def to_int_from_any(s):
    return (
        pd.Series(s, dtype="object")
          .astype(str)
          .str.replace(r"\D", "", regex=True)
          .pipe(pd.to_numeric, errors="coerce")
          .astype("Int64")
    )

df["year"] = to_int_from_any(df["year"])
df["duration"] = to_int_from_any(df["duration"])
df["votes"] = to_int_from_any(df["votes"])


def to_float(s):
    return pd.to_numeric(pd.Series(s), errors="coerce")

df["rating"] = to_float(df["rating"])

for col in ["title", "certificate", "genre", "content_type"]:
    if col in df.columns:
        df[col] = df[col].astype("string")

current_rows = len(df)

REQUIRED = ["title","rating","votes","year"]
df = df.dropna(subset=[c for c in REQUIRED if c in df.columns])

if "rating" in df.columns:
    df = df[((df["rating"] >= 1.0) & (df["rating"] <= 10.0))]
if "year" in df.columns:
    df = df[((df["year"] >= 1900) & (df["year"] <= 2030))]
if "duration" in df.columns:
    df = df[(df["duration"].isna()) | (df["duration"] > 0)]
if "votes" in df.columns:
    df = df[(df["votes"] >= 0)]

df = df.drop_duplicates(subset=["title"], keep="first")
df = df.sort_values(by="votes", ascending=False)

df = df.reset_index(drop=True)

final_order = [
    "title",
    "content_type",
    "year",
    "certificate",
    "duration",
    "genre",
    "rating",
    "votes"
]

df = df[[col for col in final_order if col in df.columns]]
print(df[["title", "certificate", "content_type","votes","rating"]].head(10))

with sqlite3.connect(DB_PATH) as con:
    df.to_sql("imdb_clean", con, if_exists="replace", index=False)

print(current_rows, len(df))

csv_path = EXPORTS_DIR / "imdb_clean.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"Exported CSV to {csv_path}")
