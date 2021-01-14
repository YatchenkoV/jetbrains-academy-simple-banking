import random
import string
from dataclasses import dataclass
from sqlite3 import Connection, Cursor
from typing import List, Optional

import db


class WrongCredentialsError(Exception):
    pass


@dataclass
class CreditCard:

    def __init__(self, number, pin, balance):
        self.number = number
        self.pin = pin
        self.balance = balance


class CreditCardGenerator:
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


class CardStorage:
    cards = 0

    def __init__(self, db_connection: Connection, card_table_name: str):
        self.db_connection: Connection = db_connection
        self.card_table_name = card_table_name

    def add_card(self, card: CreditCard):
        self.cards += 1
        sql = f"""INSERT INTO {self.card_table_name} (number, pin, balance)
         VALUES ({card.number}, {card.pin}, {card.balance})"""

        cursor: Cursor = self.db_connection.cursor()
        cursor.execute(sql)
        cursor.close()
        self.db_connection.commit()


    def get_card(self, number, pin) -> Optional[CreditCard]:
        sql = f"""
        SELECT *
        FROM {self.card_table_name}
        WHERE {self.card_table_name}.number = {number}
        AND {self.card_table_name}.pin = {pin}"""
        cursor: Cursor = self.db_connection.cursor()
        cursor.execute(sql)
        card = cursor.fetchone()
        cursor.close()
        return CreditCard(card[1], card[2], card[3]) if card else None



    def get_all_cards(self) -> List[CreditCard]:
        sql = f"SELECT * FROM {self.card_table_name}"
        cursor: Cursor = self.db_connection.cursor()
        cursor.execute(sql)
        return [CreditCard(card[1], card[2], card[3]) for card in cursor.fetchone()]


class BankApp:
    accounts: List[CreditCard] = []

    def __init__(self, card_storage: CardStorage):
        self.card_storage = card_storage

    def create_card(self) -> CreditCard:
        card = CreditCardGenerator().create_credit_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)
        self.card_storage.add_card(card)
        # self.accounts.append(card)
        return card

    def login(self, card_number: str, pin: str) -> CreditCard:
        card = self.card_storage.get_card(card_number, pin)
        if not card:
            print('Wrong card number or PIN!')
            raise WrongCredentialsError
        return card


card_storage = CardStorage(db.connection, db.card_table_name)
bank_app = BankApp(card_storage)

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
