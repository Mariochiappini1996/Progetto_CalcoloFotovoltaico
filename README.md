# SunPark: Simulatore di Calcolo Fotovoltaico

## Architettura del Sistema
L'architettura è suddivisa in due macro-componenti principali: il backend computazionale e l'interfaccia utente (frontend), orchestrati tramite engine di containerizzazione.

### 1. Livello di Backend (REST API)
Il core computazionale è implementato in Python utilizzando **FastAPI**. 
* **Validazione dei Dati:** Sfrutta `pydantic` per definire il modello di dominio (`PlantData`), garantendo la tipizzazione statica e la validazione automatica del payload JSON in ingresso.
* **Logica di Calcolo:** L'endpoint `POST /api/simulate` riceve la potenza dell'impianto e la zona geografica. Il calcolo della produzione annua si basa sulla seguente formula deterministica:
  E = P * h * PR
  Dove:
  * E è l'energia prodotta (Produzione Annua in kWh).
  * P è la potenza nominale dell'impianto in kWp.
  * h rappresenta le ore equivalenti di sole, modellate tramite una mappa chiave-valore statica (Nord: 1000, Centro: 1200, Sud: 1500).
  * PR è il Performance Ratio, fissato precauzionalmente a uno scalare di 0.75 per modellare le perdite di sistema (termiche, inverte, cablaggio).
* **Server ASGI:** Il servizio è servito tramite `uvicorn`, garantendo la gestione asincrona delle richieste concorrenti sulla porta 8000.

[ Informazioni richieste a ChatGPT ]

### 2. Livello di Frontend (Interfaccia Utente)
Il client è sviluppato in modalità Single Page Application (SPA) monolitica, utilizzando HTML5, CSS3 (con variabili native) e JavaScript (Vanilla).
* **Integrazione API:** La comunicazione con il backend avviene in modalità asincrona tramite l'API `fetch`, gestendo la serializzazione/deserializzazione JSON e le eventuali eccezioni di rete.
* **Rendering Dinamico:** Il DOM viene manipolato dinamicamente alla risoluzione della Promise per mostrare la card dei risultati.
* **Generazione Reportistica:** Integra la libreria esterna `html2pdf.js` per esportare la porzione della viewport (DOM snapshot) in formato PDF client-side, ottimizzando il documento in formato A4 con compressione JPEG.

### 3. Containerizzazione e Deployment
L'intero stack applicativo è containerizzato tramite Docker, garantendo riproducibilità e isolamento dell'ambiente di esecuzione.
* **Immagine Base:** Utilizza `python:3.11-slim` per minimizzare la footprint del container.
* **Port Mapping:** Il container espone il traffico sulla porta `8000`.
* **Orchestrazione:** Il file `docker-compose.yml` definisce il servizio `simulator_app`, semplificando il processo di build e l'iniezione delle variabili d'ambiente (es. `ENVIRONMENT=production`).

## Requisiti di Esecuzione
Per avviare il progetto in ambiente locale, è necessario aver installato Docker e Docker Compose.

1. Clonare il repository.
2. Costruire ed avviare il container eseguendo il comando:
   ```bash
   docker-compose up --build
