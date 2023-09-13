import random
import simpy


#REQUIRED TAKS WITH TIME TAKEN
ORDER_PROCESSING_TIME = 15
LOCATE_PRODUCT_TIME = 2   # Locate products using technology
RETRIEVE_ORDERS_TIME = 5  # Retrieve orders according to quantity, size etc. ensuring accuracy
BUILD_PALLETS_TIME = 5 # Build pallets with orders and position them to loading docks
WRAP_ORDERS_TIME = 10


#OPTIONAL TASKS
'''
1. Re-stock inventory manually or with warehouse equipment
2. Keep records of completed orders
3. Maintain equipment and report on malfunctions
'''


START_HOURS = 0
SHIFT_HOURS = 8


def pick(env, queue, ident):
    while True:
        try:
            order = yield queue.get()
        except simpy.Interrupt:
            break
        else:
            print(f'{env.now} {ident} begin order')

        start_time = env.now
        try:
            yield env.timeout(ORDER_PROCESSING_TIME)
        except simpy.Interrupt:
            yield env.timeout(ORDER_PROCESSING_TIME - (env.now - start_time))
        print(f'{env.now} {ident} finish order')


def picker(env, queue, ident, start_hour, shift_hours):
    yield env.timeout(start_hour * 60)
    print(f'{env.now} {ident} start shift')
    pick_process = env.process(pick(env, queue, ident))
    yield env.timeout(shift_hours * 60)
    pick_process.interrupt()
    print(f'{env.now} {ident} end shift')


def order_generator(env, queue):
    for n in range(50):
        yield env.timeout(random.randint(1, 20))
        yield queue.put(n)
        print(f'{env.now} put order')


if __name__ == '__main__':
    env = simpy.Environment()
    queue = simpy.Store(env)
    env.process(picker(env, queue, ident=0, start_hour=0, shift_hours=12))
    env.process(picker(env, queue, ident=1, start_hour=0, shift_hours=12))
    env.process(picker(env, queue, ident=2, start_hour=0, shift_hours=4))
    env.process(picker(env, queue, ident=3, start_hour=0, shift_hours=4))
    env.process(order_generator(env, queue))
    env.run(12 * 60)
