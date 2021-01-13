import random
import string
from typing import List


class WrongCredentialsError(Exception):
    pass


class CreditCard:
    IIN = '400000'

    def __init__(self):
        self.card_number = self._generate_card_number()
        self.pin = self._generate_pin()
        self.balance = 0

    def _generate_pin(self) -> str:
        return ''.join(random.choices(string.digits, k=4))

    def _generate_card_number(self) -> str:
        generated_number = self.IIN + ''.join(random.choices(string.digits, k=9))
        return generated_number + str(self._get_checksum(generated_number))

    def _get_checksum(self, code: str) -> int:
        """
        Counts checksum for card number
        :param code:
        :return:
        """
        total = 0

        for index, digit in enumerate(code):
            digit = int(digit)
            if (index + 1) % 2 != 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        checksum = 10 - total % 10

        return checksum if checksum != 10 else 0


class BankApp:
    accounts: List[CreditCard] = []

    def create_card(self) -> CreditCard:
        card = CreditCard()
        print('Your card has been created')
        print('Your card number:')
        print(card.card_number)
        print('Your card PIN:')
        print(card.pin)
        self.accounts.append(card)
        return card

    def login(self, card_number: str, pin: str) -> CreditCard:
        try:
            return list(filter(lambda x: x.card_number == card_number and x.pin == pin, self.accounts))[0]
        except IndexError:
            print('Wrong card number or PIN!')
            raise WrongCredentialsError


bank_app = BankApp()

while True:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')

    decision = int(input())

    if decision == 1:
        card = bank_app.create_card()

    if decision == 2:
        card_number = input('Enter your card number:')
        pin = input('Enter your PIN:')
        try:
            card = bank_app.login(card_number, pin)
        except WrongCredentialsError:
            continue
        print('You have successfully logged in!')

        while True:
            print('1. Balance')
            print('2. Log out')
            print('0. Exit')

            decision = int(input())

            if decision == 0:
                break

            if decision == 1:
                print(f'Balance: {card.balance}')

            if decision == 2:
                print('You have successfully logged out!')
                break

    if decision == 0:
        print('Bye!')
        break
