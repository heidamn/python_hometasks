""" Лабораторная работа №?
    Реализация пула процессов
    Шоломов Даниил, k3140
    ИТМО, 2019
    """

import time
import multiprocessing as mp
import psutil
from heavyf import heavy_computation as f


class ProcessPool():
    """ Реализация пула процессов с учетом памяти, потребляемой одним процессом"""

    def __init__(self, min_workers=1, max_workers=15, max_mem_usage='1gb'):
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
        self.min_workers = min_workers
        self.max_workers = max_workers
        #  self.cpu_usage = cpu_usage
        self.workers_num = 0
        self.mem_usage = 0
        self.mem_usage_queue = mp.Queue()

    def map(self, computations, data):
        """ Рассчет количества процессов и запуск пула"""
        #  запуск тестового процесса
        p_list = []
        p = mp.Process(target=computations, name='test process', args=(data.get(),))
        p.start()
        p_m = mp.Process(target=self.mem_testing, name='test mem', args=(p.pid,))
        p_m.start()
        p.join()
        p_m.join()
        mem_usage_list = []
        print("вычисление mem_usage...")
        while not self.mem_usage_queue.empty():
            mem = self.mem_usage_queue.get()
            mem_usage_list.append(mem)
        self.mem_usage = max(mem_usage_list)
        print("вычисление mem_usage завершено", self.mem_usage)
        if self.mem_usage > self.max_mem_usage:
            raise Warning('Your max_mem_usage is not enought')
        # вычисление колва процессов
        self.workers_num = int(self.max_mem_usage // self.mem_usage)
        if self.workers_num > self.max_workers:
            self.workers_num = self.max_workers
        elif self.workers_num < self.min_workers:
            raise Warning('Your min_workers is too big')
        # запуск пула процессов
        print("запуск пула")
        for _ in range(self.workers_num):
            if not data.empty():
                print("создание нового процесса")
                p = mp.Process(target=computations, args=(data.get(),))
                p.start()
                p_list.append(p)
                print(p.pid)
            else:
                for p2 in p_list:  # ожидание завершения всех процессов
                    p2.join()
                return self.workers_num, self.mem_usage
        while True:
            for p in p_list:
                p.join(0.001)
                if not p.is_alive():  # если вдруг процесс еще жив
                    print('процесс', p.pid, 'завершил работу')
                    p.terminate()
                    if not data.empty():
                        print("создание нового процесса вместо старого")
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
        print("создание mem_usage_queue...")
        p_psutil = psutil.Process(pid)
        while psutil.pid_exists(pid):
            try:
                self.mem_usage_queue.put(p_psutil.memory_info().rss // 1000000 / 1000)
            except:
                pass
            time.sleep(0.01)
        print("создание mem_usage_queue завершено")


if __name__ == '__main__':
    queue = mp.Queue()
    for i in range(50):
        queue.put(i * 100)
    pool = ProcessPool(max_mem_usage='1gB')
    print(pool.map(f, queue))
