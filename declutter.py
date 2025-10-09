from fastapi import File, FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
from io import StringIO 
import io

app = FastAPI(title="A Data Cleaner API")

@app.get("/")
def home():
    return {"message": "Welcome to the Data Cleaner API "}

@app.post("/Clean-CSV/")
async def clean_csv(file: UploadFile = File(...)):
    # Read uploaded file
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    # Clean column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Drop duplicates and missing rows
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    stream = io.StringIO()

    df.to_csv(stream, index=False)
    stream.seek(0)
    

    filename = f"Cleaned_{file.filename}"
    return StreamingResponse(
        stream, 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
