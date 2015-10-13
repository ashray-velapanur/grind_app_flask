from flask import render_template, request, redirect, json, session, jsonify
import requests
from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController, SlotsController
from db.user_controller import UserController, ThirdPartyUserController
import datetime, recurly
from recurly import Account, Transaction, BillingInfo
from third_party.cobot import CobotAPI

recurly.SUBDOMAIN = 'beagles'
recurly.API_KEY = '413a664bcd874f4fb2b17b68dd1cbf8c'
recurly.DEFAULT_CURRENCY = 'USD'

def create_booking(type, space_id, room_id, date, start_time, end_time):
    bookings = BookingController()
    slots = SlotsController()
    start = datetime.datetime.strptime(date+' '+start_time, '%Y-%m-%d %H:%M')
    end = datetime.datetime.strptime(date+' '+end_time, '%Y-%m-%d %H:%M')
    print start, end
    booking_id = ('%s %s'%(space_id, room_id)).strip()
    bookings.create_item(type=type, booking_id=booking_id, start_time=start.strftime('%Y-%m-%d %H:%M'), end_time=end.strftime('%Y-%m-%d %H:%M'))
    while start < end:
        time = start.strftime('%Y-%m-%d %H:%M')
        slot_id = ('%s %s'%(space_id, room_id)).strip()
        start = start + datetime.timedelta(hours=1)
        slots.create_item(slot_id=slot_id, start_time=time)

def delete_booking(type, space_id, room_id, date, start_time, end_time):
    bookings = BookingController()
    slots = SlotsController()
    start = datetime.datetime.strptime(date+' '+start_time, '%Y-%m-%d %H:%M')
    end = datetime.datetime.strptime(date+' '+end_time, '%Y-%m-%d %H:%M')
    print start, end
    booking_id = ('%s %s'%(space_id, room_id)).strip()
    bookings.delete_item(type=type, booking_id=booking_id, start_time=start.strftime('%Y-%m-%d %H:%M'))
    while start < end:
        time = start.strftime('%Y-%m-%d %H:%M')
        slot_id = ('%s %s'%(space_id, room_id)).strip()
        start = start + datetime.timedelta(hours=1)
        slots.delete_item(slot_id=slot_id, start_time=time)

def check_availability(space_id, room_id, date, start_time, end_time):
    bookings = BookingController()
    slots = SlotsController()
    start = datetime.datetime.strptime(date+' '+start_time, '%Y-%m-%d %H:%M')
    end = datetime.datetime.strptime(date+' '+end_time, '%Y-%m-%d %H:%M')
    slot_id = ('%s %s'%(space_id, room_id)).strip()
    while start < end:
        time = start.strftime('%Y-%m-%d %H:%M')
        start = start + datetime.timedelta(hours=1)
        slot = slots.get_item(slot_id=slot_id, start_time=time)
        if slot:
            return False
    return True

def booking_create_web_handler():
    booking_create_handler()
    return redirect("/bookings")

def booking_create_handler():
    print "In booking create"
    user = UserController().get_item(session['email']) if 'email' in session else None
    if user:
        form = request.form
        space_id = form['space_id']
        room_id = form['room_id']
        date = form['date']
        start = form['start']
        end = form['end']
        print date, start, end
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
        success = False
        if transaction.status == 'success':
            third_party_user_controller = ThirdPartyUserController()
            tp_user = third_party_user_controller.get_item(user['email'], 'cobot')
            from_time = datetime.datetime.strptime(date+' '+start, '%Y-%m-%d %H:%M')
            to_time = datetime.datetime.strptime(date+' '+end, '%Y-%m-%d %H:%M')
            print from_time, to_time
            type='room'
            api = CobotAPI()
            result = api.create_booking(tp_user['id'], from_time, to_time, type+'_'+space_id+'_'+room_id+'_'+str(from_time)+'_'+str(to_time))
            print result
            #create_booking(type='room', space_id=space_id, room_id=room_id, date=date, start_time=start, end_time=end)
            success = True
            bookings = api.list_bookings(tp_user['id'], from_time, to_time)
            print bookings
        return json.dumps({'success':success})

def booking_availability_handler():
    form = request.form
    space_id = room_id = date = start = end = ''
    space_id = form['space_id']
    if 'room_id' in form:
        room_id = form['room_id']
    date = form['date']
    start = form['start']
    end = form['end']
    available = check_availability(space_id=space_id, room_id=room_id, date=date, start_time=start, end_time=end)
    return jsonify({'available': available})


def create_event_handler():
    create_event()
    return redirect('/')

def create_event():
    form = request.form
    print form['date']
    print form['start']+':00Z'
    print form['end']+':00Z'
    space_id = form['space_id']
    date = form['date']
    start = form['start']
    end = form['end']
    create_booking(type='space', space_id=space_id, room_id="", date=date, start_time=start, end_time=end)
    response = requests.post(
        "https://www.eventbriteapi.com/v3/events/",
        headers = {
            "Authorization": "Bearer WWVNO7GS2EN36S5JDLS3",
        },
        verify = False,  # Verify SSL certificate,
        data = {'event.name.html':form['name'],
                'event.start.utc':form['date']+'T'+form['start']+':00Z',
                'event.start.timezone':'America/New_York',
                "event.end.utc":form['date']+'T'+form['end']+':00Z',
                "event.end.timezone": "America/New_York",
                "event.currency": "USD"
                }
    )
    print response.json()
    return response.json()

def list_event_handler():
    events = get_events()
    return render_template("events.html", events=events)

def get_events_handler():
    events = get_events()
    return json.dumps({'events':events})

def get_events():
    response = requests.get(
        "https://www.eventbriteapi.com/v3/users/115769153821/owned_events/",
        headers = {
            "Authorization": "Bearer WWVNO7GS2EN36S5JDLS3",
        },
        verify = False,  # Verify SSL certificate,
        data = {'order_by':"start_asc"}
    )
    events = response.json()['events']
    return events