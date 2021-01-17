from dataclasses import dataclass
from sqlite3 import connect, Cursor, Connection

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

    def add_item(self, query, args):
        self.cursor.execute(query, args)
        self.connection.commit()

    def delete_item(self, table_name, iid):
        stmt = f"DELETE FROM {table_name} WHERE id = (?)"
        args = (iid,)
        self.cursor.execute(stmt, args)
        self.connection.commit()

    def get_item(self, query, args=tuple()):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def get_all_items(self, query, args=tuple()):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()


@dataclass
class CreditCard:

    def __init__(self, number, pin, balance):
        self.number = number
        self.pin = pin
        self.balance = balance


class CardsModel:

    def __init__(self, db_manager: SQLiteDBHelper):
        self.db_manager = db_manager

    def add_card(self, card: CreditCard):
        query = f"INSERT INTO {card_table_name} (number, pin, balance) VALUES (?, ?, ?)"
        args = (card.number, card.pin, card.balance)
        self.db_manager.add_item(query, args)

    def delete_card(self, iid):
        self.db_manager.delete_item(card_table_name, iid)

    def get_card(self, number, pin):
        query = f"SELECT {number}, {pin} FROM card WHERE number = (?) AND pin = (?)"
        args = (number, pin)
        card = self.db_manager.get_item(query, args)
        return card

    def get_all_cards(self):
        sql = f"SELECT * FROM {card_table_name}"
        return self.db_manager.get_all_items(sql)
