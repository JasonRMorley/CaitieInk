from sqlalchemy import Column, Integer, String, Text, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    notes = Column(Text)

    # One client → many tattoos
    tattoos = relationship("Tattoo", back_populates="client")


class Tattoo(Base):
    __tablename__ = "tattoo"
    tattoo_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    price_estimate = Column(Float, nullable=False)
    price_final = Column(Float, nullable=False)
    status = Column(String)

    # Relationships
    client = relationship("Client", back_populates="tattoos")
    bookings = relationship("Booking", back_populates="tattoo")
    consultation = relationship("Consultation", back_populates="tattoo", uselist=False)  # one-to-one
    design = relationship("Design", back_populates="tattoo", uselist=False)  # one-to-one
    payments = relationship("Payment", back_populates="tattoo")  # could be multiple


class Consultation(Base):
    __tablename__ = "consultation"
    consultation_id = Column(Integer, primary_key=True)
    tattoo_id = Column(Integer, ForeignKey("tattoo.tattoo_id"), nullable=False)  # FIXED
    consultation_date = Column(Date, nullable=False)
    consultation_form = Column(String, nullable=False)
    consultation_notes = Column(Text, nullable=False)

    tattoo = relationship("Tattoo", back_populates="consultation")


class Design(Base):
    __tablename__ = "design"
    design_id = Column(Integer, primary_key=True)
    tattoo_id = Column(Integer, ForeignKey("tattoo.tattoo_id"), nullable=False)  # FIXED
    design_image = Column(String, nullable=False)

    tattoo = relationship("Tattoo", back_populates="design")


class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True)
    tattoo_id = Column(Integer, ForeignKey("tattoo.tattoo_id"), nullable=False)  # FIXED
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)

    tattoo = relationship("Tattoo", back_populates="bookings")


class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True)
    tattoo_id = Column(Integer, ForeignKey("tattoo.tattoo_id"), nullable=False)  # FIXED
    payment_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    notes = Column(String, nullable=False)

    tattoo = relationship("Tattoo", back_populates="payments")


class Expenses(Base):
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    item = Column(String, nullable=False)
    category = Column(String, nullable=False)
    notes = Column(String, nullable=False)
