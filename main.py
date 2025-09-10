from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import *
from database import SessionFactory
from unit_of_works import SqlAlchemyUnitOfWork
from services import *
from dev import print_all_entities


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    bootstrap = Bootstrap5(app)

    uow_factory = lambda: SqlAlchemyUnitOfWork(SessionFactory)
    client_service = ClientService(uow_factory)
    tattoo_service = TattooService(uow_factory)
    booking_service = BookingService(uow_factory)
    payment_service = PaymentService(uow_factory)
    expense_service = ExpensesService(uow_factory)

    @app.route("/")
    def route_home():
        return render_template("home/index.html")

    @app.route('/bookings/', defaults={'state': "Current"})
    @app.route('/bookings/<state>')
    def route_bookings(state):

        booking_list = booking_service.retrieve_bookings_for_table(state)
        form = PaymentForm()

        return render_template('bookings/bookings.html', bookings=booking_list, form=form)

    @app.route('/payments')
    def route_payments():
        payment_list = payment_service.retrieve_all_payments()
        return render_template('payments/payments.html', payments=payment_list)

    @app.route("/payment/add", methods=["POST"])
    def route_add_payment():
        form = PaymentForm()

        if not form.validate_on_submit():
            flash("Please correct the errors in the payment form.", "warning")
            return redirect(url_for("route_bookings"))

        if form.validate_on_submit():

            booking_id = int(form.booking_id.data)
            booking = booking_service.retrieve_booking_vm_by_id(booking_id)

            if booking is None:
                flash("Booking not found.", "danger")
                return redirect(url_for("route_bookings"))

            payment_service.register_payment(
                tattoo_id=booking.tattoo_id,
                client_id=booking.client_id,
                booking_id=booking_id,
                payment_type=form.payment_type.data,
                amount=form.amount.data,
                date=form.date.data,
                notes=form.notes.data or "",
            )

            booking_service.mark_completed(booking_id)
            flash("Payment recorded and booking completed.", "success")

        return redirect(url_for("route_bookings"))

    @app.route('/clients/', defaults={'client_id': None})
    @app.route('/clients/<int:client_id>/')
    def route_clients(client_id=None):
        selected_client = None

        client_list = client_service.retrieve_all_clients()
        print_all_entities(client_list)

        if client_id:
            selected_client = client_service.retrieve_client_profile(client_id)

        return render_template(
            'clients/clients.html',
            client_profiles=client_list,
            selected_client=selected_client,
        )

    @app.route("/clients/edit/<client_id>", methods=["GET", "POST"])
    def route_edit_client(client_id: int):
        form = EditClientForm()
        if form.validate_on_submit():
            first_name, last_name, phone_number, notes = (
                form.first_name.data, form.last_name.data, form.phone_number.data, form.notes.data
            )
            client_service.edit_client(client_id=client_id, first_name=first_name, last_name=last_name,
                                       phone_number=phone_number, notes=notes)

            flash("Client details updated", "success")
            return redirect(f"/clients/{client_id}")


        return render_template("clients/edit_clients.html", form=form)

    @app.route("/clients/add", methods=["GET", "POST"])
    def route_add_client():
        form = AddClientForm()
        if form.validate_on_submit():
            first_name, last_name, phone_number, notes = (
                form.first_name.data, form.last_name.data, form.phone_number.data, form.notes.data
            )
            client_service.register_client(
                first_name=first_name, last_name=last_name, phone_number=phone_number, notes=notes
            )
            flash(f"Client, {first_name} {last_name} added!", "success")
            return redirect(url_for("route_clients"))
        return render_template("clients/add_client.html", form=form)

    @app.route("/tattoo/add/<client_id>/", methods=["GET", "POST"])
    def route_add_tattoo(client_id=None):
        form = AddTattoo()
        if form.validate_on_submit():
            title, note = form.data["title"], form.data["note"]
            tattoo_service.register_tattoo(client_id=client_id, title=title, note=note)
            flash("Tattoo Created", "success")
            return redirect(url_for("route_clients") + f"/{client_id}")

        return render_template("tattoos/add_tattoo.html", form=form)

    @app.route("/tattoo/edit/<client_id>/<tattoo_id>", methods=["GET", "POST"])
    def route_edit_tattoo(client_id, tattoo_id):
        form = EditTattoo()
        if form.validate_on_submit():
            tattoo_service.edit_tattoo(client_id=int(client_id),
                                       tattoo_id=int(tattoo_id),
                                       title=form.data["title"],
                                       note=form.data["note"],
                                       estimate=form.data["price_estimate"],
                                       price=form.data["price_final"],
                                       status=form.data["status"]
                                       )
            flash("Tattoo Edited", "success")
            return redirect(url_for("route_clients") + f"/{client_id}")
        return render_template("tattoos/edit_tattoo.html", form=form)

    @app.route("/booking/",
               defaults={"client_id": None, "tattoo_id": None}
               )
    @app.route("/booking/<client_id>/<tattoo_id>", methods=["GET", "POST"])
    def route_add_booking(client_id, tattoo_id):
        form = BookingForm()
        if form.validate_on_submit():
            booking_service.register_booking(client_id=client_id,
                                             tattoo_id=tattoo_id,
                                             booking_date=form.data["date"],
                                             start_time=form.data["start_time"],
                                             end_time=form.data["end_time"],
                                             booking_type=form.data["booking_type"],
                                             state="Current"
                                             )
            flash("Booking Created", "success")
            return redirect(url_for("route_clients") + f"/{client_id}")

        return render_template("bookings/booking.html", form=form)

    @app.route('/expenses/add', methods=["GET", "POST"])
    def route_add_expense():
        form = ExpenseForm()
        if form.validate_on_submit():
            expense_service.register_expense(
                amount=form.data['amount'], expense_date=form.data['date'], item=form.data['item'],
                category=form.data['category'], notes=form.data['notes']
            )
            flash("Expense Added", "success")
            return redirect(url_for("route_expenses"))

        return render_template('expenses/add_expense.html', form=form)

    @app.route('/expenses', methods=["GET", "POST"])
    def route_expenses():
        e_list = expense_service.retrieve_all_expenses()
        for e in e_list:
            print(e.amount)

        return render_template('expenses/expenses.html', expense_list=e_list)

    app.run(debug=True)


create_app()
