from fastapi import File, FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
from io import StringIO
import io

app = FastAPI(title="A Data Cleaner API")

@app.get("/")
def home():
    return {"message": "Welcome to the Data Cleaner API"}

@app.post("/Clean-CSV/")
async def clean_csv(file: UploadFile = File(...)):
    # Read uploaded file into a pandas DataFrame
    contents = await file.read()
    df = pd.read_csv(
        StringIO(contents.decode("utf-8")),
        keep_default_na=False,
        na_filter=False         
    )

    # Clean column names: strip, lowercase, replace spaces with underscores
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # This will turn "", " ", "   " into "NA"
    df.replace(r'^\s*$', "NA", regex=True, inplace=True)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    
    if "name" in df.columns:
        df["name"] = df["name"].where(
            df["name"] == "NA",     
            df["name"].str.title()             
        )

    # Stream cleaned CSV back as a downloadable file
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    filename = f"Cleaned_{file.filename}"
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
