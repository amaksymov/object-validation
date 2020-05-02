from decimal import Decimal

import pytest

from object_validation import fields
from object_validation.models import Model


def test_integer_field():
    class Product(Model):
        price = fields.Integer(default=100)

    product = Product()
    assert product.price == 100

    product = Product(price=150)
    assert product.price == 150

    product = Product(price=Decimal('100'))
    assert product.price == 100


def test_reference_field():
    class Price(Model):
        amount = fields.Integer(default=100)

    class Item(Model):
        price = fields.Reference(Price)

    class Box(Model):
        item = fields.Reference(Item)

    box = Box(**{'item': {'price': {}}})

    assert type(box.item) == Item
    assert type(box.item.price) == Price
    assert box.item.price.amount == 100
