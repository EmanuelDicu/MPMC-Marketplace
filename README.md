## Multi Producer Multi Consumer (MPMC) in Python

This project implements a multi-producer multi-consumer (MPMC) system in Python. The system consists of a marketplace that allows producers to publish products and consumers to purchase them. The marketplace is implemented using a queue data structure. The producers and consumers are implemented as threads.

### `Marketplace` 

The class has the following methods:

- `__init__(self, queue_size_per_producer)`:  
    The constructor initializes the `Products` and `Carts` data structures.  
    It also creates a `Lock` instance to provide thread-safety to the class.  
    Finally, it sets up logging to a rotating file handler, with a maximum size of 1MB and up to 20 backups.

- `register_producer(self)`:  
    This method returns an ID for the producer that calls it.  
    It increments the producer count and returns the new ID.

- `publish(self, producer_id, product)`:  
    This method adds the product provided by the producer to the marketplace.  
    It returns `True` if the product was successfully added and `False` otherwise.  
    If the size of the producer queue is greater than or equal to `max_product_cnt`, the method returns `False`.

- `new_cart(self)`:  
    This method creates a new cart for the consumer.  
    It returns an integer representing the cart ID.  
    It increments the consumer count and returns the new ID.

- `add_to_cart(self, cart_id, product)`:  
    This method adds a product to the given cart.  
    It returns `True` if the product was successfully added and `False` otherwise.  
    If the product is not found in any of the producer queues, the method returns `False`.

- `remove_from_cart(self, cart_id, product)`:  
    This method removes a product from the cart.  
    It returns `True` if the product was successfully removed and `False` otherwise.  
    If the cart ID is invalid or the product is not found in the cart, the method returns `False`.
- `register_producer(self)`:  
    This method returns an ID for the producer that calls it.  
    It increments the producer count and returns the new ID.

- `publish(self, producer_id, product)`:  
    This method adds the product provided by the producer to the marketplace.  
    It returns `True` if the product was successfully added and `False` otherwise.  
    If the size of the producer queue is greater than or equal to `max_product_cnt`, the method returns `False`.

- `new_cart(self)`:  
    This method creates a new cart for the consumer.  
    It returns an integer representing the cart ID.  
    It increments the consumer count and returns the new ID.

- `add_to_cart(self, cart_id, product)`:  
    This method adds a product to the given cart.  
    It returns `True` if the product was successfully added and `False` otherwise.  
    If the product is not found in any of the producer queues, the method returns `False`.

- `remove_from_cart(self, cart_id, product)`:  
    This method removes a product from the cart.  
    It returns `True` if the product was successfully removed and `False` otherwise.  
    If the cart ID is invalid or the product is not found in the cart, the method returns `False`.

### `Producer`

The `__init__` method initializes the `Producer` class with the list of products that the producer will produce, a reference to the `Marketplace` class, and the `republish_wait_time` before republishing if the marketplace is unavailable.

The `run()` method first registers the producer with the marketplace by calling the `register_producer()` method of the marketplace and getting a `producer_id`.

The producer then enters a loop that iterates over the list of products and publishes each product to the marketplace `cnt_product` times, with a delay of `next_product_wait_time` between each publication. The `publish()` method of the marketplace is called, which returns `True` if the publication is successful and `False` otherwise. If the publication is unsuccessful, the producer waits for `republish_wait_time` before trying again.

### Consumer

The `__init__` method takes in a list of carts, a reference to the `Marketplace` class, a `retry_wait_time`, and other optional arguments that are passed to the Thread class constructor.

The `run()` method iterates over each cart in the carts list and creates a new cart in the marketplace. It then iterates over each operation in the cart and calls either `add_to_cart()` or `remove_from_cart()` method of the marketplace epending on the operation type. If the method call fails, it waits for `retry_wait_time` seconds before trying again.

After all the operations in the cart are completed, the consumer places the order by calling the `place_order()` method of the marketplace, which returns a list of products. It then prints a message for each product bought by the consumer.