"""Юнит-тесты + White-box для pricing.py."""
import pytest
from src.pricing import calculate_total, MIN_PRICE

def test_standard_case_adult_weekday():
    """Взрослый, будний день, без промокода."""
    assert calculate_total(100, 25, False, None) == 100

def test_age_discount_under_18():
    """Скидка для несовершеннолетних."""
    assert calculate_total(100, 10, False, None) == 80

def test_age_discount_senior():
    """Скидка для пенсионеров (65+)."""
    assert calculate_total(100, 65, False, None) == 80

def test_age_discount_ignores_promo():
    """Промокод игнорируется при наличии скидки по возрасту."""
    assert calculate_total(100, 10, False, "STUDENT2026") == 80

def test_promo_code_applies():
    """Промокод STUDENT2026 применяется, если нет скидки по возрасту."""
    assert calculate_total(100, 25, False, "STUDENT2026") == 85

def test_weekend_surcharge():
    """Наценка за выходные."""
    assert calculate_total(100, 25, True, None) == 200

def test_promo_and_weekend():
    """Промокод + Выходные."""
    assert calculate_total(100, 25, True, "STUDENT2026") == 185

def test_min_price_enforcement():
    """Итоговая цена не может быть меньше 50 руб."""
    result = calculate_total(20, 10, False, None)
    assert result == MIN_PRICE

def test_price_boundaries():
    """Проверка граничных значений возраста."""
    assert calculate_total(100, 17, False, None) == 80
    assert calculate_total(100, 18, False, None) == 100
    assert calculate_total(100, 64, False, None) == 100
    assert calculate_total(100, 65, False, None) == 80

def test_weekend_with_age_discount():
    """Выходные + возрастная скидка."""
    assert calculate_total(100, 10, True, None) == 180

def test_invalid_promo_code():
    """Неверный промокод игнорируется."""
    assert calculate_total(100, 25, False, "WRONG") == 100