"""FastAPI приложение для нагрузочного тестирования."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .booking_service import calculate_booking_price, ValidationError

app = FastAPI(title="Booking Pricing API")

class BookingRequest(BaseModel):
    base_price: int
    age: int
    is_weekend: bool
    promo_code: Optional[str] = None

class BookingResponse(BaseModel):
    price: int

@app.post("/calculate", response_model=BookingResponse)
def calc_endpoint(req: BookingRequest):
    """Рассчитывает итоговую стоимость бронирования."""
    try:
        price = calculate_booking_price(
            base_price=req.base_price,
            age=req.age,
            is_weekend=req.is_weekend,
            promo_code=req.promo_code
        )
        return BookingResponse(price=price)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    """Проверка работоспособности."""
    return {"status": "ok"}