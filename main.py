from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import *
from database import SessionFactory
from repositories import ClientRepository
from unit_of_works import SqlAlchemyUnitOfWork
from services import *


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    bootstrap = Bootstrap5(app)

    uow_factory = lambda: SqlAlchemyUnitOfWork(SessionFactory)
    client_service = ClientService(uow_factory)
    tattoo_service = TattooService(uow_factory)
    booking_service = BookingService(uow_factory)

    @app.route('/')
    def route_home():
        return render_template('index.html')

    @app.route('/bookings')
    def route_bookings():
        booking_list = booking_service.retrieve_bookings_for_table()

        return render_template('bookings.html', bookings=booking_list)

    @app.route('/payments')
    def route_payments():

        return render_template('payments.html')

    @app.route('/reports')
    def route_reports():
        return render_template('reports.html')

    @app.route('/clients/', defaults={'client_id': None})
    @app.route('/clients/<int:client_id>/')
    def route_clients(client_id=None):
        selected_client = None
        if client_id:
            selected_client = client_service.retrieve_client_profile(client_id)

        return render_template(
            'clients.html',
            client_profiles=client_service.retrieve_all_clients(),
            selected_client=selected_client,
        )

    @app.route("/add_client", methods=["GET", "POST"])
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

            return redirect(url_for("add_client_page"))
        return render_template("add_client.html", form=form)

    @app.route("/add_tattoo/<client_id>/", methods=["GET", "POST"])
    def route_add_tattoo(client_id=None):
        form = AddTattoo()
        if form.validate_on_submit():
            title, note = form.data["title"], form.data["note"]
            tattoo_service.register_tattoo(client_id=client_id, title=title, note=note)

        return render_template("add_tattoo.html", form=form)

    @app.route("/edit_tattoo/<client_id>/<tattoo_id>", methods=["GET", "POST"])
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
        return render_template("edit_tattoo.html", form=form)

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
                                             booking_type=form.data["booking_type"]
                                             )

        return render_template("booking.html", form=form)

    app.run(debug=True)


create_app()
