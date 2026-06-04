"""Модуль расчета стоимости бронирования."""
from typing import Optional

# Константы правил бизнес-логики
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
    """
    Рассчитывает итоговую стоимость билета.
    
    Правила (строго в порядке):
    1. Базовая цена должна быть > 0 (проверяется в service).
    2. Скидка по возрасту (20%), если age < 18 или age >= 65.
    3. Промокод (15%), только если нет скидки по возрасту.
    4. Наценка за выходные (+100 руб), после скидок.
    5. Минимальная граница (50 руб).
    """
    
    # 2. Определяем, применима ли скидка по возрасту
    has_age_discount = age < 18 or age >= 65
    
    # Начинаем с базовой цены
    current_price = float(base_price)
    
    # Применяем скидку по возрасту
    if has_age_discount:
        current_price *= (1 - DISCOUNT_AGE_PERCENT)
    
    # 3. Применяем промокод (только если нет возрастной скидки)
    if promo_code == PROMO_CODE and not has_age_discount:
        current_price *= (1 - DISCOUNT_PROMO_PERCENT)
    
    # 4. Наценка за выходные
    if is_weekend:
        current_price += SURCHARGE_WEEKEND
        
    # 5. Минимальная стоимость
    final_price = int(max(current_price, MIN_PRICE))
    
    return final_price