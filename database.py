from sqlalchemy import create_engine, select, text, and_
from sqlalchemy.orm import sessionmaker
from models import Client, Tattoo


# PostgreSQL 17

# Replace with your actual database details
DATABASE_URL = "postgresql+psycopg2://postgres:Jits123@localhost:5432/CaitlinsDB"

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)


Session = sessionmaker(bind=engine)

session = Session()

def get_all_clients():
    clients = session.query(Client).all()
    client_list = []
    for client in clients:
        first_name = client.first_name
        last_name = client.last_name
        full_name = first_name + " " + last_name
        print(full_name)
        client_list.append(full_name)
    return client_list

def add_client(client):
    session.add(client)
    session.commit()

def get_client_details(client_id):
    """ Gets the first instance of client based on first and second name.
    Awaiting improvement to avoid scenarios where there are clients sharing the same name"""

    client = session.query(Client).where()
    details = {"name": f"{client.first().first_name} {client.first().last_name}",
               "phone": client.first().phone_number,
               "notes": client.first().notes}

    return details

def get_tattoos(client_name):
    first_name = client_name.split(" ")[0]
    last_name = client_name.split(" ")[1]

    tattoos = session.query(Tattoo).where(
        and_(Client.first_name == first_name, Client.last_name == last_name)
    )


