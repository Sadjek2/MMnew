"""Модуль расчета стоимости бронирования."""
from typing import Optional

DISCOUNT_AGE_PERCENT = 0.20  # 20%
DISCOUNT_PROMO_PERCENT = 0.15  # 15%
SURCHARGE_WEEKEND = 100  # рублей
MIN_PRICE = 50  # рублей
PROMO_CODE = "STUDENT2026"


def calculate_total(
    base_price: int,
    age: int,
    is_weekend: bool,
    promo_code: Optional[str] = None
) -> int:
    
    has_age_discount = age < 18 or age >= 65
    
    current_price = float(base_price)

    if has_age_discount:
        current_price *= (1 - DISCOUNT_AGE_PERCENT)

    if promo_code == PROMO_CODE and not has_age_discount:
        current_price *= (1 - DISCOUNT_PROMO_PERCENT)
    
    if is_weekend:
        current_price += SURCHARGE_WEEKEND
        
    final_price = int(max(current_price, MIN_PRICE))
    
    return final_price