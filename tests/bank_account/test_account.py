import pytest
from src.bank_account.account import BankAccount
from src.bank_account.exceptions import (
    InvalidAmountError,
    InsufficientFundsError,
    NegativeInitialBalanceError,
)



def test_Add_Account_positive_balance(account_with_balance):
    account = account_with_balance
    assert account.balance == 1000

def test_Add_Account_zero_balance(empty_account):
    account = empty_account
    assert account.balance == 0.0

@pytest.mark.regression
@pytest.mark.parametrize("initial_balance", [-1, -0.01, -1000])
def test_init_negative_balance_raises(initial_balance):
    with pytest.raises(NegativeInitialBalanceError):
        BankAccount("test", initial_balance)

@pytest.mark.smoke
def test_Deposit_balance(account_with_balance):
    account_with_balance.deposit(100)
    assert account_with_balance.balance == 1100

@pytest.mark.regression
def test_Deposit_negative_balance(account_with_balance):
    with pytest.raises(InvalidAmountError):
        account_with_balance.deposit(-100)

@pytest.mark.smoke
def test_Withdraw_balance(account_with_balance):
    account_with_balance.withdraw(100)
    assert account_with_balance.balance == 900

@pytest.mark.regression
def test_Withdraw_balance_negative_balance(account_with_balance):
    with pytest.raises(InvalidAmountError):
        account_with_balance.withdraw(-100)

@pytest.mark.regression
def test_Withdraw_balance_zero_balance(account_with_balance):
    with pytest.raises(InvalidAmountError):
        account_with_balance.withdraw(0)

@pytest.mark.regression
def test_withdraw_insufficient_funds(account_with_balance):
    with pytest.raises(InsufficientFundsError):
        account_with_balance.withdraw(99999)

@pytest.mark.smoke
def test_deposit_withdraw_deposit(account_with_balance):
    account = account_with_balance
    account.deposit(100)
    account.withdraw(50)
    account.deposit(25)

    assert account.balance == pytest.approx(1075)

@pytest.mark.smoke
def test_account_get_holder(account_with_balance):
    assert account_with_balance.owner == "test"

def test_account_string_representation(account_with_balance):
    assert str(account_with_balance) == "Счёт [test]: 1000.00 руб."
    assert repr(account_with_balance) == "BankAccount(owner='test', balance=1000.0)"

@pytest.mark.parametrize(
    "amount, true_balance",
    [
        (100, 1100),
        (200, 1200),
        (500,1500)
    ],
)
def test_many_deposit(account_with_balance, amount, true_balance):
    account_with_balance.deposit(amount)
    assert account_with_balance.balance == true_balance

@pytest.mark.parametrize(
    "amount, true_balance",
    [
        (100, 900),
        (200, 800),
        (500, 500)
    ]
)
def test_many_withdraw(account_with_balance, amount, true_balance):
    account_with_balance.withdraw(amount)
    assert account_with_balance.balance == true_balance

@pytest.mark.parametrize(
    "amount, exception_type",
    [
        (0, InvalidAmountError),
        (-500, InvalidAmountError),
        (313131313131, InsufficientFundsError),
    ]
)
def test_many_withdraw_invalid(account_with_balance, amount, exception_type):
    with pytest.raises(exception_type):
        account_with_balance.withdraw(amount)

