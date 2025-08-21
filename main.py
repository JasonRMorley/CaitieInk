from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
import wtforms
from forms import AddClientForm

from database import Session, get_all_clients, add_client, get_client_details
from models import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bookings')
def bookings():
    return render_template('bookings.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')


@app.route('/clients/', defaults={'client_id': None})
@app.route('/clients/<client_id>/')
def clients(client_id=None):
    client_list = get_all_clients()

    selected_client = None
    if client_id:
        client_id = client_id.strip("<").strip(">")
        selected_client = get_client_details(client_id)

    return render_template(
        'clients.html',
        clients=client_list,
        client_details=selected_client
    )



@app.route("/add_client", methods=["GET", "POST"])
def add_client_page():
    form = AddClientForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        notes = form.notes.data
        client = Client(first_name=first_name, last_name=last_name, phone_number=phone_number, notes=notes)
        add_client(client)

        flash(f"Client, {first_name} {last_name} added!", "success")

        return redirect(url_for("add_client_page"))
    return render_template("add_client.html", form=form)


if __name__ == "__main__": \
        app.run(debug=True)
