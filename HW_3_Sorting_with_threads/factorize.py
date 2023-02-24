from functools import wraps
from multiprocessing import cpu_count, Pool
from time import time
import logging


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        logging.info(
            f'Function "{func.__name__}" have been working {(end - start):.04f} seconds.'
        )
        return result

    return wrapper


def factorize(*number):
    factors = []
    for num in number:
        num_factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                num_factors.append(i)
        factors.append(num_factors)
    return factors


@measure_time
def single_test_factorize():
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]


@measure_time
def process_test_factorize():
    with Pool(cpu_count()) as pool:
        a, b, c, d = pool.map(factorize, (128, 255, 99999, 10651060))
    pool.close()
    pool.join()

    assert a == [[1, 2, 4, 8, 16, 32, 64, 128]]
    assert b == [[1, 3, 5, 15, 17, 51, 85, 255]]
    assert c == [[1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]]
    assert d == [
        [
            1,
            2,
            4,
            5,
            7,
            10,
            14,
            20,
            28,
            35,
            70,
            140,
            76079,
            152158,
            304316,
            380395,
            532553,
            760790,
            1065106,
            1521580,
            2130212,
            2662765,
            5325530,
            10651060,
        ]
    ]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(processName)s - %(message)s")
    single_test_factorize()
    process_test_factorize()
