from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.services.weather_fetcher import fetch_weather_from_api

router = APIRouter(prefix="/weather", tags=["Weather"])


# ---------------- FETCH WEATHER ----------------
@router.get("/fetch/{city}", response_model=schemas.WeatherResponse)
def fetch_weather(city: str, db: Session = Depends(get_db)):
    try:
        data = fetch_weather_from_api(city)

        if not data:
            crud.log_api(db, "/weather/fetch", "failed")
            raise HTTPException(status_code=404, detail="City not found or API failed")

        city_obj = crud.get_or_create_city(db, city)

        crud.save_weather(
            db,
            city_id=city_obj.id,
            temp=data["temperature"],
            humidity=data["humidity"],
            date=data["date"]
        )

        crud.log_api(db, "/weather/fetch", "success")

        return {
            "city": city,
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "date": data["date"]
        }

    except Exception as e:
        crud.log_api(db, "/weather/fetch", "error")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- WEATHER HISTORY ----------------
@router.get("/history/{city}")
def get_history(city: str, db: Session = Depends(get_db)):
    try:
        records = crud.get_weather_history(db, city)

        if not records:
            crud.log_api(db, "/weather/history", "failed")
            raise HTTPException(status_code=404, detail="No weather data found")

        result = []
        for r in records:
            result.append({
                "city": city,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "date": r.date
            })

        crud.log_api(db, "/weather/history", "success")
        return result

    except Exception as e:
        crud.log_api(db, "/weather/history", "error")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- WEATHER BY DATE ----------------
@router.get("/date/{city}")
def get_weather_by_date(city: str, date: str, db: Session = Depends(get_db)):
    try:
        records = crud.get_weather_history(db, city)

        for r in records:
            if r.date.startswith(date):
                crud.log_api(db, "/weather/date", "success")
                return {
                    "city": city,
                    "temperature": r.temperature,
                    "humidity": r.humidity,
                    "date": r.date
                }

        crud.log_api(db, "/weather/date", "failed")
        raise HTTPException(status_code=404, detail="No data for given date")

    except Exception as e:
        crud.log_api(db, "/weather/date", "error")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- COMPARE WEATHER ----------------
@router.get("/compare")
def compare_weather(city: str, date1: str, date2: str, db: Session = Depends(get_db)):
    try:
        records = crud.get_weather_history(db, city)

        data1 = None
        data2 = None

        for r in records:
            if r.date.startswith(date1):
                data1 = r
            if r.date.startswith(date2):
                data2 = r

        if not data1 or not data2:
            crud.log_api(db, "/weather/compare", "failed")
            raise HTTPException(status_code=404, detail="Data not found for comparison")

        crud.log_api(db, "/weather/compare", "success")

        return {
            "city": city,
            "date1": {
                "temperature": data1.temperature,
                "humidity": data1.humidity
            },
            "date2": {
                "temperature": data2.temperature,
                "humidity": data2.humidity
            }
        }

    except Exception as e:
        crud.log_api(db, "/weather/compare", "error")
        raise HTTPException(status_code=500, detail=str(e))