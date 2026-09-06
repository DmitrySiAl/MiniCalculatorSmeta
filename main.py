from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Мини-калькулятор сметы")

@app.post("/items", response_model=schemas.EstimateItemResponse)
def create_item(item: schemas.EstimateItemCreate, db: Session = Depends(get_db)):
    db_item = models.EstimateItem(title = item.title, quantity=item.quantity, unit_price=item.unit_price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.EstimateItem).filter(models.EstimateItem.id == item_id).first()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Позиция не найдена")

    db.delete(db_item)
    db.commit()
    return {"message":f"Позиция с ID {item_id} успешно удалена"}

@app.get("/estimate", response_model=schemas.EstimateResponse)
def get_estimate(markup_percent: float = 0.0, db: Session = Depends(get_db)):
    items = db.query(models.EstimateItem).all()

    subtotal = sum(item.quantity * item.unit_price for item in items)
    grand_total = subtotal * (1 + markup_percent/100)

    return {
        "items": items,
        "markup_percent": markup_percent,
        "subtotal": round(subtotal, 2),
        "grand_total": round(grand_total, 2)
    }