from sqlite3 import connect, Cursor, Connection

connection: Connection = connect('card.s3db', check_same_thread=False)
cursor: Cursor = connection.cursor()
card_table_name = 'card'

# creating card table
create_table_sql = f"""CREATE TABLE IF NOT EXISTS {card_table_name} (
	id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	number text NOT NULL,
	pin text NOT NULL,
	balance integer default 0
);"""

cursor.execute(create_table_sql)
