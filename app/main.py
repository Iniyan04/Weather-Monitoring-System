from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routes import auth, weather, favorites
from app.services.scheduler import start_scheduler

app = FastAPI(title="Weather Monitoring API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(weather.router)
app.include_router(favorites.router)

# ✅ START SCHEDULER (IMPORTANT)
start_scheduler()

@app.get("/")
def root():
    return {"message": "Weather Monitoring API is running"}