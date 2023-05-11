import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from models import delete_table, create_table, Publisher, Book, Shop, Stock, Sale


with open("postgres_info", "r") as file_object:
    login = file_object.readline().strip()
    password_postgres = file_object.readline().strip()
    name_db = file_object.readline().strip()

DSN = f"postgresql://{login}:{password_postgres}@localhost:5432/{name_db}"
engine = sqlalchemy.create_engine(DSN)

delete_table(engine=engine)
create_table(engine=engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

for name_shop in session.query(Shop).join(Stock).join(Book).join(Publisher).\
        filter(Publisher.id == input("Введите id издателя: ")).all():
    print(name_shop)

session.close()