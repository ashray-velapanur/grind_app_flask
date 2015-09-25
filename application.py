from flask import Flask, render_template, request, redirect, json, session, jsonify
import boto

from uuid import uuid4

from db.space_controller import SpaceController
from db.booking_controller import BookingController
from db.user_controller import UserController
from db.setup import setup_connection
from third_party.recurly_api import RecurlyAPI


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

@application.route('/')
@application.route('/index', methods=["GET", "POST"])
def index():
    print 'In index page'
    userController = UserController()
    user = userController.get_user(session['email']) if 'email' in session else None
    if not user:
        return render_template("index.html", user=user)
    else:
        return redirect('/grind')

@application.route('/grind', methods=["GET", "POST"])
def grind():
    print 'In grind page'
    controller = SpaceController()
    spaces = controller.get_spaces()
    userController = UserController()
    user = userController.get_user(session['email']) if 'email' in session else None
    return render_template("grind.html", spaces=spaces, user=user)

@application.route('/rooms', methods=["GET", "POST"])
def rooms():
    print 'In rooms page'
    controller = SpaceController()
    args = request.args
    space_id = args.get('space', '')
    space = controller.get_spaces(space_id=space_id)
    rooms = controller.get_rooms(space)
    user = UserController().get_user(session['email']) if 'email' in session else None
    return render_template("rooms.html", space=space, rooms=rooms, user=user)

@application.route('/book', methods=["GET", "POST"])
def book():
    print 'In book page'
    controller = SpaceController()
    args = request.args
    space_id = args.get('space', '')
    room_id = args.get('room', '')
    space = controller.get_spaces(space_id=space_id)
    room = controller.get_rooms(space, room_id=room_id)
    user = UserController().get_user(session['email']) if 'email' in session else None
    return render_template("book.html", space=space, room=room, user=user)

@application.route('/bookings', methods=["GET", "POST"])
def bookings():
    print 'In bookings page'
    controller = BookingController()
    bookings = controller.get_bookings()
    user = UserController().get_user(session['email']) if 'email' in session else None
    return render_template("bookings.html", bookings=bookings, user=user)

@application.route('/setup_data')
def setup_data():
    controller = SpaceController()

    space = controller.create_space('Grind Broadway', '1412 Broadway, 22nd Fl', 'New York', 'NY', '10018', '(646) 558 - 6026')
    controller.create_room(space, 'Play Tank', 5, 'WiFi, Whiteboard, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone, TV/Monitor, Wired Internet', 10)
    controller.create_room(space, 'Shark Tank', 18, 'WiFi, Whiteboard, Wired Internet, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone, TV/Monitor, Video Conference',25)
    controller.create_room(space, 'Work Tank', 5, 'WiFi, Whiteboard, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone,TV/Monitor, Wired Internet', 10)

    space = controller.create_space('Grind Park', '419 Park Avenue South, 2nd Fl', 'New York', 'NY', '10016', '(646) 558 - 3250')
    controller.create_room(space, 'Think Tank', 10, 'WiFi, TV/Monitor, Whiteboard, Coffee/Tea, Filtered Water, Print/Scan/Copy ($), Phone, Wired Internet',15)

    space = controller.create_space('Grind LaSalle', '2 N. LaSalle Street', 'Chicago', 'IL', '60602', '(312) 488 - 4887')
    controller.create_room(space, 'Do Tank', 8, 'WiFi, TV/Monitor, Whiteboard, Wired Internet, Accessibility, Coffee/Tea, Filtered Water, On-site Restaurant, Print/Scan/Copy', 12)
    controller.create_room(space, 'Play Tank', 4, 'WiFi, TV/Monitor, Whiteboard, Accessibility, Coffee/Tea, Filtered Water, Wired Internet, On-site Restaurant, Print/Scan/Copy', 8)
    controller.create_room(space, 'Think Tank', 8, 'WiFi, TV/Monitor, Whiteboard, Wired Internet, Accessibility, Coffee/Tea, Filtered Water, On-site Restaurant, Print/Scan/Copy', 12)
    controller.create_room(space, 'Work Tank', 4, 'WiFi, Whiteboard, Accessibility, Coffee/Tea, Filtered Water, Wired Internet, On-site Restaurant, Print/Scan/Copy', 8)
    user = UserController().get_user(session['email']) if 'email' in session else None
    return redirect('/', user=user)
 
@application.route('/test')
def test():
    controller = SpaceController()
    for space in controller.get_spaces():
        for room in controller.get_rooms(space):
            booking_controller = BookingController()
            booking_controller.create_booking(space, room)
    user = UserController().get_user(session['email']) if 'email' in session else None
    return redirect('/', user=user)

@application.route('/bookings/create', methods=["POST"])
def booking_create_handler():
    print "In booking create"
    form = request.form
    space_id = form['space_id']
    room_id = form['room_id']
    print space_id
    print room_id
    controller = BookingController()
    controller.create_booking(space_id, room_id)
    return redirect("/bookings")

@application.route('/users/signup', methods=["POST"])
def user_signup_handler():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    controller = UserController()
    controller.create_user(email, first_name, last_name)
    session['email'] = email
    recurlyapi = RecurlyAPI()
    recurlyapi.create_account(email, email, first_name, last_name)
    return redirect('/grind')

@application.route('/users/login', methods=["POST"])
def user_login_handler():
    email = request.form['email']
    controller = UserController()
    user = controller.get_user(email)
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

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

