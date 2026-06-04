"""Слой сервиса для бронирования (Валидация + Интеграция)."""
from typing import Optional
from .pricing import calculate_total

class ValidationError(Exception):
    """Ошибка валидации входных данных."""
    pass


def calculate_booking_price(
    base_price: int,
    age: int,
    is_weekend: bool,
    promo_code: Optional[str] = None
) -> int:
    """
    Публичный метод для расчета цены.
    Выполняет валидацию перед передачей в pricing.py
    """
    
    # Валидация типов и значений
    if not isinstance(base_price, int) or not isinstance(age, int):
        raise ValidationError("Цена и возраст должны быть целыми числами.")
    
    if base_price <= 0:
        raise ValidationError("Базовая цена должна быть строго больше 0.")
        
    if age < 0:
        raise ValidationError("Возраст не может быть отрицательным.")

    # Вызов чистой функции бизнес-логики
    return calculate_total(
        base_price=base_price,
        age=age,
        is_weekend=is_weekend,
        promo_code=promo_code
    )