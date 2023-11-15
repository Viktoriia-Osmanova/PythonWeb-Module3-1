import multiprocessing
import time

def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(*numbers):
    with multiprocessing.Pool() as pool:
        result = pool.map(factorize_single, numbers)
    return result

# Тест
start_time = time.time()
result_parallel = factorize_parallel(12, 18, 24, 30)
end_time = time.time()

print("Parallel result:", result_parallel)
print("Parallel execution time:", end_time - start_time, "seconds")