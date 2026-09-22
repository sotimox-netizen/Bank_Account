import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bank_account.account import BankAccount
from src.bank_account.exceptions import InsufficientFundsError, InvalidAmountError


def print_line() -> None:
    """Печатает разделительную линию."""
    print("=" * 50)


def print_logs(accounts: dict) -> None:
    """Выводит последнюю транзакцию по каждому счёту."""
    for name, account in accounts.items():
        transactions = account.transactions
        if transactions:
            print(name, " : ", transactions[-1])
        else:
            print(name, " : нет транзакций")


def print_users(accounts: dict) -> None:
    """Выводит текущий баланс каждого счёта."""
    for name, account in accounts.items():
        print(name, " | ", account.balance)


def run_user_commands(accounts: dict) -> None:
    """Выполняет случайные операции (депозит/снятие) для каждого счёта."""
    for name, account in accounts.items():
        try:
            command_type = random.randint(1, 2)
            amount = random.randint(1, 100)
            if command_type == 1:
                account.deposit(amount)
            else:
                account.withdraw(amount)
        except (InsufficientFundsError, InvalidAmountError) as e:
            print(f"[{name}] Ошибка операции: {e}")


def main() -> None:
    time_start = time.ctime()
    print_line()
    print("СИСТЕМА СОЗДАНИЯ ТЕСТОВЫХ СЧЕТОВ")
    print(f"время запуска {time_start}")
    print_line()

    accounts = {
        "Alice": BankAccount("Alice", 100),
        "Bob": BankAccount("Bob", 500),
        "Charlie": BankAccount("Charlie", 2500),
        "Diana": BankAccount("Diana", 750),
        "Eve": BankAccount("Eve", 3000),
        "Frank": BankAccount("Frank", 100),
    }

    print_line()
    print("СВОДКА ПО СЧЕТАМ")
    print_line()
    print_users(accounts)
    print_line()

    run_user_commands(accounts)

    print_line()
    print("ХОД ОПЕРАЦИЙ")
    print_logs(accounts)
    print("СВОДКА ПО СЧЕТАМ ПОСЛЕ ОПЕРАЦИЙ")
    print_line()
    print_users(accounts)
    print_line()


if __name__ == "__main__":
    main()