"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
"""

from threading import Lock
import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass

@dataclass
class Carts:
    """
    Class that holds the information about all consumer carts
    """
    def __init__(self):
        """
        Constructor
        """
        self.consumer_list = []  # products in each consumer cart
        self.lock = Lock()  # prevents concurrent access to carts

@dataclass
class Products:
    """
    Class that holds the information about all products and producers
    """
    def __init__(self, max_product_cnt):
        """
        Constructor
        """
        self.producer_list = []  # products for each producer
        self.transactions = {}  # maps a purchase to the producer_id of the product
        self.max_product_cnt = max_product_cnt
        self.lock = Lock()  # prevents concurrent access to products


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
        self.products = Products(queue_size_per_producer)  # initialize products / producers
        self.carts = Carts()  # initialize carts
        self.lock = Lock()  # marketplace lock, used for printing

        self.handler = RotatingFileHandler(
                'marketplace.log', maxBytes=1000000, backupCount=20)  # configure handler
        logging.basicConfig(
                handlers=[self.handler],
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')  # configure logging

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        logging.info("register_producer() called")

        with self.products.lock:  # prevent multiple registrations at the same time
            producer_id = len(self.products.producer_list)  # id of the new producer
            self.products.producer_list.append([])  # initialize producer's list

        logging.info("register_producer() returned %d", producer_id)
        return producer_id  # return the id of the new producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        logging.info("publish() called with %d, %s", producer_id, product)

        # check if product can be added to the producer's list
        if len(self.products.producer_list[producer_id]) >= self.products.max_product_cnt:
            logging.info("publish() returned False")
            return False

        with self.products.lock:  # prevent multiple products to be added at the same time
            self.products.producer_list[producer_id].append(product)  # add product

        logging.info("publish() returned True")
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        logging.info("new_cart() called")

        with self.carts.lock:  # prevent multiple carts from being accessed at the same time
            cart_id = len(self.carts.consumer_list)  # next unused id of the new cart
            self.carts.consumer_list.append([])  # initialize cart

        logging.info("new_cart() returned %d", cart_id)
        return cart_id  # return the id of the added cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        logging.info("add_to_cart() called with %d, %s", cart_id, product)

        # check if cart id is valid
        if cart_id < 0 or cart_id >= len(self.carts.consumer_list):
            logging.warning("add_to_cart(): cart %d not found", cart_id)
            return False

        with self.products.lock:  # prevent concurrent access to products
            for producer_id, _ in enumerate(self.products.producer_list): # search product
                # check if product is in current producer's list
                if product not in self.products.producer_list[producer_id]:
                    continue

                # add product to cart
                self.products.producer_list[producer_id].remove(product)
                self.carts.consumer_list[cart_id].append(product)

                # register transaction
                if (cart_id, product) not in self.products.transactions:
                    self.products.transactions[(cart_id, product)] = []
                self.products.transactions[(cart_id, product)].append(producer_id)

                logging.info("add_to_cart() returned True")
                return True  # product was added succesfully

        logging.warning("add_to_cart(): %s not found", product)
        return False  # product could not be found

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        logging.info("remove_from_cart() called with %d, %s", cart_id, product)

        # check if card id is valid
        if cart_id < 0 or cart_id >= len(self.carts.consumer_list):
            logging.warning("remove_from_cart(): cart %d not found", cart_id)
            return False

        # check if the cart contains the product
        if product not in self.carts.consumer_list[cart_id]:
            logging.warning("remove_from_cart(): %s not found in cart %d", product, cart_id)
            return False

        with self.products.lock:  # prevent concurrent access to products
            producer_id = self.products.transactions[(cart_id, product)].pop()  # get transaction

            # remove product from cart
            self.carts.consumer_list[cart_id].remove(product)
            self.products.producer_list[producer_id].append(product)

            logging.info("remove_from_cart() returned True")
            return True  # product was removed succesfully

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        logging.info("place_order() called with %d", cart_id)

        # check if card id is valid
        if cart_id < 0 or cart_id >= len(self.carts.consumer_list):
            logging.warning("remove_from_cart(): cart %d not found", cart_id)
            return False

        ret_products = self.carts.consumer_list[cart_id]  # get cart products

        logging.info("place_order() returned %s", ret_products)
        return ret_products  # return products

    def __del__(self):
        """
        Destructor
        """
        self.handler.close()
        logging.shutdown()
