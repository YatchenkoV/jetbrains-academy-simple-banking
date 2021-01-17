from card_manager import CreditCardManager
from db import CreditCard, CardsModel, SQLiteDBHelper


class WrongCredentialsError(Exception):
    pass


class BankApp:

    def __init__(self, cards_model: CardsModel):
        self.cards_model = cards_model

    def create_card(self) -> CreditCard:
        card = self.cards_model.add_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)
        return card

    def login(self, card_number: str, pin: str) -> CreditCard:
        card = self.cards_model.get_card(card_number, pin)
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

                self.user_menu(card)

            if decision == 0:
                print('Bye!')
                exit()

    def user_menu(self, card: CreditCard):
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
                balance = self.cards_model.get_card(card.number, card.pin).balance
                print(f'Balance: {balance}')

            if decision == 2:
                print("Enter income:")
                income = int(input())
                self.cards_model.add_income(card.number, income)
                print("Income was added!")

            if decision == 3:
                print("Transfer")
                print("Enter card number")
                card_number = input()

                if not CreditCardManager.check_card_number_validity(card_number):
                    print('Probably you made a mistake in the card number. Please try again!')
                    continue

                if not self.cards_model.check_card_existence(card_number):
                    print('Such a card does not exist.')
                    continue

                print('Enter how much money you want to transfer:')
                amount = int(input())

                if self.cards_model.get_card(card.number, card.pin).balance < amount:
                    print('Not enough money!')
                    continue

                self.cards_model.send_money(card, card_number, amount)

                print('Success!')

            if decision == 4:
                self.cards_model.delete_card(card)
                print('The account has been closed!')
                break

            if decision == 5:
                print('You have successfully logged out!')
                break

db_manager = SQLiteDBHelper("card.s3db")
cards_model = CardsModel(db_manager)
bank_app = BankApp(cards_model)

bank_app.main_menu()
