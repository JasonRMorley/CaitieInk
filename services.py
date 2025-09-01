from models import Client


class ClientService:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    def register_client(self, first_name, last_name, phone_number, notes):
        with self.uow_factory() as uow:
            client = Client(first_name=first_name, last_name=last_name, phone_number=phone_number, notes=notes)
        uow.clients.add(client)
        print("client added")

    def get_all_clients(self):
        with self.uow_factory() as uow:
            return uow.clients.session.query(Client).all()
