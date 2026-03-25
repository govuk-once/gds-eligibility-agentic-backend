import json
from pathlib import Path
from typing import Any
from fastapi import FastAPI

app = FastAPI(title="Eligibility Agent Discovery Registry")

@app.get("/catalog")
def get_agent_catalog() -> dict[str, list[Any]]:
    """Scans the agents directory and returns all A2A agent.json cards."""
    agents_dir = Path(__file__).resolve().parent.parent
    
    catalog: list[Any] = []
    for card_path in agents_dir.rglob("agent.json"):
        try:
            with open(card_path, "r") as f:
                card_data = json.load(f)
                catalog.append(card_data)
        except Exception as e:
            print(f"Failed to read card {card_path}: {e}")
            
    return {"services": catalog}

if __name__ == "__main__":
    import uvicorn
    # Boot the registry on port 7999 so it doesn't conflict with agents
    print("🚀 Booting Agent Discovery Registry on port 7999...")
    uvicorn.run(app, host="0.0.0.0", port=7999)