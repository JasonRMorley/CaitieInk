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
                    selectinload(Client.tattoos),
                    selectinload(Client.tattoos)
                    .selectinload(Tattoo.bookings),
                    selectinload(Client.tattoos)
                    .selectinload(Tattoo.payments),
                )
                .where(Client.id == client_id)
            )
            client = uow.clients.session.execute(stmt).scalar_one_or_none()
            if client is None:
                return None

            # map ORM -> VM while session is open
            v = ClientDetailVM(
                id=client.id,
                first_name=client.first_name,
                last_name=client.last_name,
                phone=client.phone_number,
                notes=client.notes,
                tattoos=[
                    TattooVM(
                        id=t.id,
                        title=t.title,
                        note=t.note,
                        status=t.status,
                        price_estimate=t.price_estimate,
                        price_final=t.price_final,
                        bookings=[
                            BookingVM(id=b.id, date=b.date, start_time=b.start_time, end_time=b.end_time,
                                      booking_type=b.booking_type, client_id=b.client, tattoo_id=b.tattoo_id
                                      )
                            for b in t.bookings
                        ],
                        payments=[
                            PaymentVM(id=p.id, amount=p.amount, method=getattr(p, "method", None))
                            for p in t.payments
                        ],
                    )
                    for t in client.tattoos
                ],
                bookings=[
                    BookingVM(id=b.id, date=b.date, start_time=b.start_time,
                              end_time=b.end_time, booking_type=b.booking_type,
                              client_id=b.client, tattoo_id=b.tattoo_id
                              )
                    for b in client.bookings
                ],
                payments=[
                    PaymentVM(id=p.id, amount=p.amount, method=p.method
                              )
                    for p in client.payments
                ]
            )
            return v


class TattooService:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

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

            if tattoo.id != client_id:
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


class BookingService:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    def register_booking(self, client_id, tattoo_id, booking_date, start_time, end_time, booking_type, state):
        with self.uow_factory() as uow:
            tattoo = uow.clients.session.get(Tattoo, tattoo_id)
            booking = Booking(client_id=client_id, tattoo_id=tattoo_id, date=booking_date,
                              start_time=start_time, end_time=end_time, booking_type=booking_type, state=state)
            tattoo.bookings.append(booking)
            print(f"booking sent to db {tattoo.id}")

    def retrieve_bookings_for_table(self, state):
        with self.uow_factory() as uow:
            bookings = uow.bookings.get_all_bookings()
            if bookings is None:
                return None
            vm = []

            for b in bookings:
                if b.state == state:
                    client = uow.clients.get_by_id(b.client.id)
                    client_name = f"{str(client.first_name)} {str(client.last_name)}"
                    tattoo_id, tattoo_name = b.tattoo_id, uow.tattoos.get_by_id(b.tattoo_id).title

                    vm.append(TableBookingVM(id=b.id, date=b.date, start_time=b.start_time,
                                             end_time=b.end_time, booking_type=b.booking_type,
                                             client=ClientMiniVM(id=b.client, name=client_name),
                                             client_id=b.client, tattoo_id=b.tattoo_id,
                                             tattoo=TattooMiniVM(id=tattoo_id, title=tattoo_name)
                                             ))

            return vm

    def retrieve_booking_vm_by_id(self, booking_id):
        with self.uow_factory() as uow:
            b = uow.bookings.get_booking_by_id(booking_id=booking_id)
            booking = BookingVM(id=b.id, tattoo_id=b.tattoo_id, client_id=b.client_id, date=b.date,
                                start_time=b.start_time, end_time=b.end_time, booking_type=b.booking_type)
            return booking

    def mark_completed(self, booking_id: int):
        with self.uow_factory() as uow:
            booking = uow.bookings.get_booking_by_id(booking_id)
            if booking is None:
                raise ValueError("Booking not found")

            booking.state = "Completed"
            uow.bookings.add(booking)


class PaymentService:
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    def register_payment(self, tattoo_id, client_id, booking_id, amount, payment_type, date, notes):
        with self.uow_factory() as uow:
            payment = Payment(tattoo_id=tattoo_id, client_id=client_id, booking_id=booking_id,
                              payment_type=payment_type, amount=amount, date=date, notes=notes)
            uow.payments.add(payment)

    def retrieve_all_payments(self):
        with self.uow_factory() as uow:
            all_payments = uow.payments.get_all_payments()
            vm = []
            for p in all_payments:
                client = uow.clients.get_by_id(p.client_id)
                client_name = f"{str(client.first_name)} {str(client.last_name)}"
                tattoo = uow.tattoos.get_by_id(p.tattoo_id)

                vm.append(PaymentTableVM(
                        id=p.id, tattoo_title=tattoo.title, client_name=client_name, booking_id=None,
                        payment_type=p.payment_type, amount=p.amount, note=p.notes
                    ))

            return vm
