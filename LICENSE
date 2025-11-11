---

## ⚙️ main.py
```python
from fastapi import FastAPI
from crafting_engine import craft_item
from blueprint_engine import discover_blueprint

app = FastAPI(title="Realm of Echoes")

@app.get("/")
def root():
    return {"message": "Welcome to Realm of Echoes — where creation reshapes the world."}

@app.post("/craft")
def craft(payload: dict):
    return craft_item(payload)

@app.post("/discover")
def discover(payload: dict):
    return discover_blueprint(payload)
