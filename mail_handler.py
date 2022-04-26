import smtplib
from init import db
from ticket_handler import Showing, Movie, Ticket


def send_tickets(send_data):

    showing = Showing.query.get(send_data['showing_id'])
    movie = Movie.query.get(showing.movie)

    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user="DevonLearnsCode@yahoo.com", password="rdjzisxknmqbblyl")
        connection.sendmail(
            from_addr="DevonLearnsCode@yahoo.com",
            to_addrs=send_data['buyer'],
            msg=f"Subject:Tickets for {movie.title}\n\nThank you for choosing Movie Time!\n\n"
            "Here are your tickets purchased on xx/xx/xxxx:\n\n"
            f"{build_tickets(send_data['ticket_ids'], send_data['showing_id'])}"
            "Please present this email at the theatre for admittance\n\n"
            "Enjoy the Show!"
        )

def build_tickets(ticket_ids, showing_id):

    build_list = []
    showing = Showing.query.get(showing_id)
    movie = Movie.query.get(showing.movie)

    for ticket_id in ticket_ids:
        ticket = Ticket.query.get(ticket_id)
        build_list.append(f"{ticket.ticket_code} | {ticket.ticket_type} | {movie.title} | {showing.date} at {showing.time}"
                          f"\n\n ~~+ BARCODE PLACEHOLDER +~~ \n\n")
    return ''.join(build_list)