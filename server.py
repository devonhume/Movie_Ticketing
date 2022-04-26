from flask import render_template, redirect, url_for
from init import app, db
from ticket_handler import TicketHandler, Movie, Showing, Ticket
from billing_handler import BillingHandler
from sqlalchemy import inspect
from forms import TicketsForm, PurchaseForm,ConfirmForm

# Create Handler Objects

ticketer = TicketHandler()
biller = BillingHandler()
tickets = 0
purchase_flag = 0


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
    global tickets
    global purchase_flag
    showing = Showing.query.get(showing_id)
    movie = Movie.query.get(showing.movie)
    ticket_form = TicketsForm()
    purchase_form = PurchaseForm()
    success_button = ConfirmForm()
    fail_button = ConfirmForm()
    ticket_flag = False
    if tickets > showing.seats_available:
        ticket_flag = True
    if ticket_form.submit.data and ticket_form.validate_on_submit():
        tickets = ticket_form.number_of_tickets.data
        return redirect(url_for('purchase', showing_id=showing_id))
    if purchase_form.purchase_submit.data and purchase_form.validate_on_submit():
        order = {
            'tickets': tickets,
            'showing_id': showing_id,
            'total': tickets * showing.ticket_price
        }
        print(order)
        billing_data = {
            'buyer': purchase_form.email.data,
            'first_name': purchase_form.first_name.data,
            'last_name': purchase_form.last_name.data,
            'cc_number': purchase_form.credit_card.data,
            'cc_month': purchase_form.exp_month.data,
            'cc_year': purchase_form.exp_year.data,
            'code': purchase_form.secret_code.data
        }
        print(billing_data)
        if biller.buy_tickets(purchases=order, billing_info=billing_data):
            new_seats = showing.seats_available - tickets
            showing.seats_available = new_seats
            db.session.commit()
            tickets = 0
            purchase_flag = 1
            return redirect(url_for('purchase', showing_id=showing_id))
        else:
            purchase_flag = 2
            return redirect(url_for('purchase', showing_id=showing_id))
    if success_button.confirm.data and success_button.validate_on_submit():
        purchase_flag = 0
        return redirect(url_for('home'))
    if fail_button.confirm.data and fail_button.validate_on_submit():
        purchase_flag = 0
        return redirect(url_for('purchase', showing_id=showing_id))


    return render_template('purchase.html',
                           showing=showing,
                           movie=movie,
                           tickets=tickets,
                           ticket_form=ticket_form,
                           purchase_form=purchase_form,
                           ticket_flag=ticket_flag,
                           purchase_flag=purchase_flag,
                           fail_button=fail_button,
                           success_button=success_button
                           )




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)