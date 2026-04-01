from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# ---------------- USERS TABLE ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    favorites = relationship("Favorite", back_populates="user")


# ---------------- CITIES TABLE ----------------
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, default="Unknown")

    weather_records = relationship("WeatherRecord", back_populates="city")
    favorites = relationship("Favorite", back_populates="city")


# ---------------- WEATHER RECORDS ----------------
class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    temperature = Column(Float)
    humidity = Column(Float)
    date = Column(String)  # Store as YYYY-MM-DD

    city = relationship("City", back_populates="weather_records")


# ---------------- FAVORITES ----------------
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))

    user = relationship("User", back_populates="favorites")
    city = relationship("City", back_populates="favorites")


# ---------------- API LOGS ----------------
class APILog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)