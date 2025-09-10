from contextlib import AbstractContextManager
from sqlalchemy.orm import sessionmaker
from repositories import *

class SqlAlchemyUnitOfWork(AbstractContextManager):
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session = None
        self.clients = None
        self.bookings = None
        self.tattoos = None
        self.payments = None
        self.expenses = None

    def __enter__(self):
        self.session = self.session_factory()
        self.clients = ClientRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.tattoos = TattooRepository(self.session)
        self.payments = PaymentRepository(self.session)
        self.expenses = ExpenseRepository(self.session)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            print("session closed")
            self.session.close()

    def commit(self):
        print("session committed")
        self.session.commit()

    def rollback(self):
        print("session rolled back")
        self.session.rollback()
