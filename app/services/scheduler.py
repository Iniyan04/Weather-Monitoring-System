from apscheduler.schedulers.background import BackgroundScheduler
from app.services.weather_fetcher import fetch_weather_from_api
from app.database import SessionLocal
from app import crud
from datetime import datetime


def fetch_and_store():
    db = SessionLocal()

    print("\n Scheduler running at:", datetime.now())

    cities = ["bangalore", "chennai", "delhi"]

    for city in cities:
        print(f"\n Fetching weather for {city}...")

        data = fetch_weather_from_api(city)

        if data:
            city_obj = crud.get_or_create_city(db, city)

            crud.save_weather(
                db,
                city_id=city_obj.id,
                temp=data["temperature"],
                humidity=data["humidity"],
                date=data["date"]
            )

            print(f"Stored weather for {city} → Temp: {data['temperature']}°C")

        else:
            print(f" Failed to fetch data for {city}")

    print("✅ Scheduler cycle completed\n")

    db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run every 1 minute (for testing)
    scheduler.add_job(fetch_and_store, "interval", minutes=1)

    scheduler.start()
