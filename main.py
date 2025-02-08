from code_generator import StandardizeFormatCodeGenerator
from db_connection.db_utils import upload_to_mysql
from fastapi import FastAPI, HTTPException, Query
import json
import mysql.connector

app = FastAPI()

def fetch_data(table_name: str):
    try:
        conn = mysql.connector.connect(
            host="10.10.240.93",
            user="app_user",
            password="app_password",
            database="payment_resolution"
        )
        cursor = conn.cursor()
        
        # Prevent SQL injection by using parameterized query
        query = f"SELECT * FROM {table_name} LIMIT 5;"
        cursor.execute(query)
        
        # Fetch column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch rows and convert to dict
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch")
def get_data(table_name: str = Query(..., description="Name of the table")):
    data = fetch_data(table_name)
    return {"table": table_name, "data": data}
 

# if __name__ == '__main__':
#     code_gen = StandardizeFormatCodeGenerator('')
#     generated_code = code_gen.generate()
#     clean_code = generated_code.replace("```python", "", 1).strip("```")
#     upload_to_mysql(clean_code, 'payment')
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

    
    