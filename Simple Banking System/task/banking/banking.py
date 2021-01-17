import random
import string
from typing import List, Optional

import db
from db import CreditCard, CardsModel, SQLiteDBHelper


class WrongCredentialsError(Exception):
    pass



class CreditCardManager:
    IIN = '400000'

    @classmethod
    def create_credit_card(cls):
        return CreditCard(number=cls._generate_card_number(),
                          pin=cls._generate_pin(),
                          balance=0)

    @staticmethod
    def _generate_pin() -> str:
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def _generate_card_number(cls) -> str:
        generated_number = cls.IIN + ''.join(random.choices(string.digits, k=9))
        return generated_number + str(cls._get_checksum(generated_number))

    @staticmethod
    def _get_checksum(code: str) -> int:
        """
        Counts checksum for card number using Lunh algorithm
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


class CardStorage:
    cards = 0

    def __init__(self, cards_model: CardsModel, card_table_name: str):
        self.cards_model = cards_model
        self.card_table_name = card_table_name

    def add_card(self, card: CreditCard):
        self.cards_model.add_card(card)

    def get_card(self, number, pin) -> Optional[CreditCard]:
        card = self.cards_model.get_card(number, pin)
        return CreditCard(card[1], card[2], card[3]) if card else None

    def get_all_cards(self) -> List[CreditCard]:
        return [CreditCard(card[1], card[2], card[3]) for card in self.cards_model.get_all_cards()]


class BankApp:

    def __init__(self, card_storage: CardStorage):
        self.card_storage = card_storage

    def create_card(self) -> CreditCard:
        card = CreditCardManager().create_credit_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)
        self.card_storage.add_card(card)
        return card

    def login(self, card_number: str, pin: str) -> CreditCard:
        card = self.card_storage.get_card(card_number, pin)
        if not card:
            print('Wrong card number or PIN!')
            raise WrongCredentialsError
        return card

    def main_menu(self):

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

                self.user_menu()

            if decision == 0:
                print('Bye!')
                exit()

    def user_menu(self):
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')

            decision = int(input())

            if decision == 0:
                print('Bye!')
                exit()

            if decision == 1:
                print(f'Balance: {card.balance}')

            if decision == 5:
                print('You have successfully logged out!')
                break



db_manager = SQLiteDBHelper("card.s3db")
cards_model = CardsModel(db_manager)

card_storage = CardStorage(cards_model, db.card_table_name)
bank_app = BankApp(card_storage)

bank_app.main_menu()
