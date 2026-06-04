"""Нагрузочное тестирование с Locust."""
import random
from locust import HttpUser, task, between

class BookingUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(3)
    def standard_booking(self):
        """Стандартное бронирование."""
        payload = {
            "base_price": random.randint(100, 2000),
            "age": random.randint(18, 60),
            "is_weekend": False
        }
        self.client.post("/calculate", json=payload)

    @task(2)
    def weekend_booking(self):
        """Бронирование на выходные."""
        payload = {
            "base_price": random.randint(100, 2000),
            "age": random.randint(18, 60),
            "is_weekend": True
        }
        self.client.post("/calculate", json=payload)

    @task(1)
    def student_booking(self):
        """Бронирование со студенческим промокодом."""
        payload = {
            "base_price": random.randint(100, 2000),
            "age": random.randint(18, 25),
            "is_weekend": False,
            "promo_code": "STUDENT2026"
        }
        self.client.post("/calculate", json=payload)