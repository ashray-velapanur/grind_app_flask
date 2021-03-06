from flask import Flask, render_template, request, redirect, json, session, jsonify
import boto
import requests
from uuid import uuid4
from handlers import temp, bookings, users, cobot, hubspot, auth, layer

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
    ('/identity_token', layer.get_identity_token, ['GET']),
    ('/test', temp.test, ['GET']),
    ('/index', temp.index, ['GET']),
    ('/grind', temp.grind, ["GET", "POST"]),
    ('/spaces', temp.get_spaces, ["POST"]),
    ('/rooms', temp.rooms, ["GET"]),
    ('/rooms', temp.get_rooms, ["POST"]),
    ('/book/room', bookings.booking_create_handler, ["POST"]),
    ('/book', temp.book, ["GET", "POST"]),
    ('/bookings', cobot.bookings_handler, ["GET"]),
    ('/bookings', temp.get_bookings, ["POST"]),
    ('/setup_data', temp.setup_data, ["GET"]),
    ('/venue/create', temp.create_venue_handler, ["GET"]),
    ('/bookings/create', bookings.booking_create_web_handler, ["POST"]),
    ('/bookings/check_availability', bookings.booking_availability_handler, ["POST"]),
    ('/linkedin/callback', users.linkedin_login_handler, ["GET"]),
    ('/users/signup', users.user_signup_handler, ["POST"]),
    ('/users/login', users.user_login_handler, ["POST"]),
    ('/users/logout', users.user_logout_handler, ["GET"]),
    ('/users/industry', users.get_users_for_industry, ["POST"]),
    ('/auth/linkedin', auth.linkedin_auth_handler, ["GET"]),
    ('/auth/logout', auth.logout, ["GET", "POST"]),
    ('/auth/check_login', auth.check_login_handler, ["GET"]),
    ('/event/create', temp.create_event_page_handler, ["GET"]),
    ('/event/create', bookings.create_event_handler, ["POST"]),
    ('/events/create', bookings.create_event, ["POST"]),
    ('/events/list', bookings.list_event_handler, ["GET"]),
    ('/events/list', bookings.get_events_handler, ["POST"]),
    ('/events/tickets', bookings.get_tickets_handler, ["GET"]),
    ('/cobot/auth', cobot.auth_handler, ["GET"]),
    ('/cobot/callback', cobot.callback_handler, ["GET"]),
    ('/cobot/create_member', cobot.create_member_handler, ["GET"]),
    ('/cobot/assign_pass', cobot.assign_pass_handler, ["POST"]),
    ('/cobot/checkin', cobot.checkin_handler, ["POST"]),
    ('/cobot/all_checkins', cobot.all_checking_handler, ["GET"]),
    ('/hubspot/auth', hubspot.hubspot_auth_handler, ["GET"]),
    ('/hubspot/callback', hubspot.hubspot_callback_handler, ["GET"]),
    ('/hubspot/contacts', hubspot.hubspot_contacts_handler, ["GET"]),
    ('/hubspot/search', hubspot.hubspot_search_handler, ["POST"]),
    ('/hubspot/create_contact', hubspot.hubspot_create_contact_handler, ["POST"]),
    ('/hubspot/deal/create', hubspot.hubspot_deal_create_handler, ["POST"]),
    ('/hubspot/deal/update', hubspot.hubspot_deal_update_handler, ["POST"]),
    ('/hubspot/deal/list', hubspot.hubspot_deal_list_handler, ["GET"]),
    ('/hubspot/workflows/list', hubspot.hubspot_workflows_list_handler, ["GET"]),
    ('/hubspot/workflows/create', hubspot.hubspot_workflows_create_handler, ["POST"])
]

for url in urls:
    application.add_url_rule(url[0], None, url[1], methods=url[2])        

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

