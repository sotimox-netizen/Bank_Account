import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bank_account.account import BankAccount
from src.bank_account.exceptions import InsufficientFundsError, InvalidAmountError


def get_numeric_input() -> int:
    while True:
        try:
            return int(input())
        except ValueError:
            print("Вводу подходят только цифры!")


def main() -> None:
    user = BankAccount("Потешкин", 500)
    while True:
        print("\nВыбор операции:\n1 - пополнить\n2 - снять\n3 - вывод логов\n0 - выход")
        x = get_numeric_input()

        if x == 1:
            print("Сколько внести?")
            try:
                user.deposit(get_numeric_input())
                print(f"Баланс: {user.balance}")
            except InvalidAmountError as e:
                print(f"Ошибка: {e}")

        elif x == 2:
            print("Сколько снять?")
            try:
                user.withdraw(get_numeric_input())
                print(f"Баланс: {user.balance}")
            except (InsufficientFundsError, InvalidAmountError) as e:
                print(f"Ошибка: {e}")

        elif x == 3:
            print("История транзакций:")
            for t in user.transactions:
                print(t)

        elif x == 0:
            print("До свидания!")
            break


if __name__ == "__main__":
    main()