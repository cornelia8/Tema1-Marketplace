"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import random
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        self.queue_size_per_producer = queue_size_per_producer
        self.prod_seed = 0
        self.cart_seed = 0

        # producers = List [producer_id]
        # producer_id = str
        self.producers = []

        # items_by_producers = Dict { "producer_id" : [products] }
        # items_by_producers[producer_index] = products = List [product]
        # product = type Product
        self.items_by_producers = {}

        # carts = List [product, item_index, producer_index]
        self.carts = []

        # sync elements
        self.p_seed = Lock()
        self.c_seed = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # create an 5 digit id for the new producer and update the seed
        # this sections needs a lock to protect the seed

        self.p_seed.acquire()

        random.seed(self.prod_seed)
        producer_id = random.randint(10000, 99999)
        self.prod_seed = self.prod_seed + 1

        self.p_seed.release()

        # create empty lists of products and add it to the dictionary

        products = []
        self.items_by_producers[str(producer_id)] = products
        self.producers.append(str(producer_id)) # will be used as keys for the dictionary

        return str(producer_id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        products = self.items_by_producers[producer_id]

        # a producer has a single thread, thus we don't need a lock here
        if len(self.items_by_producers[producer_id]) >= self.queue_size_per_producer:
            return False

        products.append(product)

        self.items_by_producers[producer_id] = products

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        self.c_seed.acquire()

        cart_id = self.cart_seed
        self.cart_seed = self.cart_seed + 1

        self.c_seed.release()

        new_cart = []
        self.carts.append(new_cart)

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        for producer_id in self.producers:
            for item in self.items_by_producers[producer_id]:
                if item == product:

                    # we will remove the product from the normal list, but not from the absolute one
                    self.items_by_producers[producer_id].remove(item)

                    self.carts[cart_id].append([product, producer_id])
                    # self.lock.release()
                    return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # I think this is thread safe
        found = False
        for prod in self.carts[cart_id]:
            if prod[0] == product:

                # mark as found and extract the information about the product
                found = True
                put_back = prod[0]
                producer_id = prod[1]

                # remove from cart
                self.carts[cart_id].remove(prod)

                # put back the item in the list at the same index
                self.items_by_producers[producer_id].append(put_back)

                break

        if not found:
            return False # something must be wrong, the product is not in the cart
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        list_of_products = []

        # checkout - should be thread safe
        for prod in self.carts[cart_id]:

            # update the list of products
            list_of_products.append(prod[0])

        return list_of_products
