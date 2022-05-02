import init
import billing_handler
import ticket_handler
import mail_handler
import server
import unittest



# Tests for Billing_Handler:
# 1) Instantiate Billing handler class
# 2) Ticket_total
# 3) Buy_tickets
# 4) Charge Customer

class TestBillingHandler(unittest.TestCase):

    # does BillingHandler successfully instantiate?
    def test_handler_create(self):
        handler = billing_handler.BillingHandler()
        self.assertEqual(handler.status, True)

    def test_buy_tickets(self):
        handler = billing_handler.BillingHandler()
        showing = ticket_handler.Showing.query.get(0)

        # data for standard ticket order
        data_1_order = {
            'adult_tickets': 3,
            'child_tickets': 3,
            'showing_id': 0,
            'total': 3 * showing.ticket_price + 3 * showing.ticket_price / 2
        }
        data_1_billing_data = {
            'buyer': 'devonlearnscode@gmail.com',
            'first_name': 'test FN',
            'last_name': 'test_LN',
            'cc_number': 000000000000000,
            'cc_month': 00,
            'cc_year': 00,
            'code': 000
        }

        result = handler.buy_tickets(purchases=data_1_order, billing_info=data_1_billing_data)
        # did it successfully return ids for six tickets?
        self.assertEqual(result, True)

        # check tickets created

        # check number of adult tickets
        tickets = ticket_handler.Ticket.query.filter_by(showing=0, ticket_type='adult')
        count = 0
        for ticket in tickets:
            count += 1
        self.assertEqual(count, 3)

        # check number of child tickets
        tickets = ticket_handler.Ticket.query.filter_by(showing=0, ticket_type='child')
        count = 0
        for ticket in tickets:
            count += 1
        self.assertEqual(count, 3)

        # check total number of tickets found
        tickets = ticket_handler.Ticket.query.filter_by(showing=0)
        count = 0
        for ticket in tickets:
            count += 1
        self.assertEqual(count, 6)

        # check individual ticket attributes
        for ticket in tickets:
            self.assertNotEqual(ticket.ticket_code, None)
            self.assertEqual(ticket.ticket_used, 0)
            self.assertNotEqual(ticket.buyer, None)

        # cleanup test tickets
        for ticket in tickets:
            init.db.session.delete(ticket)
            init.db.session.commit()

        # data for overselling
        data_2_order = {
            'adult_tickets': 8,
            'child_tickets': 3,
            'showing_id': 0,
            'total': 3 * showing.ticket_price + 3 * showing.ticket_price / 2
        }

        result = handler.buy_tickets(purchases=data_2_order, billing_info=data_1_billing_data)
        self.assertEqual(result, False)



# Tests for Ticket_handler
# 1) Instantiate Ticket Handler
# 2) get_all_movies
# 3) generate Tickets
# 4) generate ticket code

class TestTicketHandler(unittest.TestCase):

    def test_handler_create(self):
        handler = ticket_handler.TicketHandler()
        self.assertEqual(handler.status, True)

    def test_generate_tickets(self):
        handler = ticket_handler.TicketHandler()
        buyer = 'devonlearnscode@gmail.com'

        # test adult ticket creation
        result = handler.generate_tickets(0, 5, 0, buyer)
        self.assertNotEqual(result, False)
        self.assertEqual(len(result), 5)

        for id in result:
            ticket = ticket_handler.Ticket.query.get(id)
            self.assertEqual(ticket.ticket_type, 'adult')
            self.assertEqual(ticket.ticket_used, 0)
            self.assertNotEqual(ticket.ticket_code, None)

        # cleanup test tickets
        for id in result:
            ticket = ticket_handler.Ticket.query.get(id)
            init.db.session.delete(ticket)
            init.db.session.commit()

        # test child ticket creation
        result = handler.generate_tickets(0, 0, 5, buyer)
        self.assertNotEqual(result, False)
        self.assertEqual(len(result), 5)

        for id in result:
            ticket = ticket_handler.Ticket.query.get(id)
            self.assertEqual(ticket.ticket_type, 'child')
            self.assertEqual(ticket.ticket_used, 0)
            self.assertNotEqual(ticket.ticket_code, None)

        # cleanup test tickets
        for id in result:
            ticket = ticket_handler.Ticket.query.get(id)
            init.db.session.delete(ticket)
            init.db.session.commit()

        # Test overselling
        result = handler.generate_tickets(0, 11, 0, buyer)
        self.assertEqual(result, False)

        # test no tickets passed
        result = handler.generate_tickets(0, 0, 0, buyer)
        self.assertEqual(result, False)




# Tests for Mail Handler
# Send Tickets
# Build Tickets

# Tests for Server
# Home
# Showings
# Purchase

if __name__ == '__main__':
    unittest.main()