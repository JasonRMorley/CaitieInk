from dataclasses import dataclass, field
from datetime import date, time

@dataclass
class ConsultationVM:
    id: int
    path: str
    notes: str | None

@dataclass
class DesignVM:
    id: int
    path: str
    notes: str | None

@dataclass
class BookingVM:
    id: int
    date: date
    start_time: time
    end_time: time

@dataclass
class PaymentVM:
    id: int
    amount: float
    method: str | None

@dataclass
class TattooVM:
    id: int
    title: str
    note: str | None
    price_estimate: int | None
    price_final: int | None
    status: str
    consultation: ConsultationVM | None = None
    design: DesignVM | None = None
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

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
