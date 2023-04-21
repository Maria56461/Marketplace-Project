"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
"""
import unittest, uuid, tema.product
from threading import Lock, current_thread

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
        self.queue_size_per_producer, self.idproducerlock = queue_size_per_producer, Lock()
        self.idproducernoproducts, self.idproducer_products = {}, {}
        self.allcarts, self.idcartlock = {}, Lock()
        '''
        allcarts is a dict containing cartID:
        [(idproducer1, product1), (idproducer2, product2), etc]
        '''
        self.addtocartlock = Lock()
        self.removefromcartlock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.idproducerlock.acquire()
        idproducer = "Producer_" + str(uuid.uuid4())
        self.idproducernoproducts[idproducer] = 0
        self.idproducerlock.release()
        return idproducer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.queue_size_per_producer <= self.idproducernoproducts[producer_id]:
            return False

        self.idproducernoproducts[producer_id] += 1
        if producer_id in self.idproducer_products:
            self.idproducer_products[producer_id].append(product)
        else:
            self.idproducer_products[producer_id] = [product]
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.idcartlock.acquire()
        idcart = int(uuid.uuid4())
        self.allcarts[idcart] = []
        self.idcartlock.release()
        return idcart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for idproducer in self.idproducer_products:
            '''
            if the product is available on the market, it must be deleted from
            all the producers lists, then added to the given cart
            '''
            productslist = self.idproducer_products[idproducer]
            if product in productslist:
                productslist.remove(product)
                # remove is thread-safe
                self.addtocartlock.acquire()
                self.idproducernoproducts[idproducer] -= 1
                self.addtocartlock.release()
                # append is thread-safe
                self.allcarts[cart_id].append((idproducer, product))
                return True
        else:
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        productslist = self.allcarts[cart_id]
        for (idproducer, produs) in productslist:
            if produs == product:
                productslist.remove((idproducer, product))
                # remove is thread-safe
                self.removefromcartlock.acquire()
                self.idproducernoproducts[idproducer] += 1
                self.removefromcartlock.release()
                # append is thread-safe
                self.idproducer_products[idproducer].append(product)
                return True
        else:
            return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        listt = self.allcarts.pop(cart_id, None)
        for (idproducer, product) in listt:
            print("{} bought {}".format(current_thread().name, product))

        return listt

class TestMarketplace(unittest.TestCase):

    def setUp(self):
        self.marketplace = Marketplace(12)

    def test_register_producer(self):
        self.assertNotEqual(self.marketplace.register_producer(), self.marketplace.register_producer())

    def test_publish(self):
        id1 = self.marketplace.register_producer()
        product1 = product.Tea("BestTea", 12, "Black Tea")
        product2 = product.Coffee("TurkishCoffee", 23, "LOW", "Medium")
        self.assertTrue(self.marketplace.publish(id1, product1))
        self.assertTrue(self.marketplace.publish(id1, product2))
        self.assertEqual(self.marketplace.idproducer_products[id1], [product1, product2])

    def test_add_to_cart(self):
        cartid = self.marketplace.new_cart()
        producerid = self.marketplace.register_producer()
        newproduct = product.Coffee("BritishCoffee", 50, "High", "Medium")
        self.assertTrue(self.marketplace.publish(producerid, newproduct))
        self.assertTrue(self.marketplace.add_to_cart(cartid, newproduct))
        self.assertIn((producerid, newproduct), self.marketplace.allcarts[cartid])

    def test_remove_from_cart(self):
        cartid = self.marketplace.new_cart()
        producerid = self.marketplace.register_producer()
        newproduct = product.Coffee("FrenchCoffee", 35, "High", "Low")
        self.assertTrue(self.marketplace.publish(producerid, newproduct))
        self.assertTrue(self.marketplace.add_to_cart(cartid, newproduct))
        self.assertIn((producerid, newproduct), self.marketplace.allcarts[cartid])
        self.assertTrue(self.marketplace.remove_from_cart(cartid, newproduct))
        self.assertNotIn((producerid, newproduct), self.marketplace.allcarts[cartid])

    def test_place_order(self):
        cartid = self.marketplace.new_cart()
        producerid = self.marketplace.register_producer()
        newproduct = product.Coffee("FrenchCoffee", 35, "High", "Low")
        self.assertTrue(self.marketplace.publish(producerid, newproduct))
        self.assertTrue(self.marketplace.add_to_cart(cartid, newproduct))
        self.assertIn((producerid, newproduct), self.marketplace.allcarts[cartid])
        self.assertEqual([(producerid, newproduct)], self.marketplace.place_order(cartid))





