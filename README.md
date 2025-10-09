# CSV DATA CLEANER
This FastAPI micro service cleans 'messy' CSV data: The API currently drops duplicates, missing rows, strips white spaces and makes txt lowercase.
Users can upload messy Csv's and then download the cleaned up version.

# Features
-Remove duplicate rows
-Drop rows with missing values
-Standardize column names:
-Lowercase
-Replace spaces with underscores
-Strip leading/trailing whitespace
-Trim whitespace from all string columns
-Automatically download cleaned CSV
-Works entirely in-memory (no temp files)

# Tech stack
Python
FastApi
Pandas

# Notes
-The API works best with CSVs encoded in UTF-8.
-Large CSVs are processed in-memory using io.StringIO to avoid writing temp files.
-Missing values are dropped. You can modify dropna() to handle them differently if needed.
