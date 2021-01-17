from dataclasses import dataclass
from sqlite3 import connect, Cursor, Connection
from typing import Optional
from card_manager import CreditCardManager

card_table_name = 'card'


class SQLiteDBHelper:

    def __init__(self, dbname: str = "card.s3db"):
        self.dbname = dbname
        self.connection: Connection = connect(dbname)
        self.cursor: Cursor = self.connection.cursor()
        self.setup()

    def setup(self):
        # creating card table
        create_table_sql = f"""CREATE TABLE IF NOT EXISTS {card_table_name} (
                            id          integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            number      text NOT NULL,
                            pin         text NOT NULL,
                            balance     integer default 0
        );"""
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def execute_query(self, query, args=tuple()):
        self.cursor.execute(query, args)
        self.connection.commit()

    def execute_multiple(self, query):
        self.cursor.executescript(query)
        self.connection.commit()

    def delete_item(self, table_name, iid):
        query = f"DELETE FROM {table_name} WHERE id = (?)"
        args = (iid,)
        self.execute_query(query, args)

    def get_item(self, query, args=tuple()):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def get_all_items(self, query, args=tuple()):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()


@dataclass
class CreditCard:

    def __init__(self, card_id: int, number: str, pin: str, balance: int):
        self.id = card_id
        self.number = number
        self.pin = pin
        self.balance = balance


class CardsModel:

    def __init__(self, db_manager: SQLiteDBHelper):
        self.db_manager = db_manager

    def add_card(self) -> CreditCard:
        card_number, pin = CreditCardManager.generate_credit_card()
        query = f"INSERT INTO {card_table_name} (number, pin, balance) VALUES (?, ?, ?)"
        args = (card_number, pin, 0)
        res = self.db_manager.execute_query(query, args)
        return self.get_card(card_number, pin)

    def delete_card(self, card: CreditCard):
        self.db_manager.delete_item(card_table_name, card.id)

    def get_card(self, number, pin) -> Optional[CreditCard]:
        query = f"SELECT id, number, pin, balance  FROM {card_table_name} WHERE number = (?) AND pin = (?)"
        args = (number, pin)
        card = self.db_manager.get_item(query, args)
        return CreditCard(*card) if card else None

    def check_card_existence(self, number) -> bool:
        query = f"SELECT number FROM {card_table_name} WHERE number = (?)"
        args = (number,)
        return self.db_manager.get_item(query, args) is not None

    def add_income(self, card_number, amount):
        query = f"""
        UPDATE {card_table_name}
        SET balance = balance + (?)
        WHERE number = (?);
        """
        args = (amount, card_number)
        self.db_manager.execute_query(query, args)

    def send_money(self, sender_card: CreditCard, recipient_card_number: str, amount):
        query = f"""
        UPDATE {card_table_name}
        SET balance = balance - {amount}
        WHERE number = {sender_card.number} AND pin = {sender_card.pin};
        UPDATE {card_table_name}
        SET balance = balance + {amount}
        WHERE number = {recipient_card_number};
        """
        self.db_manager.execute_multiple(query)

    def get_all_cards(self):
        sql = f"SELECT * FROM {card_table_name}"
        return self.db_manager.get_all_items(sql)
