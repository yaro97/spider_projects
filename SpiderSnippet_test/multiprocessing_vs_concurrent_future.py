#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yaro

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def pool_main(primes, nprocs):
    # Let the executor divide the work among processes by using 'map'.
    with ProcessPoolExecutor(max_workers=nprocs) as executor:
        return {num: factors for num, factors in
                zip(primes,
                    executor.map(is_prime, primes))}


def mp_main(primes, nprocs):
    with mp.Pool(nprocs) as pool:
        return {num: factors for num, factors in
                zip(primes,
                    pool.map(is_prime, primes))}