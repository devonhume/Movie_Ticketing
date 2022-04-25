from init import db
from ticket_handler import TicketHandler


class BillingHandler:

    def __init__(self):
        self.ticketer = TicketHandler()

    def ticket_total(self, tickets, showing_id):
        showing = db.showings.query.filter_by(id=showing_id).first()
        if showing.seats_available < tickets:
            return False
        return showing.ticket_price * tickets

    def buy_tickets(self, purchases, billing_info):
        showing = db.showings.query.filter_by(id=purchases['showing_id']).first()
        if showing.seats_available < purchases['tickets']:
            return False

        tickets = self.ticketer.generate_tickets(
            showing_id=purchases['showing_id'],
            tickets=purchases['tickets'],
            buyer=billing_info['buyer']
        )

        if tickets:
            if self.charge_customer(total=purchases['total'], billing_info=billing_info):
                return True
            else:
                for ticket in tickets:
                    del_ticket = db.tickets.query.filter_by(id=ticket).first()
                    db.session.delete(del_ticket)
                    db.commit
                return False

    def charge_customer(self, total, billing_info):

        # Charge Customer via Electronic Billing API
        # If Successful, return True
        # If Charge Fails Return False

        return True