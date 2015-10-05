from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController, SlotsController
from db.user_controller import UserController
from boto.dynamodb2.exceptions import ConditionalCheckFailedException
import requests
from third_party.recurly_api import RecurlyAPI
from flask import Flask, render_template, request, redirect, json, session, jsonify

def user_signup_handler():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    controller = UserController()
    controller.create_item(email=email, first_name=first_name, last_name=last_name)
    session['email'] = email
    recurlyapi = RecurlyAPI()
    try:
        recurlyapi.create_account(email, email, first_name, last_name)
    except ConditionalCheckFailedException:
        pass
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

def linkedin_login_handler():
    print 'In linkedin_login_handler'
    values = {'grant_type':'authorization_code',
            'code':request.args.get('code',''),
            'redirect_uri':'https://oscarosl-test.appspot.com/linkedin/callback',
            'client_id':'75z1lnoajxsagn',
            'client_secret':'ks6phGNwAUQXUo9J'}
    url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    response = requests.post(
        url,
        verify = False,  # Verify SSL certificate,
        data = values
    )
    at = response.json()
    print at
    profile_response = requests.get('https://api.linkedin.com/v1/people/~:(id,first-name,last-name,headline,picture-url,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer,email-address)?format=json', headers={"Authorization" : "Bearer "+at['access_token']}, verify = False)
    profile = profile_response.json()
    email = profile['emailAddress']
    first_name = profile['firstName']
    last_name = profile['lastName']
    controller = UserController()
    user = controller.get_item(email)
    print user
    if not user:
        user = controller.create_item(email=email, first_name=first_name, last_name=last_name, access_token=at['access_token'], industry=profile['industry'])
        print 'User Created'
        recurlyapi = RecurlyAPI()
        try:
            recurlyapi.create_account(email, email, first_name, last_name)
        except ConditionalCheckFailedException:
            pass
    session['email'] = email
    return redirect('/')

def get_users_for_industry():
    industry = request.form['industry']
    controller = UserController()
    industry_users = controller.get_items_for_industry(industry)
    print industry_users
    users = []
    for user in industry_users:
        print user['first_name'] + ' , ' + user['last_name']
        users.append(user['first_name'] + ' , ' + user['last_name'])
    return jsonify({'Users belonging to '+industry:users})
