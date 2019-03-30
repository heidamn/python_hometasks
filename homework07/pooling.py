""" Лабораторная работа №?
    Реализация пула процессов
    Шоломов Даниил, k3140
    ИТМО, 2019
    """

import time
import threading as th
import multiprocessing as mp
import psutil
from heavyf import heavy_computation as f


class ProcessPool:
    """ Реализация пула процессов с учетом памяти, потребляемой одним процессом"""

    def __init__(self, min_workers=1, max_workers=15, max_mem_usage='1gb'):
        self.max_mem_comp(max_mem_usage)
        self.min_workers = min_workers
        self.max_workers = max_workers
        #  self.cpu_usage = cpu_usage
        self.workers_num = 0
        self.mem_usage = 0
        self.mem_usage_list = []
        if self.min_workers > self.max_workers:
            raise Warning('Your max < min')

    def max_mem_comp(self, max_mem_usage):
        max_mem_usage = max_mem_usage.lower()
        if max_mem_usage.endswith('gb'):
            self.max_mem_usage = int(max_mem_usage[:-2])
        elif max_mem_usage.endswith('mb'):
            self.max_mem_usage = int(max_mem_usage[:-2]) / 1000
        elif max_mem_usage.endswith('kb'):
            self.max_mem_usage = int(max_mem_usage[:-2]) // 1000 / 1000
        elif not max_mem_usage.isdigit():
            self.max_mem_usage = int(max_mem_usage[:-1]) // 1000000 / 1000
        else:
            self.max_mem_usage = int(max_mem_usage)

    def map(self, computations, data):
        """ Рассчет количества процессов и запуск пула"""
        #  запуск тестового процесса
        p_list = []
        p = mp.Process(target=computations, name='test process', args=(data.get(),))
        p.start()
        p_m = th.Thread(target=self.mem_testing, name='test mem', args=(p.pid,))
        p_m.start()
        p.join()
        p_m.join()
        self.mem_usage = max(self.mem_usage_list)
        if self.mem_usage > self.max_mem_usage:
            raise Warning('Your max_mem_usage is not enought')
        # вычисление колва процессов
        self.workers_num = int(self.max_mem_usage // self.mem_usage)
        if not self.workers_num:
            self.workers_num = 0.0001
        if self.workers_num > self.max_workers:
            self.workers_num = self.max_workers
        elif self.workers_num < self.min_workers:
            raise Warning('Your min_workers is too big')
        # запуск пула процессов
        for _ in range(self.workers_num):
            if not data.empty():
                p = mp.Process(target=computations, args=(data.get(),))
                p.start()
                p_list.append(p)
            else:
                for p2 in p_list:  # ожидание завершения всех процессов
                    p2.join()
                return self.workers_num, self.mem_usage
        while True:
            for p in p_list:
                p.join(0.001)
                if not p.is_alive():  # если вдруг процесс еще жив
                    p.terminate()
                    if not data.empty():
                        p_list.remove(p)
                        p2 = mp.Process(target=computations, args=(data.get(),))
                        p2.start()
                        p_list.append(p2)
                    else:
                        for p2 in p_list:  # ожидание завершения всех процессов
                            p2.join()
                        return self.workers_num, self.mem_usage

    def mem_testing(self, pid):
        """ Рассчет требуемой памяти"""
        p_psutil = psutil.Process(pid)
        while psutil.pid_exists(pid):
            try:
                # SWAP
                self.mem_usage_list.append(p_psutil.memory_info().rss // 1000000 / 1000)
            except:
                pass
            time.sleep(0.01)



if __name__ == '__main__':
    queue = mp.Queue()
    for i in range(20):
        queue.put(i * 100)
    pool = ProcessPool(max_mem_usage='2gB')
    print(pool.map(f, queue))
