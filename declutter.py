from fastapi import File, FastAPI, UploadFile
import pandas as pd
from io import StringIO

app = FastAPI(title="A Data Cleaner API")

@app.get("/")
def home():
    return {"message": "Welcome to the Data Cleaner API "}

@app.post("/Clean-CSV/")
async def clean_csv(file: UploadFile = File(...)):
    # Read uploaded file
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    # Save original count
    rows_before = len(df)

    # Clean column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Drop duplicates and missing rows
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # Prepare cleaned summary
    result = {
        "rows_before": rows_before,
        "rows_after": len(df),
        "columns": list(df.columns),
        "preview": df.head(5).to_dict(orient="records")
    }

    return result
