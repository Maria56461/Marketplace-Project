"""
This module represents the Producer.
Computer Systems Architecture Course, Assignment 1
"""
import time
from threading import Thread

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.wait_time, self.products = republish_wait_time, products
        self.marketplace, self.name = marketplace, marketplace.register_producer()

    def run(self):
        while 1:
            '''
            each product must be published as many times as its quantity
            if a producer has already published queue_size_per_producer elements
            that have not been bought yet, he must wait republish_wait_time until
            he can publish products again;
            after each publication, the producer must wait  the amount of time
            associated with the published product
            '''
            for product in self.products:
                index_quantity = 0
                while product[1] > index_quantity:
                    done = self.marketplace.publish(self.name, product[0])
                    if done:
                        index_quantity = index_quantity + 1
                        time.sleep(product[2])
                    else:
                        time.sleep(self.wait_time)
