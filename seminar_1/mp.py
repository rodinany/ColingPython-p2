import time
from multiprocessing import Process, Pool
import os


start = time.time()

def do_work(t):
    print(f'Starting work with {t}...')
    time.sleep(t)
    print('Work done!')


with Pool(10) as pool:
    pool.map(do_work, range(1, 10))


print(f'Time spent: {(time.time() - start):.2f} seconds')
