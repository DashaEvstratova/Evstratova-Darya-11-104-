from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from math import log2
from queue import Queue
import time
import random

def toss():
    time.sleep(random.randint(0, 3))
    return random.randint(1, 6)

def fin(idx: int, queue):
    print(f'{idx} is tossing...')
    res = 0
    while res != 6:
        res = toss()
    print(f'{idx} got {res}')
    queue.put(idx)

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

def find_wi(pair):
    print(f'{pair[0]} and {pair[1]} are battling')
    queue = Queue()
    thred1 = Thread(target=fin, args=(pair[0], queue))
    thred2 = Thread(target=fin, args=(pair[1], queue))
    thred1.start()
    thred2.start()
    thred1.join()
    thred2.join()
    res = queue.get()
    print(f'{res} has won a battle!')
    return res


def runt():
    lsting = [i for i in range(1, 21)]
    if log2(len(lsting)) % 1 == 0:
        rounds = int(log2(len(lsting)))
    else:
        rounds = int(log2(len(lsting))) + 1
    for _ in range(rounds):
        pairs = []
        while len(lsting) != 1 and len(lsting) > 0:
            pair = (pop_random(lsting), pop_random(lsting))
            pairs.append(pair)
        with ThreadPoolExecutor(4) as thread:
            result_idx = thread.map(find_wi, pairs)
        lsting.extend(list(result_idx))
    print(f'{lsting[0]} has won a tournament!')


if __name__ == '__main__':
    runt()