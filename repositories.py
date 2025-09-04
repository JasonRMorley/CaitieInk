from sqlalchemy.orm import Session, selectinload, joinedload, Load
from models import Client, Booking
from sqlalchemy import select
from typing import Sequence


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, client: Client):
        self.session.add(client)

    def get_by_id(self, client_id: int, *, options: Sequence[Load] = ()) -> Client | None:
        if options:
            stmt = select(Client).options(*options).where(Client.id == client_id)
            return self.session.execute(stmt).scalar_one_or_none()
        return self.session.get(Client, client_id)

    def get_all_clients(self):
        return self.session.query(Client).all()



class BookingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_bookings(self):
        return self.session.query(Booking).all()



class TattooRepository:
    def __init__(self, session: Session):
        self.session = session