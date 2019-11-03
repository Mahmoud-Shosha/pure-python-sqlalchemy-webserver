from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine # connection between classes and tables
Session = sessionmaker(bind=engine)
session = Session()

myFirstRestaurant = Restaurant(name='Pizza Palace')
session.add(myFirstRestaurant)
session.commit()
print(session.query(Restaurant).all())

cheezepizza = MenuItem(name='Cheeze Pizza')
session.add(cheezepizza)
session.commit()
print(session.query(MenuItem).all())
