from pydantic import BaseModel, ConfigDict
from typing import Optional


# ---------------- USER ----------------
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


# ---------------- CITY ----------------
class CityBase(BaseModel):
    name: str
    country: Optional[str] = "Unknown"

    model_config = ConfigDict(from_attributes=True)


# ---------------- WEATHER ----------------
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: float
    date: str

    model_config = ConfigDict(from_attributes=True)


# ---------------- FAVORITES ----------------
class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)