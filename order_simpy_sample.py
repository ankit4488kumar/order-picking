import random
import simpy



RANDOM_SEED =  40        
NUMBER_OF_PICKER = 2           # number of picker in the warehouse
MIN_LOCATE_PRODUCT_TIME = 5    # min time taken in locating products using technology
MAX_LOCATE_PRODUCT_TIME = 10   # max time taken in locating products using technology
MIN_RETRIVE_ORDER_TIME = 10    # min time taken in retriving the order in terms of quantity, size, volume etc.
MAX_RETRIVE_ORDER_TIME = 20    # max time taken in retriving the order in terms of quantity, size, volume etc.
MIN_PICKING_TIME = 20          # min time taken in picking
MAX_PICKING_TIME = 30          # max time taken in picking

SIM_TIME = 60                  # Simulation time in minutes
#T_INTER = 7       # Create a car every ~7 minutes


try:
    class OrderPick(object):
        
        def __init__(self, env, num_picker, product_locate_time, picking_time):
            self.env = env
            self.picker = simpy.Resource(env, num_picker)
            self.picking_time = picking_time
            self.product_locate_time = product_locate_time

        def order_locating(self, env, order):
            """The order is trying to locating in warehouse using technology. It takes a ``order`` processes and tries
            to locate the place where it is present."""
            yield self.env.timeout(random.randint(MIN_LOCATE_PRODUCT_TIME, MAX_LOCATE_PRODUCT_TIME))
            print("{0} has been located at {1}.".format(order,env.now))

        def retrive_order(self,env, order):
            """The order is trying to retrive the ``order`` according to quantity, size etc."""
            yield self.env.timeout(random.randint(MIN_RETRIVE_ORDER_TIME, MAX_RETRIVE_ORDER_TIME))
            print("order {0} has been retrived at {1}".format(order, env.now))

        def picking(self, env, order):
            """The picking processes. It takes a ``order`` processes and tries
            to pick it."""
            yield self.env.timeout(random.randint(MIN_PICKING_TIME, MAX_PICKING_TIME))
            print("Picked {0} for put away at {1}.".format(order, env.now))
            

    def order(env, name, op):
        """The order process (each order has a ``name``) ready at the warehouse
        (``op``) and requests for picking.

        It then starts the picking process, waits for it to finish and
        leaves to put away ...

        """
        if int(name.split(" ")[1]) < NUMBER_OF_PICKER:
            print('%s ready for picking by pickers at %.2f.' % (name, env.now))
        else:
            print('%s is waiting for picker at %.2f.' % (name, env.now))
        with op.picker.request() as request:
            yield request

            print('%s is going to search the location at %.2f.' % (name, env.now))
            yield env.process(op.order_locating(env, name))

            print('%s is going for order retriving at %.2f.' % (name, env.now))
            yield env.process(op.retrive_order(env, name))


            print('%s going for picking %.2f.' % (name, env.now))
            yield env.process(op.picking(env, name))

            print('%s ready to put away from warehouse at %.2f.' % (name, env.now))


    def setup(env, num_picker, product_locate_time, picking_time):
        """Create a warehouse, a number of initial orders and keep creating orders
        approx. every ``t_inter`` minutes."""

        # Create the warehouse
        order_pick = OrderPick(env, num_picker, product_locate_time, picking_time)

        # Create 4 initial orders
        for i in range(NUMBER_OF_PICKER):
            env.process(order(env, 'order %d' % i, order_pick))
        
        while True:
            #yield env.timeout(random.randint(1,2))
            yield env.timeout(5)
            #yield env.put(i)
            i += 1
            env.process(order(env, 'order %d' % i, order_pick))

        # # Create more orders while the simulation is running
        # while True:
        #     yield env.timeout(random.randint(t_inter-2, t_inter+2))
        #     i += 1
        #     env.process(order(env, 'Car %d' % i, order_pick))



    # Setup and start the simulation
    print('Order Picking of Geodis Warehouse started....')

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

