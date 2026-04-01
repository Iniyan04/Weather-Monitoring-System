from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, models

router = APIRouter(prefix="/favorites", tags=["Favorites"])


# ---------------- ADD FAVORITE ----------------
@router.post("/{user_id}/{city}")
def add_favorite(user_id: int, city: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    city_obj = crud.get_or_create_city(db, city)
    crud.add_favorite(db, user_id, city_obj.id)

    return {"message": f"{city} added to favorites"}


# ---------------- GET FAVORITES ----------------
@router.get("/{user_id}")
def get_favorites(user_id: int, db: Session = Depends(get_db)):

    favorites = db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

    result = []
    for f in favorites:
        city = db.query(models.City).filter(models.City.id == f.city_id).first()

        result.append({
            "user_id": f.user_id,
            "city": city.name
        })

    return result