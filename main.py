from fastapi import FastAPI
import uvicorn, os, json
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# MySQL connection configuration
mysql_config = {
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': os.getenv("HOST"),
    'database': os.getenv("DATABASE"),
}

@app.get("/")
def get_fecha(cedula: int):
    # Connect to MySQL
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()

    # Query to select fecha based on cedula
    query = f"SELECT fecha FROM citas_medicas WHERE cedula = {cedula};"
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    fecha = result[0] if result else None

    conn.close()
    
    return {'fecha': fecha}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT"))
