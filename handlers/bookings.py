from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController, SlotsController
from db.user_controller import UserController

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
        if transaction.status == 'success':
            create_booking(type='room', space_id=space_id, room_id=room_id, date=date, start_time=start, end_time=end)
        return redirect("/bookings")

def booking_availability_handler():
    form = request.form
    space_id = form['space_id']
    room_id = form['room_id']
    date = form['date']
    start = form['start']
    end = form['end']
    available = check_availability(space_id=space_id, room_id=room_id, date=date, start_time=start, end_time=end)
    return jsonify({'available': available})
