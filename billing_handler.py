from init import db
from ticket_handler import TicketHandler, Showing, Ticket


class BillingHandler:

    def __init__(self):
        self.ticketer = TicketHandler()

    def ticket_total(self, tickets, showing_id):
        showing = Showing.query.get(showing_id)
        if showing.seats_available < tickets:
            return False
        return showing.ticket_price * tickets

    def buy_tickets(self, purchases, billing_info):
        showing = Showing.query.get(purchases['showing_id'])
        if showing.seats_available < purchases['tickets']:
            print("Not Enough Seats")
            return False

        tickets = self.ticketer.generate_tickets(
            showing_id=purchases['showing_id'],
            tickets=purchases['tickets'],
            buyer=billing_info['buyer']
        )

        if tickets:
            if self.charge_customer(total=purchases['total'], billing_info=billing_info):
                print("Charge Successful")
                return True
            else:
                for ticket in tickets:
                    del_ticket = Ticket.query.get(ticket)
                    db.session.delete(del_ticket)
                    db.commit
                print("Charge Failed")
                return False

    def charge_customer(self, total, billing_info):

        # Charge Customer via Electronic Billing API
        # If Successful, return True
        # If Charge Fails Return False

        print(f"Charging {billing_info['first_name']} {billing_info['last_name']} ${total} to credit card number "
              f"{billing_info['cc_number']}, exp date {billing_info['cc_month']}/{billing_info['cc_year']}, "
              f"code {billing_info['code']}")

        return True