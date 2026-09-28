import pytest
from src.bank_account.account import BankAccount
from tests.conftest import empty_account
from src.bank_account.exceptions import *

##from tests.conftest import *



def test_Add_Accont_positive_balance(account_with_balance):
    account = account_with_balance
    assert account.balance == 1000

def test_Add_Accont_zero_balance(empty_account):
    account = empty_account
    assert account.balance == 0.0

def test_Add_Accont_negative_balance():
    with  pytest.raises(NegativeInitialBalanceError):
        BankAccount("negative", -1)

def test_Deposit_balance(account_with_balance):
    account = account_with_balance
    account.deposit(100)
    assert account.balance == 1100

def test_Deposit_negative_balance(account_with_balance):
    account = account_with_balance
    with pytest.raises(InvalidAmountError):
        account.deposit(-100)

def test_Withdraw_balance(account_with_balance):
    account = account_with_balance
    account.withdraw(100)
    assert account.balance == 900

def test_Withdraw_balance_negative_balance(account_with_balance):
    account = account_with_balance
    with pytest.raises(InvalidAmountError):
        account.withdraw(-100)

def test_Withdraw_balance_zero_balance(account_with_balance):
    account = account_with_balance
    with pytest.raises(InvalidAmountError):
        account.withdraw(0)

def test_account_get_holder(account_with_balance):
    account = account_with_balance
    assert account.get_owner == "test"

def test_account_string_representation(account_with_balance):
    account = account_with_balance
    assert str(account) == "Счёт [test]: 1000.00 руб."

    assert repr(account) == "BankAccount(owner='test', balance=1000.0)"

