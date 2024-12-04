import threading
import time
import random
from datetime import datetime

def restock(unprocessed_meat):
    """補充肉類庫存並隨機排序"""
    for meat, quantity in meat_quantity:
        unprocessed_meat.extend([meat] * quantity)

    random.shuffle(unprocessed_meat)

def processing_meat(employee_name, unprocessed_meat, lock):
    """處理肉類"""
    while True:
        # 確保當下只有一個執行緒操作資源
        with lock:
            # 無資源需處理則停止
            if not unprocessed_meat:
                break
            meat = unprocessed_meat.pop()
            print(f"{employee_name} 在 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 取得{meat}")

        time.sleep(meat_processing_time[meat])
        print(f"{employee_name} 在 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 處理完{meat}")


def working():
    unprocessed_meat = []
    restock(unprocessed_meat)
    lock = threading.Lock()
    threads = []
    for name in employees:
        # 建立多執行緒
        thread = threading.Thread(target=processing_meat, args=(name, unprocessed_meat, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
		# 等待所有執行緒完成
        thread.join()


meat_quantity = [('牛肉', 10), ('豬肉', 7), ('雞肉', 5)]
meat_processing_time = {'牛肉': 1, '豬肉': 2, '雞肉': 3}
employees = ('A', 'B', 'C', 'D', 'E')
working()
