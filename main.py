import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000
BATCH_SIZE = 10000


class BoundedStack:
    def __init__(self, size):
        self.size = size
        self.stack = []
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            if len(self.stack) < self.size:
                self.stack.append(item)
                return True
            return False

    def pop(self):
        with self.lock:
            if self.stack:
                return self.stack.pop()
            return None

    def getTop(self):
        with self.lock:
            if self.stack:
                return self.stack[-1]
            return "empty"


def number_generator(stack, all_file):
    global finished_generating
    i = 0
    nums_to_write = []
    while i < MAX_COUNT:
        num = random.randint(LOWER_NUM, UPPER_NUM)
        count = 0
        while count < 2 and i < MAX_COUNT:
            if stack.push(num):
                i += 1
                nums_to_write.append(num)
                count += 1
        if len(nums_to_write) >= BATCH_SIZE:
            random.shuffle(nums_to_write)
            with all_file:
                all_file.write('\n'.join(map(str, nums_to_write)) + '\n')
            nums_to_write = []

    if nums_to_write:
        random.shuffle(nums_to_write)
        with all_file:
            all_file.write('\n'.join(map(str, nums_to_write)) + '\n')

    finished_generating = True


def odd_thread(stack, odd_file):
    global finished_generating
    nums_to_write = []
    while True:
        if finished_generating and len(stack.stack) == 0:
            break
        num = stack.getTop()
        while (num != "empty") and (num % 2 != 0):
            num = stack.pop()
            if num is not None:
                nums_to_write.append(num)
            num = stack.getTop()

            if len(nums_to_write) >= BATCH_SIZE:
                random.shuffle(nums_to_write)
                with odd_file:
                    odd_file.write('\n'.join(map(str, nums_to_write)) + '\n')
                nums_to_write = []

    if nums_to_write:
        random.shuffle(nums_to_write)
        with odd_file:
            odd_file.write('\n'.join(map(str, nums_to_write)) + '\n')


def even_thread(stack, even_file):
    global finished_generating
    nums_to_write = []
    while True:
        if finished_generating and len(stack.stack) == 0:
            break
        num = stack.getTop()
        while (num != "empty") and (num % 2 == 0):
            num = stack.pop()
            if num is not None:
                nums_to_write.append(num)
            num = stack.getTop()

            if len(nums_to_write) >= BATCH_SIZE:
                random.shuffle(nums_to_write)
                with even_file:
                    even_file.write('\n'.join(map(str, nums_to_write)) + '\n')
                nums_to_write = []

    if nums_to_write:
        random.shuffle(nums_to_write)
        with even_file:
            even_file.write('\n'.join(map(str, nums_to_write)) + '\n')


stack = BoundedStack(BUFFER_SIZE)
finished_generating = False

with open("all.txt", 'w') as all_file, open("odd.txt", 'w') as odd_file, open("even.txt", 'w') as even_file:
    gen_thread = threading.Thread(target=number_generator, args=(stack, all_file))
    odd_thread = threading.Thread(target=odd_thread, args=(stack, odd_file))
    even_thread = threading.Thread(target=even_thread, args=(stack, even_file))

    gen_thread.start()
    odd_thread.start()
    even_thread.start()

    gen_thread.join()
    odd_thread.join()
    even_thread.join()
