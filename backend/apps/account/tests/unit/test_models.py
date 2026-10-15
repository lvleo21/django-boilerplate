import pytest
from django.core.exceptions import ValidationError

from apps.account.models import Account


def run_username_validators(value):
    Account._meta.get_field("username").run_validators(value)


def test_username_accepts_letters_digits_and_allowed_symbols():
    assert run_username_validators("ana.m+1@x_y-z") is None


def test_username_rejects_spaces():
    with pytest.raises(ValidationError):
        run_username_validators("ana maria")


def test_username_rejects_more_than_15_characters():
    with pytest.raises(ValidationError):
        run_username_validators("a" * 16)
