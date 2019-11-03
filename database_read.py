from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine # connection between classes and tables
Session = sessionmaker(bind=engine)
session = Session()

items = session.query(MenuItem).all()
for item in items:
    print(item.name)
