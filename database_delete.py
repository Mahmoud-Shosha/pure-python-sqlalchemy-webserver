from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine # connection between classes and tables
Session = sessionmaker(bind=engine)
session = Session()

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
session.delete(spinach())
session.commit()
print(spinach)
