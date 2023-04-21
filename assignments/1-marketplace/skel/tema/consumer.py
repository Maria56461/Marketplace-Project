"""
This module represents the Consumer.
Computer Systems Architecture Course
Assignment 1
"""
import time
from threading import Thread

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts, self.marketplace, self.retry_wait_time = carts, marketplace, retry_wait_time

    def run(self):

        for i in range(len(self.carts)):
            # each cart must be have a unique id
            idcurrentcart = self.marketplace.new_cart()
            for j in range(len(self.carts[i])):
                k = 0
                while k < ((self.carts[i])[j])["quantity"]:
                    if (((self.carts[i])[j])["type"] == "add" and
                            self.marketplace.add_to_cart(idcurrentcart,
                                                     ((self.carts[i])[j])["product"])) or \
                            (((self.carts[i])[j])["type"] == "remove" and
                             self.marketplace.remove_from_cart(idcurrentcart,
                                                               ((self.carts[i])[j])["product"])):
                        k += 1
                    else:
                        time.sleep(self.retry_wait_time)
            self.marketplace.place_order(idcurrentcart)
