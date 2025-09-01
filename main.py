from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import AddClientForm
from database import SessionFactory
from repositories import ClientRepository
from unit_of_works import SqlAlchemyUnitOfWork
from services import ClientService


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    bootstrap = Bootstrap5(app)
    uow_factory = lambda: SqlAlchemyUnitOfWork(SessionFactory)
    client_service = ClientService(uow_factory)

    @app.route('/')
    def route_home():
        return render_template('index.html')

    @app.route('/bookings')
    def route_bookings():
        return render_template('bookings.html')

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
            selected_client = client_service.get_client(client_id)
            print(selected_client)

        return render_template(
            'clients.html',
            client_profiles=client_service.get_all_clients(),
            selected_client=selected_client
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

    @app.route("/add_tattoo")
    def route_add_tattoo():
        return render_template("add_tattoo.html")

    @app.route("/test/", defaults={"var": None})
    @app.route("/test/<var>")
    def route_test(var):
        return f"<h1>{var} This is a test</h1>"

    app.run(debug=True)


create_app()
