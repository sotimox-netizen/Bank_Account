import pytest

from src.bank_account.account import BankAccount
from src.bank_account.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    NegativeInitialBalanceError,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def account() -> BankAccount:
    """Счёт с начальным балансом 100.0 для базовых тестов."""
    return BankAccount("Test", 100.0)


@pytest.fixture
def empty_account() -> BankAccount:
    """Счёт с нулевым балансом."""
    return BankAccount("Zero", 0.0)


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------

class TestInit:
    def test_initial_balance(self, account: BankAccount) -> None:
        assert account.balance == 100.0

    def test_initial_owner(self, account: BankAccount) -> None:
        assert account.owner == "Test"

    def test_initial_transactions_empty(self, account: BankAccount) -> None:
        assert account.transactions == []

    def test_negative_initial_balance_raises(self) -> None:
        with pytest.raises(NegativeInitialBalanceError):
            BankAccount("Bad", -1)

    def test_empty_owner_raises(self) -> None:
        with pytest.raises(ValueError):
            BankAccount("", 100)

    def test_whitespace_owner_raises(self) -> None:
        with pytest.raises(ValueError):
            BankAccount("   ", 100)


# ---------------------------------------------------------------------------
# deposit
# ---------------------------------------------------------------------------

class TestDeposit:
    def test_deposit_increases_balance(self, account: BankAccount) -> None:
        account.deposit(50)
        assert account.balance == 150.0

    def test_deposit_records_transaction(self, account: BankAccount) -> None:
        account.deposit(50)
        assert account.transactions[-1] == ("DEPOSIT", 50)

    def test_deposit_zero_raises(self, account: BankAccount) -> None:
        with pytest.raises(InvalidAmountError):
            account.deposit(0)

    def test_deposit_negative_raises(self, account: BankAccount) -> None:
        with pytest.raises(InvalidAmountError):
            account.deposit(-10)

    def test_multiple_deposits(self, account: BankAccount) -> None:
        account.deposit(10)
        account.deposit(20)
        assert account.balance == 130.0
        assert len(account.transactions) == 2


# ---------------------------------------------------------------------------
# withdraw
# ---------------------------------------------------------------------------

class TestWithdraw:
    def test_withdraw_decreases_balance(self, account: BankAccount) -> None:
        account.withdraw(30)
        assert account.balance == 70.0

    def test_withdraw_records_transaction(self, account: BankAccount) -> None:
        account.withdraw(30)
        assert account.transactions[-1] == ("WITHDRAW", 30)

    def test_withdraw_exact_balance(self, account: BankAccount) -> None:
        account.withdraw(100)
        assert account.balance == 0.0

    def test_withdraw_insufficient_funds_raises(self, account: BankAccount) -> None:
        with pytest.raises(InsufficientFundsError):
            account.withdraw(9999)

    def test_withdraw_zero_raises(self, account: BankAccount) -> None:
        with pytest.raises(InvalidAmountError):
            account.withdraw(0)

    def test_withdraw_negative_raises(self, account: BankAccount) -> None:
        with pytest.raises(InvalidAmountError):
            account.withdraw(-5)

    def test_withdraw_from_empty_account_raises(self, empty_account: BankAccount) -> None:
        with pytest.raises(InsufficientFundsError):
            empty_account.withdraw(1)


# ---------------------------------------------------------------------------
# __str__ / __repr__
# ---------------------------------------------------------------------------

class TestStringRepresentation:
    def test_str_contains_owner(self, account: BankAccount) -> None:
        assert "Test" in str(account)

    def test_str_contains_balance(self, account: BankAccount) -> None:
        assert "100.00" in str(account)

    def test_repr_contains_owner(self, account: BankAccount) -> None:
        assert "owner='Test'" in repr(account)

    def test_repr_contains_balance(self, account: BankAccount) -> None:
        assert "balance=100.0" in repr(account)
