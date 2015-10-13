from flask import Flask, render_template, request, redirect, json, session, jsonify
from db.user_controller import UserController, ThirdPartyUserController
from third_party.cobot import CobotAPI

def auth_handler():
	print 'asdasdasd'
	api = CobotAPI()
	return redirect(api.auth_url())

def callback_handler():
	code = request.args.get('code', None)
	api = CobotAPI()
	access_token = api.get_access_token(code)
	print '#'*80
	print 'access_token'
	print access_token

def create_member_handler():
	api = CobotAPI()
	print api.create_membership('new name', 'some country')['id']

def bookings_handler():
	api = CobotAPI()
	user = UserController().get_item(session['email']) if 'email' in session else None
	third_party_user_controller = ThirdPartyUserController()
	tp_user = third_party_user_controller.get_item(session['email'], 'cobot')
	from_time = '2015-10-13 00:00:00' #datetime.datetime.strptime(date+' '+start, '%Y-%m-%d %H:%M')
	to_time = '2015-10-13 12:00:00' #datetime.datetime.strptime(date+' '+end, '%Y-%m-%d %H:%M')
	bookings = api.list_bookings(tp_user['id'], from_time, to_time)
	print '***Bookings***'
	bookings_list = bookings.json()
	for booking in bookings_list:
		for key in booking:
				print key+' :: '+str(booking[key])
	return render_template("bookings.html", bookings=bookings_list, user=user)

def checkin_handler():
	email = session['email']
	third_party_user = ThirdPartyUserController().get(email=email, network="cobot")
	membership_id = third_party_user['id'] if third_party_user else None
	if membership_id:
		CobotAPI().checkin(membership_id)
	return redirect('/')

def assign_pass_handler():
	email = session['email']
	number = request.form['number']
	third_party_user = ThirdPartyUserController().get(email=email, network="cobot")
	membership_id = third_party_user['id'] if third_party_user else None
	if membership_id:
		CobotAPI().assign_pass(membership_id, number)
	return redirect('/')

def all_checking_handler():
	return CobotAPI().all_checkins()
