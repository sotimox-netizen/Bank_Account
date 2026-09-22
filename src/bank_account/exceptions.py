class BankAccountError(Exception):
    """Базовое исключение для операций с банковским счётом."""


class NegativeInitialBalanceError(BankAccountError):
    """Вызывается при попытке создать счёт с отрицательным начальным балансом."""


class InvalidAmountError(BankAccountError):
    """Вызывается при передаче некорректной суммы (нулевой или отрицательной)."""


class InsufficientFundsError(BankAccountError):
    """Вызывается при попытке снять сумму, превышающую текущий баланс."""