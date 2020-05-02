from object_validation.datastructures import ValidationResult


def test_validation_result():
    result = ValidationResult('value')
    assert result.value == 'value'
    assert not result.has_error()
    assert result.get_errors() is None

    errors = {'error': 'errors'}
    result = ValidationResult('value', errors)
    assert result.value == 'value'
    assert result.has_error()
    assert result.get_errors() == errors
