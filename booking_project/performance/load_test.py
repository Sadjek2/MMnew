#тестовый файл

import threading
import time

def calculate_total(base_price, age, is_weekend, promo_code):
    price = base_price
    if age < 18 or age >= 65:
        price *= 0.80
    if promo_code == "STUDENT2026" and not (age < 18 or age >= 65):
        price *= 0.85
    if is_weekend:
        price += 100
    if price < 50:
        price = 50
    return price

times = []
errors = 0
lock = threading.Lock()

def worker():
    global errors
    start = time.perf_counter()
    try:
        for _ in range(1000):
            calculate_total(500, 30, False, None)
    except:
        errors += 1
    elapsed = (time.perf_counter() - start) * 1000
    with lock:
        times.append(elapsed)

threads = []
start_time = time.time()
while time.time() - start_time < 10:
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
    if len(threads) >= 500:
        for t in threads:
            t.join()
        threads = []

for t in threads:
    t.join()

times.sort()
total_requests = len(times) * 1000
avg = sum(times) / len(times)
p95 = times[int(len(times) * 0.95)]

print(f"Всего запросов: {total_requests}")
print(f"Среднее время: {avg:.2f} мс")
print(f"95-й перцентиль: {p95:.2f} мс")
print(f"Ошибки: {errors}")