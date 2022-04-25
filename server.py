from flask import render_template, redirect, url_for
from init import app, db
from ticket_handler import TicketHandler, Movie, Showing, Ticket
from billing_handler import BillingHandler
from sqlalchemy import inspect
from forms import TicketsForm, PurchaseForm

# Create Handler Objects

ticketer = TicketHandler()
biller = BillingHandler()


# ----------- Routes --------------


# Home

@app.route('/')
def home():
    current_movies = []
    query = db.session.query(Movie)
    for movie in query:
        current_movies.append({c.key: getattr(movie, c.key) for c in inspect(movie).mapper.column_attrs})
    return render_template('index.html', movies=current_movies)


@app.route('/showings/<ticket>')
def showings(ticket):
    movie = Movie.query.get(ticket)
    return render_template('showings.html', movie=movie)


@app.route('/purchase/<showing_id>', methods=['GET', 'POST'])
def purchase(showing_id):
    showing = Showing.query.get(showing_id)
    movie = Movie.query.get(showing.movie)
    ticket_form = TicketsForm()
    if ticket_form.validate_on_submit():
        return redirect(url_for('pay', data=(showing_id, ticket_form.number_of_tickets.data)))
    return render_template('purchase.html', showing=showing, movie=movie, form=ticket_form)

@app.route('/buy/<data>', methods=['GET', 'POST'])
def buy(data):
    return render_template('buy.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)