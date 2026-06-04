"""Интеграционные тесты для booking_service."""
import pytest
from src.pricing import calculate_total
from src.booking_service import calculate_booking_price, ValidationError

def test_valid_booking_standard():
    """Успешный расчёт стандартного бронирования."""
    result = calculate_booking_price(100, 25, False, None)
    assert result == 100

def test_valid_with_age_discount():
    """Расчёт со скидкой по возрасту."""
    result = calculate_booking_price(100, 10, False, None)
    assert result == 80

def test_valid_weekend_surcharge():
    """Расчёт с наценкой за выходные."""
    result = calculate_booking_price(100, 30, True, "STUDENT2026")
    assert result == 185

def test_invalid_negative_price():
    """Отрицательная цена должна вызвать ошибку."""
    with pytest.raises(ValidationError) as exc_info:
        calculate_booking_price(-50, 25, False, None)
    assert "строго больше 0" in str(exc_info.value)

def test_invalid_zero_price():
    """Нулевая цена должна вызвать ошибку."""
    with pytest.raises(ValidationError) as exc_info:
        calculate_booking_price(0, 25, False, None)
    assert "строго больше 0" in str(exc_info.value)

def test_invalid_negative_age():
    """Отрицательный возраст должен вызвать ошибку."""
    with pytest.raises(ValidationError) as exc_info:
        calculate_booking_price(100, -5, False, None)
    assert "отрицательным" in str(exc_info.value)

def test_invalid_type_string_price():
    """Строка вместо цены должна вызвать ошибку."""
    with pytest.raises(ValidationError):
        calculate_booking_price("100", 25, False, None)

def test_invalid_type_string_age():
    """Строка вместо возраста должна вызвать ошибку."""
    with pytest.raises(ValidationError):
        calculate_booking_price(100, "25", False, None)

def test_min_price_integration():
    """Интеграция с минимальной ценой."""
    result = calculate_booking_price(20, 10, False, None)
    assert result == 50

def test_max_price_integration():
    """Расчёт для большой базовой цены."""
    result = calculate_booking_price(5000, 65, True, "STUDENT2026")
    assert result == 4100


#доптест
def test_minimum_price_rule():
    """
    Ребенок (age < 18), цена билета 10 руб -> скидка 20% = 8 руб.
    Но минимальная цена по правилам: 50 руб.
    Ожидание: 50 руб. | Факт (с багом): 8 руб.
    """
    result = calculate_total(base_price=10, age=10, is_weekend=False, promo_code=None)
    assert result == 50, f"Price {result} is below minimum 50 RUB!"