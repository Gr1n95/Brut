import itertools
import string
import time
from multiprocessing import Pool, cpu_count

def brute_force_sequential(target_password, max_length, charset=None):
    if charset is None:
        charset = string.printable.strip()
    target_tuple = tuple(target_password)
    charset = list(charset)
    attempts = 0
    start_time = time.time()
    
    for length in range(1, max_length + 1):
        for candidate in itertools.product(charset, repeat=length):
            attempts += 1
            if candidate == target_tuple:
                return {
                    'password': target_password,
                    'attempts': attempts,
                    'time_elapsed': time.time() - start_time
                }
    return None

def worker(args):
    target_tuple, length, charset = args
    attempts = 0
    for candidate in itertools.product(charset, repeat=length):
        attempts += 1
        if candidate == target_tuple:
            return {'password': ''.join(target_tuple), 'attempts': attempts, 'time_elapsed': None}
    return None

def brute_force_parallel(target_password, max_length, charset=None):
    if charset is None:
        charset = string.printable.strip()
    target_tuple = tuple(target_password)
    charset = list(charset)
    start_time = time.time()
    
    with Pool(processes=cpu_count()) as pool:
        tasks = [(target_tuple, length, charset) for length in range(1, max_length + 1)]
        results = pool.map(worker, tasks)
    
    for res in results:
        if res is not None:
            res['time_elapsed'] = time.time() - start_time
            return res
    return None

if __name__ == "__main__":
    target = input("Введите пароль для брутфорса: ")
    max_len = int(input("Максимальная длина пароля: "))
    
    use_parallel = input("Использовать параллельный режим? (y/n): ").lower() == 'y'
    use_custom_charset = input("Использовать кастомный набор символов? (y/n): ").lower() == 'y'
    
    if use_custom_charset:
        custom_set = input("Введите символы для перебора: ")
        charset = list(custom_set)
    else:
        # Автоматически сужаем набор до символов пароля (если не кастомный)
        charset = list(set(target)) if target else string.printable.strip()
        print(f"Автоматически выбран набор: {''.join(charset)}")
    
    print("\nНачало брутфорса...")
    if use_parallel:
        result = brute_force_parallel(target, max_len, charset)
    else:
        result = brute_force_sequential(target, max_len, charset)
    
    if result:
        print(f"\nПароль взломан: {result['password']}")
        print(f"Попыток: {result['attempts']}")
        print(f"Затраченное время: {result['time_elapsed']:.2f} секунд")
    else:
        print("\nПароль не найден в заданном диапазоне")