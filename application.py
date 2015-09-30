from flask import Flask, render_template, request, redirect, json, session, jsonify
import boto
import requests
from uuid import uuid4

from handlers import temp

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.secret_key = str(uuid4())

# # add a rule for the index page.
# application.add_url_rule('/', 'index', (lambda: header_text +
#     say_hello() + instructions + footer_text))

# # add a rule when the page is accessed with a name appended to the site
# # URL.
# application.add_url_rule('/<username>', 'hello', (lambda username:
#     header_text + say_hello(username) + home_link + footer_text))

urls = [
    ('/', temp.index, ['GET']),
    ('/index', temp.index, ['GET']),
    ('/grind', temp.grind, ["GET", "POST"]),
    ('/rooms', temp.rooms, ["GET", "POST"]),
    ('/book', temp.book, ["GET", "POST"]),
    ('/bookings', temp.bookings, ["GET", "POST"]),
    ('/setup_data', temp.setup_data, ["GET"]),
    ('/bookings/create', temp.booking_create_handler, ["POST"]),
    ('/bookings/check_availability', temp.booking_availability_handler, ["POST"]),
    ('/users/signup', temp.user_signup_handler, ["POST"]),
    ('/users/login', temp.user_login_handler, ["POST"]),
    ('/users/logout', temp.user_logout_handler, ["POST"]),
    ('/venue/create', temp.create_venue_handler, ["GET"]),
    ('/event/create', temp.create_event_page_handler, ["GET"]),
    ('/event/create', temp.create_event_handler, ["POST"]),
    ('/event/list', temp.list_event_handler, ["GET"]),
]

for url in urls:
    application.add_url_rule(url[0], None, url[1], methods=url[2])        

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

