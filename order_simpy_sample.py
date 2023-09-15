import random
import simpy



RANDOM_SEED =  42
NUMBER_OF_PICKER = 2
MIN_PICKING_TIME = 20
MAX_PICKING_TIME = 30
MIN_LOCATE_PRODUCT_TIME = 5   # Locate products using technology
MAX_LOCATE_PRODUCT_TIME = 10   # Locate products using technology
SIM_TIME = 60     # Simulation time in minutes
#T_INTER = 7       # Create a car every ~7 minutes


try:
    class OrderPick(object):
        
        def __init__(self, env, num_picker, product_locate_time, picking_time):
            self.env = env
            self.picker = simpy.Resource(env, num_picker)
            self.picking_time = picking_time
            self.product_locate_time = product_locate_time

        def order_locating(self,order):
            """The order is trying to locating in warehouse using technology. It takes a ``order`` processes and tries
            to locate the place where it is present."""
            yield self.env.timeout(random.randint(MIN_LOCATE_PRODUCT_TIME, MAX_LOCATE_PRODUCT_TIME))
            print("order {} has been located.".format(order))

        def picking(self, order):
            """The picking processes. It takes a ``order`` processes and tries
            to pick it."""
            yield self.env.timeout(random.randint(MIN_PICKING_TIME, MAX_PICKING_TIME))
            print("Picked order {} for put away.".format(order))
            

    def order(env, name, op):
        """The order process (each order has a ``name``) ready at the warehouse
        (``op``) and requests for picking.

        It then starts the picking process, waits for it to finish and
        leaves to put away ...

        """
        print('%s arrives at the warehouse at %.2f.' % (name, env.now))
        with op.picker.request() as request:
            yield request

            print('%s pick the order at %.2f.' % (name, env.now))
            yield env.process(op.order_locating(name))


            print('%s going for picking %.2f.' % (name, env.now))
            yield env.process(op.picking(name))

            print('%s ready to put away from warehouse at %.2f.' % (name, env.now))


    def setup(env, num_picker, product_locate_time, picking_time):
        """Create a warehouse, a number of initial orders and keep creating orders
        approx. every ``t_inter`` minutes."""
        # Create the warehouse
        order_pick = OrderPick(env, num_picker, product_locate_time, picking_time)

        # Create 4 initial orders
        for i in range(4):
            env.process(order(env, 'order %d' % i, order_pick))
        
        while True:
            #yield env.timeout(random.randint(t_inter-2, t_inter+2))
            yield env.timeout(random.randint(1,2))
            i += 1
            env.process(order(env, 'order %d' % i, order_pick))
            #i += 1

        # # Create more orders while the simulation is running
        # while True:
        #     yield env.timeout(random.randint(t_inter-2, t_inter+2))
        #     i += 1
        #     env.process(order(env, 'Car %d' % i, order_pick))



    # Setup and start the simulation
    print('Order Picking')

    random.seed(RANDOM_SEED)  # This helps reproducing the results

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, NUMBER_OF_PICKER, MAX_LOCATE_PRODUCT_TIME, MAX_PICKING_TIME
                    #   , T_INTER
                    ))

    # Execute!
    env.run(until=SIM_TIME)
except Exception as ex:
        print('error:', ex)

