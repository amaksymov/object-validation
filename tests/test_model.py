from decimal import Decimal

import pytest

from object_validation import fields
from object_validation.models import Model


def test_model():
    class Product(Model):
        price = fields.Integer()

    product = Product()

    assert not hasattr(Product, 'price')
    assert hasattr(product, 'price')
