"""
This module represents the unit testing for Marketplace.

Computer Systems Architecture Course
Assignment 1
"""

import unittest
from marketplace import Marketplace


class TestMarketplace(unittest.TestCase):
    """
    Class that represents the unit testing for Marketplace.
    """

    def setUp(self):
        """
        Set up the testing environment.
        """
        self.marketplace = Marketplace(5)

    def test_register_producer(self):
        """
        Test the register_producer() method.
        """
        self.assertEqual(0, self.marketplace.register_producer())

    def test_publish(self):
        """
        Test the publish() method.
        """
        producer_id = self.marketplace.register_producer()
        for i in range(5):
            self.assertTrue(self.marketplace.publish(
                producer_id, f"Product {i}"))
        for i in range(5, 10):
            self.assertFalse(self.marketplace.publish(
                producer_id, f"Product {i}"))

    def test_new_cart(self):
        """
        Test the new_cart() method.
        """
        for i in range(5):
            cart_id = self.marketplace.new_cart()
            self.assertEqual(cart_id, i)

    def test_add_to_cart(self):
        """
        Test the add_to_cart() method.
        """
        producer_id = self.marketplace.register_producer()
        for i in range(5):
            self.marketplace.publish(producer_id, f"Product {i}")

        cart_id = self.marketplace.new_cart()
        for i in range(5):
            self.assertTrue(self.marketplace.add_to_cart(
                cart_id, f"Product {i}"))

        self.assertFalse(self.marketplace.add_to_cart(
            cart_id + 1, "Product 1"))
        for i in range(5):
            self.assertFalse(self.marketplace.add_to_cart(
                cart_id, f"Product {i}"))
        for i in range(5, 10):
            self.assertFalse(self.marketplace.add_to_cart(
                cart_id, f"Product {i}"))

    def test_remove_from_cart(self):
        """
        Test the remove_from_cart() method.
        """
        producer_id = self.marketplace.register_producer()
        for i in range(5):
            self.marketplace.publish(producer_id, f"Product {i}")

        cart_id = self.marketplace.new_cart()
        for i in range(5):
            self.assertFalse(self.marketplace.remove_from_cart(
                cart_id, f"Product {i}"))
        for i in range(5):
            self.marketplace.add_to_cart(cart_id, f"Product {i}")
        for i in range(5):
            self.assertTrue(self.marketplace.remove_from_cart(
                cart_id, f"Product {i}"))

    def test_place_order(self):
        """
        Test the place_order() method.
        """
        producer_id = self.marketplace.register_producer()
        for i in range(5):
            self.marketplace.publish(producer_id, f"Product {i}")

        cart_id = self.marketplace.new_cart()
        for i in range(5):
            self.marketplace.add_to_cart(cart_id, f"Product {i}")
        self.assertEqual(self.marketplace.place_order(cart_id),
            ["Product 0", "Product 1", "Product 2", "Product 3", "Product 4"])
