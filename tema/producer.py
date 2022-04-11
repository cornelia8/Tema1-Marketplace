"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

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

        # products = List [product_info]
        # product_info = List [(product, quantity, waiting_time)]
        # product = type Product, quantity = int, waiting_time = float

        Thread.__init__(self)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):

        producer_id = self.marketplace.register_producer()

        while True:
            for (product, quantity, waiting_time) in self.products:

                while quantity > 0:

                    published = self.marketplace.publish(producer_id, product)

                    if published:
                        quantity = quantity - 1
                        time.sleep(waiting_time)
                    else:
                        time.sleep(self.republish_wait_time)
