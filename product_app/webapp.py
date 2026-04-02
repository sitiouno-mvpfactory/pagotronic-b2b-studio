from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from product_app.landing import render_landing

app = FastAPI()

@app.get("/")
async def root():
    index_path = Path("index.html")
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(), status_code=200)
    return render_landing()
