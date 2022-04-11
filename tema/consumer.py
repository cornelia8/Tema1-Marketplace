"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

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

        # carts = List [cart]
        # cart = List [product_info]
        # product_info = {"type": str, "product": type Product, "quantity": int}

        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs["name"]

    def run(self):

        for cart in self.carts:

            cart_id = self.marketplace.new_cart()

            for product_info in cart:

                op = product_info['type']
                product = product_info['product']
                quantity = product_info['quantity']

                while quantity > 0:

                    if op == "add":
                        added = self.marketplace.add_to_cart(cart_id, product)

                        if added:
                            quantity = quantity - 1
                        else:
                            time.sleep(self.retry_wait_time)

                    if op == "remove":
                        self.marketplace.remove_from_cart(cart_id, product)
                        quantity = quantity - 1

            products = self.marketplace.place_order(cart_id)
        
            # print as per the output files
            for prod in products:
                print(self.name + " bought " + str(prod))
