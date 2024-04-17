# import psycopg2
# import sqlalchemy
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# engine = create_engine("postgresql+psycopg2://ro_user_2:L6YdK57LfQ7OmegBXv@rds.lgcity.dev:8635/user-service-dev")
#
# try:
#     # Попытка подключения к базе данных и выполнения запроса
#     engine.connect()
#     # Здесь можно добавить дополнительный код для выполнения запроса или других операций
# except Exception as e:
#     print(f"Ошибка при подключении к базе данных: {e}")
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
#
#
#
# Base = sqlalchemy.orm.declarative_base()
# class User(Base):
#     __tablename__ = 'sverka'
#
#     orderId = Column(Integer, primary_key=True)
#     bitUserId = Column(Integer)
#
# Base.metadata.create_all(engine)
#
# user = session.query(User).filter_by(username='646579').first()
# if user:
#     print(f"Найден пользователь с UserId: {bitUserId}")
# else:
#     print("Заказ не найден")
