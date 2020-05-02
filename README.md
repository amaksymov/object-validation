# object-validation

[![Build Status](https://travis-ci.org/amaksymov/object-validation.svg?branch=master)](https://travis-ci.org/amaksymov/object-validation)

Object validation

## Example
```python
from object_validation import fields
from object_validation.models import Model 


class User(Model):
  age = fields.Integer()

user = User(age=21)
print(user.age)  # 21
```
Validation error:
```python
from object_validation import fields
from object_validation.models import Model 
from object_validation.exceptions import ValidationError


class User(Model):
  age = fields.Integer()

try:
  user = User(age='error')
except ValidationError as err:
  print(err.errors)  # {'age': {'value_error': 'error'}}
```
