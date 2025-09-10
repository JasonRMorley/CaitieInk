from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class ClientMiniVM:
    id: int
    name: str


@dataclass
class TattooMiniVM:
    id: int
    title: str


@dataclass
class TableBookingVM:
    id: int
    date: date
    start_time: time
    end_time: time
    booking_type: str
    client_id: int
    tattoo_id: int
    client: ClientMiniVM
    tattoo: TattooMiniVM | None


@dataclass
class BookingVM:
    id: int
    tattoo_id: int
    client_id: int

    date: date
    start_time: time
    end_time: time
    booking_type: str


@dataclass
class PaymentVM:
    id: int
    amount: float
    method: str | None


@dataclass
class PaymentTableVM:
    id: int
    tattoo_title: str
    client_name: str
    booking_id: int | None
    payment_type: str
    amount: float
    note: str


@dataclass
class TattooVM:
    id: int
    title: str
    note: str | None
    price_estimate: int | None
    price_final: int | None
    status: str
    bookings: list[BookingVM] = field(default_factory=list)
    payments: list[PaymentVM] = field(default_factory=list)


@dataclass
class ClientDetailVM:
    id: int
    first_name: str
    last_name: str
    phone: str
    notes: str | None
    tattoos: list[TattooVM] = field(default_factory=list)
    bookings: list[BookingVM] = field(default_factory=list)
    payments: list[PaymentVM] = field(default_factory=list)

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

@dataclass
class ExpenseVM:
    id: int
    amount: int
    date: date
    item: str
    category: str
    notes: str
