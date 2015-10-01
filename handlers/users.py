from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController, SlotsController
from db.user_controller import UserController

from third_party.recurly_api import RecurlyAPI

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

def user_login_handler():
    email = request.form['email']
    controller = UserController()
    user = controller.get_item(email)
    if user:
        session['email'] = email
        return redirect('/grind')
    else:
        return jsonify({'success': False, 'message': 'Email not in database'})

def user_logout_handler():
    session.pop("email", None)
    return redirect('/')
