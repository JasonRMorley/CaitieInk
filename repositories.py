from sqlalchemy.orm import Session
from models import Client


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, client: Client):
        self.session.add(client)

    def get_by_id(self, client_id: int) -> Client | None:
        return self.session.get(Client, client_id)

    def get_all_client_names(self):
        return self.session.query(Client).all()
