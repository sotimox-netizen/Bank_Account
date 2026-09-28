import pytest
from src.bank_account.account import BankAccount

@pytest.fixture
def account_with_balance():
    return BankAccount("test", 1000)

@pytest.fixture
def empty_account():
    return BankAccount("Empty", 0.0)

