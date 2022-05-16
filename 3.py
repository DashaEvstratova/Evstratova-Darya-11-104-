import random
import time
import threading

def get_data(task_id):
    print(f"processing get_data({task_id})")
    time.sleep(random.randint(1, 3))
    print(f"completed get_data({task_id})")


def write_to_file(task_id):
    print(f"processing write_to_file({task_id})")
    time.sleep(random.randint(1, 5))
    print(f"completed write_to_file({task_id})")


def write_to_console(task_id):
    print(f"processing write_to_console({task_id})")
    time.sleep(random.randint(1, 5))
    print(f"completed write_to_console({task_id})")


lock = threading.Lock()
s_get = threading.Semaphore(10)
s_file = threading.Semaphore(5)
s_console = threading.Semaphore(1)
class TaskThread(threading.Thread):
    def __init__(self, task_id: int):
        super().__init__()
        self.task_id = task_id
    def run(self):
        s_get.acquire()
        lock.acquire()
        ferst = threading.Thread(target=get_data, args=(self.task_id,))
        ferst.start()
        lock.release()
        s_get.release()
        s_file.acquire()
        second = threading.Thread(target=write_to_file, args=(self.task_id,))
        second.start()
        s_file.release()
        s_console.acquire()
        therd = threading.Thread(target=write_to_console, args=(self.task_id,))
        therd.start()
        s_console.release()

if __name__ == '__main__':
    for task in range(1, 21):
        new_thread = TaskThread(task)
        new_thread.start()
        new_thread.join()
