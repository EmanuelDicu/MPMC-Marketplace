"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.
lint
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

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        """
        Run method for the producer thread.
        """
        producer_id = self.marketplace.register_producer()

        while True:  # produce infinitely
            for (product, cnt_product, next_product_wait_time) in self.products:
                for _ in range(cnt_product):
                    while not self.marketplace.publish(producer_id, product):
                        sleep(self.republish_wait_time)  # wait and try again
                    sleep(next_product_wait_time)  # wait and move to the next product
