from sqlalchemy.orm import Session
from app import models
from datetime import datetime


# ---------------- USER ----------------
def create_user(db: Session, username: str, password: str):
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ---------------- CITY ----------------
def get_or_create_city(db: Session, city_name: str):
    city = db.query(models.City).filter(models.City.name == city_name).first()
    if not city:
        city = models.City(name=city_name)
        db.add(city)
        db.commit()
        db.refresh(city)
    return city


# ---------------- WEATHER ----------------
def save_weather(db: Session, city_id: int, temp: float, humidity: float, date: str):
    record = models.WeatherRecord(
        city_id=city_id,
        temperature=temp,
        humidity=humidity,
        date=date
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_weather_history(db: Session, city_name: str):
    return db.query(models.WeatherRecord).join(models.City).filter(models.City.name == city_name).all()


# ---------------- FAVORITES ----------------
def add_favorite(db: Session, user_id: int, city_id: int):
    fav = models.Favorite(user_id=user_id, city_id=city_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


def get_user_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

def log_api(db, endpoint: str, status: str):
    log = models.APILog(endpoint=endpoint, status=status)
    db.add(log)
    db.commit()