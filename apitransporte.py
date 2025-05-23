# Comentario en primera línea para vídeo
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especificá tu origen: ["http://192.168.1.70"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
@app.get("/consultatransportista/")
async def consultatransportista():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()  # ❌ No usar dictionary=True aquí

        query = f"SELECT Nombre, Telefono, Direccion, TipoVehiculo FROM Transportistas"
        cursor.execute(query)

        columns_servicios = [col[0] for col in cursor.description]
        servicios_result = [dict(zip(columns_servicios, row)) for row in cursor.fetchall()]

        serviciosdados = [
            {
                "Nombre": item["Nombre"],
                "Telefono": item["Telefono"],
                "Direccion": item["Direccion"],
                "TipoVehiculo": item["TipoVehiculo"],
            }
            for item in servicios_result
        ]

        cursor.close()
        conn.close()

        return {
            "serviciosdados": serviciosdados
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))