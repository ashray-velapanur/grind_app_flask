from flask import Flask, render_template, request, redirect, json, session, jsonify
import boto
import requests
from uuid import uuid4

from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController
from db.user_controller import UserController
from db.setup import setup_connection
from third_party.recurly_api import RecurlyAPI
import recurly
from recurly import Account, Transaction, BillingInfo


# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

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

recurly.SUBDOMAIN = 'beagles'
recurly.API_KEY = '413a664bcd874f4fb2b17b68dd1cbf8c'
recurly.DEFAULT_CURRENCY = 'USD'

@application.route('/')
@application.route('/index', methods=["GET", "POST"])
def index():
    print 'In index page'
    userController = UserController()
    user = userController.get_item(session['email']) if 'email' in session else None
    if not user:
        return render_template("index.html", user=user)
    else:
        return redirect('/grind')

@application.route('/grind', methods=["GET", "POST"])
def grind():
    print 'In grind page'
    controller = SpaceController()
    spaces = controller.get_items()
    userController = UserController()
    user = userController.get_item(session['email']) if 'email' in session else None
    return render_template("grind.html", spaces=spaces, user=user)

@application.route('/rooms', methods=["GET", "POST"])
def rooms():
    print 'In rooms page'
    space_controller = SpaceController()
    room_controller = RoomController()
    args = request.args
    space_id = args.get('space', '')
    space = space_controller.get_item(space_id=space_id)
    rooms = room_controller.get_items(space_id=space_id)
    user = UserController().get_item(session['email']) if 'email' in session else None
    return render_template("rooms.html", space=space, rooms=rooms, user=user)

@application.route('/book', methods=["GET", "POST"])
def book():
    print 'In book page'
    space_controller = SpaceController()
    room_controller = RoomController()
    args = request.args
    space_id = args.get('space', '')
    room_id = args.get('room', '')
    space = space_controller.get_item(space_id)
    room = room_controller.get_item(space_id, room_id)
    user = UserController().get_item(session['email']) if 'email' in session else None
    return render_template("book.html", space=space, room=room, user=user)

@application.route('/bookings', methods=["GET", "POST"])
def bookings():
    print 'In bookings page'
    controller = BookingController()
    bookings = controller.get_items()
    user = UserController().get_item(session['email']) if 'email' in session else None
    return render_template("bookings.html", bookings=bookings, user=user)

@application.route('/setup_data')
def setup_data():
    space_controller = SpaceController()
    room_controller = RoomController()

    space = space_controller.create_item(space_id='grind_broadway', name='Grind Broadway', address='1412 Broadway, 22nd Fl', city='New York', state='NY', zip='10018', phone='(646) 558 - 6026')
    room_controller.create_item(space_id=space['space_id'], room_id='play_tank', name='Play Tank', size=5, amenities_list='WiFi, Whiteboard, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone, TV/Monitor, Wired Internet', price=10)
    room_controller.create_item(space_id=space['space_id'], room_id='shark_tank', name='Shark Tank', size=18, amenities_list='WiFi, Whiteboard, Wired Internet, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone, TV/Monitor, Video Conference', price=25)
    room_controller.create_item(space_id=space['space_id'], room_id='work_tank', name='Work Tank', size=5, amenities_list='WiFi, Whiteboard, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone,TV/Monitor, Wired Internet', price=10)

    '''
    space = controller.create_space('Grind Park', '419 Park Avenue South, 2nd Fl', 'New York', 'NY', '10016', '(646) 558 - 3250')
    controller.create_room(space['space_id'], 'Think Tank', 10, 'WiFi, TV/Monitor, Whiteboard, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone, Wired Internet',15)

    space = controller.create_space('Grind LaSalle', '2 N. LaSalle Street', 'Chicago', 'IL', '60602', '(312) 488 - 4887')
    controller.create_room(space['space_id'], 'Do Tank', 8, 'WiFi, TV/Monitor, Whiteboard, Wired Internet, Accessibility, Coffee/Tea, Filtered Water, On-site Restaurant, Print/Scan/Copy', 12)
    controller.create_room(space['space_id'], 'Play Tank', 4, 'WiFi, TV/Monitor, Whiteboard, Accessibility, Coffee/Tea, Filtered Water, Wired Internet, On-site Restaurant, Print/Scan/Copy', 8)
    controller.create_room(space['space_id'], 'Think Tank', 8, 'WiFi, TV/Monitor, Whiteboard, Wired Internet, Accessibility, Coffee/Tea, Filtered Water, On-site Restaurant, Print/Scan/Copy', 12)
    controller.create_room(space['space_id'], 'Work Tank', 4, 'WiFi, Whiteboard, Accessibility, Coffee/Tea, Filtered Water, Wired Internet, On-site Restaurant, Print/Scan/Copy', 8)
    '''
    user = UserController().get_item(session['email']) if 'email' in session else None
    return redirect('/', user=user)
 
@application.route('/test')
def test():
    controller = SpaceController()
    for space in controller.get_spaces():
        for room in controller.get_rooms(space):
            booking_controller = BookingController()
            booking_controller.create_booking(space, room)
    user = UserController().get_item(session['email']) if 'email' in session else None
    return redirect('/', user=user)

@application.route('/bookings/create', methods=["POST"])
def booking_create_handler():
    print "In booking create"
    user = UserController().get_item(session['email']) if 'email' in session else None
    if user:
        form = request.form
        space_id = form['space_id']
        room_id = form['room_id']
        controller = BookingController()
        account = Account.get(user['email'])
        account.billing_info = BillingInfo(token_id = form['recurly-token'])
        account.save()
        transaction = Transaction(
          amount_in_cents=int(form['amount'])*100,
          currency='INR',
          account=account
        )
        transaction.save()
        if transaction.status == 'success':
            controller.create_item(space_id=space_id, room_id=room_id)
        return redirect("/bookings")

@application.route('/users/signup', methods=["POST"])
def user_signup_handler():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    controller = UserController()
    controller.create_item(email=email, first_name=first_name, last_name=last_name)
    session['email'] = email
    recurlyapi = RecurlyAPI()
    recurlyapi.create_account(email, email, first_name, last_name)
    return redirect('/grind')

@application.route('/users/login', methods=["POST"])
def user_login_handler():
    email = request.form['email']
    controller = UserController()
    user = controller.get_item(email)
    if user:
        session['email'] = email
        return redirect('/grind')
    else:
        return jsonify({'success': False, 'message': 'Email not in database'})

@application.route('/users/logout')
def user_logout_handler():
    session.pop("email", None)
    return redirect('/')

@application.route('/users/current_user')
def current_user_handler():
    return jsonify(session)

@application.route('/venue/create')
def create_venue_handler():
    response = requests.post(
        "https://www.eventbriteapi.com/v3/venues/",
        headers = {
            "Authorization": "Bearer WWVNO7GS2EN36S5JDLS3",
        },
        verify = False,  # Verify SSL certificate,
        data = {'venue.name':'Grind Park',
                'venue.address.latitude':'37.78',
                'venue.address.longitude':'-122.4',
                "venue.address.address_1": "Apartment 106",
                "venue.address.address_2": "45 Royal Street",
                "venue.address.city": "London",
                "venue.address.region": "London",
                "venue.address.postal_code": "SW1A 1AA",
                "venue.address.country": "GB"
                }
    )
    print response.json()

@application.route('/event/create', methods=["GET"])
def create_event_page_handler():
    print 'In create event page'
    userController = UserController()
    user = userController.get_item(session['email']) if 'email' in session else None
    return render_template("create_event.html")

@application.route('/event/create', methods=["POST"])
def create_event_handler():
    print request.form['start']+':00Z'
    print request.form['end']+':00Z'
    response = requests.post(
        "https://www.eventbriteapi.com/v3/events/",
        headers = {
            "Authorization": "Bearer WWVNO7GS2EN36S5JDLS3",
        },
        verify = False,  # Verify SSL certificate,
        data = {'event.name.html':request.form['name'],
                'event.start.utc':request.form['start']+':00Z',
                'event.start.timezone':'America/New_York',
                "event.end.utc":request.form['end']+':00Z',
                "event.end.timezone": "America/New_York",
                "event.currency": "USD",
                "event.venue_id":"11584742"
                }
    )
    print response.json()
    return redirect('/')

@application.route('/event/list', methods=["GET"])
def list_event_handler():
    response = requests.get(
        "https://www.eventbriteapi.com/v3/users/115769153821/owned_events/",
        headers = {
            "Authorization": "Bearer WWVNO7GS2EN36S5JDLS3",
        },
        verify = False,  # Verify SSL certificate,
        data = {'order_by':"start_asc"}
    )
    events = response.json()['events']
    return render_template("events.html", events=events)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

