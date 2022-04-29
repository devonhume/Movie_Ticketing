import string
import random
from init import db
from sqlalchemy.orm import relationship


class TicketHandler:

    def __init__(self):
        pass

    def get_all_movies(self):
        dict = {}
        for column in db.movies.columns:
            dict[column.name] = db.getattr(self, column.name)
        return dict

    def generate_tickets(self, showing_id, adult_tickets, child_tickets, buyer):
        showing = Showing.query.get(showing_id)
        ticket_ids = []
        if showing.seats_available < adult_tickets + child_tickets:
            return False
        elif adult_tickets or child_tickets:
            if adult_tickets:
                for i in range(adult_tickets):
                    new_code = self.generate_ticket_code()
                    new_ticket = Ticket(
                        showing=showing_id,
                        ticket_code=new_code,
                        ticket_type='adult',
                        ticket_used=False,
                        buyer=buyer
                    )
                    db.session.add(new_ticket)
                    db.session.commit()
                    ticket_ids.append(new_ticket.id)
            if child_tickets:
                for i in range(child_tickets):
                    new_code = self.generate_ticket_code()
                    new_ticket = Ticket(
                        showing=showing_id,
                        ticket_code=new_code,
                        ticket_type='child',
                        ticket_used=False,
                        buyer=buyer
                    )
                    db.session.add(new_ticket)
                    db.session.commit()
                    ticket_ids.append(new_ticket.id)
            return ticket_ids
        else:
            return False

    def generate_ticket_code(self):
        while True:
            code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            if not Ticket.query.filter_by(ticket_code=code).first():
                return code


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    runtime_hrs = db.Column(db.Integer, nullable=False)
    runtime_mins = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    showings = relationship("Showing")


class Showing(db.Model):
    __tablename__ = 'showings'
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.Integer, db.ForeignKey('movies.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    seats_total = db.Column(db.Integer, nullable=False)
    tickets = relationship("Ticket")


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    showing = db.Column(db.Integer, db.ForeignKey('showings.id'))
    ticket_code = db.Column(db.String(20), unique=True, nullable=False)
    ticket_type = db.Column(db.String(20), nullable=False)
    ticket_used = db.Column(db.Boolean, nullable=False)
    buyer = db.Column(db.String(250), nullable=False)



if __name__ == "__main__":
    # db.create_all()
    pass

