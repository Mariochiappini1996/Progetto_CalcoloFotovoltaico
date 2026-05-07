from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


app = FastAPI(title="Test Tecnico SUNPARK Chiappini Mario", description="API per calcolo fotovoltaico")

app.mount("/static", StaticFiles(directory="static"), name="static")

class PlantData(BaseModel):
    potenza: float
    zona_interesse: str = Field(..., alias="Zona_interesse")

    model_config = {
        "populate_by_name": True
    }

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/api/simulate")
async def simulate_plant(data: PlantData):
    irraggiamento_map = {
        "Nord": 1000,
        "Centro": 1200,
        "Sud": 1500
    }

    ore_sole = irraggiamento_map.get(data.zona_interesse, 1200)
    performance_ratio = 0.75

    produz_annua = data.potenza * ore_sole * performance_ratio

    return {
        "impianto": { "potenza": data.potenza, "zona": data.zona_interesse },
        "risultati": {"produzione_annua_kWh": round(produz_annua, 2) },
        "stato": "Successo"
    }

