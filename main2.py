from fastapi import FastAPI, HTTPException, UploadFile, File
import pandas as pd
import mysql.connector
import io
import traceback

app = FastAPI()

def create_table_if_not_exists(cursor, table_name, df):
    """Dynamically create a table based on CSV columns if it does not exist."""
    column_types = []
    
    for col in df.columns:
        col_name = col.strip().replace(" ", "_")  # Clean column name
        sample_value = df[col].dropna().astype(str).head(1).values
        
        # Determine column type
        if sample_value.size > 0:
            if sample_value[0].isdigit():
                column_type = "INT"
            else:
                column_type = "VARCHAR(255)"
        else:
            column_type = "VARCHAR(255)"  # Default type
        
        column_types.append(f"{col_name} {column_type}")

    columns_sql = ", ".join(column_types)
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
    
    cursor.execute(create_table_query)

def upload_csv_to_mysql(file: UploadFile):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root_password",
            database="mysql"
        )
        cursor = conn.cursor()

        contents = file.file.read()
        try:
            df = pd.read_csv(io.StringIO(contents.decode("utf-8", errors="ignore")))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"CSV Format Error: {str(e)}")

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty.")

        print("CSV Loaded Successfully:\n", df.head())  # Debugging log

        table_name = "uploaded_data"

        df.columns = [col.strip().replace(" ", "_") for col in df.columns]

        create_table_if_not_exists(cursor, table_name, df)

        # Insert data into MySQL
        columns = ", ".join(df.columns)
        values_placeholder = ", ".join(["%s"] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"

        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        conn.close()
        return {"message": "CSV uploaded successfully"}

    except HTTPException as http_ex:
        raise http_ex  # Re-raise HTTP exceptions

    except Exception as e:
        print("Error Occurred:", traceback.format_exc())  # Print full error traceback
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/upload_csv")
def upload_csv(file: UploadFile = File(...)):
    return upload_csv_to_mysql(file)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)