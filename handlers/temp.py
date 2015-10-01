from flask import Flask, render_template, request, redirect, json, session, jsonify

from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController, SlotsController
from db.user_controller import UserController
from db.setup import setup_connection
from third_party.recurly_api import RecurlyAPI
import recurly
from recurly import Account, Transaction, BillingInfo

import datetime


recurly.SUBDOMAIN = 'beagles'
recurly.API_KEY = '413a664bcd874f4fb2b17b68dd1cbf8c'
recurly.DEFAULT_CURRENCY = 'USD'

def index():
    print 'In index page'
    userController = UserController()
    user = userController.get_item(session['email']) if 'email' in session else None
    if not user:
        return render_template("index.html", user=user)
    else:
        return redirect('/grind')

def grind():
    print 'In grind page'
    controller = SpaceController()
    spaces = controller.get_items()
    userController = UserController()
    user = userController.get_item(session['email']) if 'email' in session else None
    return render_template("grind.html", spaces=spaces, user=user)

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
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    print date
    return render_template("book.html", space=space, room=room, user=user, date=date)

def bookings():
    print 'In bookings page'
    controller = BookingController()
    bookings = controller.get_items()
    user = UserController().get_item(session['email']) if 'email' in session else None
    return render_template("bookings.html", bookings=bookings, user=user)


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

def create_event_page_handler():
    print 'In create event page'
    userController = UserController()
    user = userController.get_item(session['email']) if 'email' in session else None
    spaceController = SpaceController()
    spaces = spaceController.get_items()
    return render_template("create_event.html", user=user, spaces=spaces)
