import os
import logging
from enum import IntEnum
from logging.handlers import RotatingFileHandler

from src.bank_account.exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    NegativeInitialBalanceError,
)


def _setup_logger() -> logging.Logger:
    """Настраивает и возвращает логгер для модуля."""
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.dirname(current_dir)
    project_root = os.path.dirname(src_dir)
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "bank_account.log")
    handler = RotatingFileHandler(log_file, maxBytes=1_048_576, backupCount=2)
    formatter = logging.Formatter(
        "%(asctime)s %(funcName)s %(name)s %(levelname)s %(message)s"
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    _logger.info("Log directory and file initialized")
    return _logger


logger = _setup_logger()


class TransactionType(IntEnum):
    DEPOSIT = 1
    WITHDRAW = 2


class BankAccount:
    """Банковский счёт с поддержкой депозита, снятия и истории транзакций."""

    def __init__(self, owner: str, balance: float) -> None:
        if not owner or not owner.strip():
            raise ValueError("Имя владельца не может быть пустым.")
        if balance < 0:
            raise NegativeInitialBalanceError(
                f"Начальный баланс не может быть отрицательным: {balance}"
            )
        self.owner = owner
        self._balance = float(balance)
        self._transactions: list[tuple[str, float]] = []

    def deposit(self, amount: float) -> None:
        """Пополняет счёт на указанную сумму."""
        if amount <= 0:
            raise InvalidAmountError(
                f"Сумма пополнения должна быть положительной, получено: {amount}"
            )
        self._balance += amount
        self._add_transaction(TransactionType.DEPOSIT, amount)
        logger.info("deposit successful")

    def withdraw(self, amount: float) -> None:
        """Снимает указанную сумму со счёта."""
        if amount <= 0:
            raise InvalidAmountError(
                f"Сумма снятия должна быть положительной, получено: {amount}"
            )
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Недостаточно средств: баланс {self._balance}, запрошено {amount}"
            )
        self._balance -= amount
        self._add_transaction(TransactionType.WITHDRAW, amount)
        logger.info("withdraw successful")

    @property
    def balance(self) -> float:
        """Текущий баланс счёта."""
        return self._balance

    @property
    def transactions(self) -> list[tuple[str, float]]:
        """История всех транзакций."""
        return self._transactions

    def _add_transaction(self, transaction_type: TransactionType, amount: float) -> None:
        self._transactions.append((transaction_type.name, amount))

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"

    def __str__(self) -> str:
        return f"Счёт [{self.owner}]: {self._balance:.2f} руб."
