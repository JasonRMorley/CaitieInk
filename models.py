from sqlalchemy import Column, Integer, String, Text, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    notes = Column(Text)

    # One client → many tattoos
    tattoos = relationship("Tattoo", back_populates="client")
    bookings = relationship("Booking", back_populates="client")
    payments = relationship("Payment", back_populates="client")


class Tattoo(Base):
    __tablename__ = "tattoo"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    price_estimate = Column(Float, nullable=True)
    price_final = Column(Float, nullable=True)
    status = Column(String)
    title = Column(String)
    note = Column(String)

    # Relationships
    client = relationship("Client", back_populates="tattoos")
    bookings = relationship("Booking", back_populates="tattoo")
    payments = relationship("Payment", back_populates="tattoo")



class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True)
    tattoo_id = Column(Integer, ForeignKey("tattoo.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    booking_type = Column(String, nullable=False)

    tattoo = relationship("Tattoo", back_populates="bookings")
    client = relationship("Client", back_populates="bookings")


class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True)
    tattoo_id = Column(Integer, ForeignKey("tattoo.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    payment_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    notes = Column(String, nullable=False)

    tattoo = relationship("Tattoo", back_populates="payments")
    client = relationship("Client", back_populates="payments")


class Expenses(Base):
    __tablename__ = "expense"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    item = Column(String, nullable=False)
    category = Column(String, nullable=False)
    notes = Column(String, nullable=False)
