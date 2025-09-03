from models import *
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from dtos import *
from typing import Optional

class ClientService:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    def register_client(self, first_name, last_name, phone_number, notes):
        with self.uow_factory() as uow:
            client = Client(first_name=first_name, last_name=last_name, phone_number=phone_number, notes=notes)
        uow.clients.add(client)
        print("client added")

    def retrieve_all_clients(self):
        with self.uow_factory() as uow:
            return uow.clients.get_all_clients()

    def retrieve_client_profile(self, client_id: int) -> ClientDetailVM | None:
        with self.uow_factory() as uow:
            stmt = (
                select(Client)
                .options(
                    selectinload(Client.tattoos)  # collection
                    .joinedload(Tattoo.consultation),  # 1-1
                    selectinload(Client.tattoos)
                    .joinedload(Tattoo.design),  # 1-1
                    selectinload(Client.tattoos)
                    .selectinload(Tattoo.bookings),  # 1-many
                    selectinload(Client.tattoos)
                    .selectinload(Tattoo.payments),  # 1-many
                )
                .where(Client.client_id == client_id)
            )
            client = uow.clients.session.execute(stmt).scalar_one_or_none()
            if client is None:
                return None

            # map ORM -> VM while session is open
            v = ClientDetailVM(
                id=client.client_id,
                first_name=client.first_name,
                last_name=client.last_name,
                phone=client.phone_number,
                notes=client.notes,
                tattoos=[
                    TattooVM(
                        id=t.tattoo_id,
                        title=t.title,
                        note=t.note,
                        status=t.status,
                        price_estimate=t.price_estimate,
                        price_final=t.price_final,
                        consultation=(
                            ConsultationVM(
                                id=t.consultation.consultation_id,
                                path=t.consultation.consultation_form,
                                notes=t.consultation.notes
                            )
                            if t.consultation else None
                        ),
                        design=(
                            DesignVM(id=t.design.design_id,
                                     path=t.design.design_image,
                                     notes=t.design.notes
                                     )
                            if t.design else None
                        ),
                        bookings=[
                            BookingVM(id=b.booking_id, date=b.date, start_time=b.start_time,
                                      end_time=getattr(b, "end_time", None))
                            for b in t.bookings
                        ],
                        payments=[
                            PaymentVM(id=p.payment_id, amount=p.amount, method=getattr(p, "method", None))
                            for p in t.payments
                        ],
                    )
                    for t in client.tattoos
                ],
            )
            return v

    def register_tattoo(self, client_id, title, note):
        with self.uow_factory() as uow:
            default_status = "Consultation"
            tat = Tattoo(client_id=client_id, status=default_status, title=title, note=note)
            client = uow.clients.get_by_id(client_id)
            return client.tattoos.append(tat)

    def edit_tattoo(
            self,
            client_id: int,
            tattoo_id: int,
            *,
            title: Optional[str] = None,
            note: Optional[str] = None,
            estimate: Optional[int] = None,
            price: Optional[int] = None,
            status: Optional[str] = None,
    ) -> bool:
        """Return True if updated, False if tattoo not found."""
        with self.uow_factory() as uow:
            tattoo = uow.clients.session.get(Tattoo, tattoo_id)

            if tattoo is None:
                return False

            if tattoo.client_id != client_id:
                raise ValueError("Tattoo does not belong to this client")

            if title is not None and title != "":
                tattoo.title = title
            if note is not None and note != "":
                tattoo.note = note
            if estimate is not None:
                tattoo.price_estimate = int(estimate)
            if price is not None:
                tattoo.price_final = int(price)
            if status is not None and status != "":
                tattoo.status = status

            return True

    def delete_tattoo(self, tattoo_id):
        with self.uow_factory() as uow:
            tattoo = uow.clients.session.get(Tattoo, tattoo_id)
            delete(tattoo)

