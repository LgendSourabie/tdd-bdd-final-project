# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    def test_read_a_product(self):
        """Product should be read"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        get_product = Product.find(product.id)
        self.assertEqual(product.name, get_product.name)
        self.assertEqual(product.description, get_product.description)
        self.assertEqual(product.price, get_product.price)
        self.assertEqual(product.available, get_product.available)
        self.assertEqual(product.category, get_product.category)

    def update_a_product(self):
        """Produt should be updated"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "new product description"
        old_id = product.id
        product.update()
        self.assertEqual(old_id, product.id)
        self.assertEqual(product.description,"new product description" )
        all_products = Product.all()
        self.assertEqual(len(all_products),1)
        self.assertEqual(all_products[0].id, old_id)
        self.assertEqual(all_products[0].description, "new product description" )

    def delete_a_product(self):
        """Produt should be deleted"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()),1)
        product.delete()
        self.assertEqual(len(Product.all()),0)

    def test_list_all_products(self):
        """All products should be listed"""
        products = Product.all()
        self.assertEqual(len(products),0)
        for _ in range(5):
            product = ProductFactory()
            product.create()
        products = Product.all()
        self.assertEqual(len(products),5)


    def test_find_a_product_by_name(self):
        """Product should be found by name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        first_product_name = products[0].name
        count = len([product for product in products if product.name == first_product_name])
        get_product_by_name = Product.find_by_name(first_product_name)
        self.assertEqual(get_product_by_name.count(), count)
        for product in get_product_by_name:
            self.assertEqual(product.name, first_product_name)
       
    def test_find_a_product_by_availability(self):
        """Product should be found by availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        first_product_available = products[0].available
        count = len([product for product in products if product.available == first_product_available])
        get_product_by_availability = Product.find_by_availability(first_product_available)
        self.assertEqual(get_product_by_availability.count(), count)
        for product in get_product_by_availability:
            self.assertEqual(product.available, first_product_available)
       
    def test_find_a_product_by_category(self):
        """Product should be found by category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        first_product_category = products[0].category
        count = len([product for product in products if product.category == first_product_category])
        get_product_by_category = Product.find_by_category(first_product_category)
        self.assertEqual(get_product_by_category.count(), count)
        for product in get_product_by_category:
            self.assertEqual(product.category, first_product_category)
       
