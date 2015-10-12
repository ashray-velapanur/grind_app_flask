from db.space_controller import SpaceController, RoomController
from db.booking_controller import BookingController, SlotsController
from db.user_controller import UserController, ThirdPartyUserController
import requests
from third_party.recurly_api import RecurlyAPI
from third_party.cobot import CobotAPI
from flask import Flask, render_template, request, redirect, json, session, jsonify

def user_signup_handler():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    controller = UserController()
    user = controller.get_item(email)
    print user
    if not user:
        controller.create_item(email=email, first_name=first_name, last_name=last_name)
        session['email'] = email
        recurlyapi = RecurlyAPI()
        recurlyapi.create_account(email, email, first_name, last_name)
        return redirect('/grind')
    else:
        return redirect('/?message=Email '+email+' is already signed up! Try logging in instead.')

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
    ).json()
    print '#'*80
    print response
    access_token = response['access_token']
    profile_response = requests.get('https://api.linkedin.com/v1/people/~:(id,first-name,last-name,headline,picture-url,industry,summary,specialties,positions:(id,title,summary,start-date,end-date,is-current,company:(id,name,type,size,industry,ticker)),educations:(id,school-name,field-of-study,start-date,end-date,degree,activities,notes),associations,interests,num-recommenders,date-of-birth,publications:(id,title,publisher:(name),authors:(id,name),date,url,summary),patents:(id,title,summary,number,status:(id,name),office:(name),inventors:(id,name),date,url),languages:(id,language:(name),proficiency:(level,name)),skills:(id,skill:(name)),certifications:(id,name,authority:(name),number,start-date,end-date),courses:(id,name,number),recommendations-received:(id,recommendation-type,recommendation-text,recommender),honors-awards,three-current-positions,three-past-positions,volunteer,email-address)?format=json', headers={"Authorization" : "Bearer "+access_token}, verify = False)
    profile = profile_response.json()
    email = profile['emailAddress']
    first_name = profile['firstName']
    last_name = profile['lastName']
    user = create_user(email, first_name, last_name, industry=profile['industry'])
    create_third_party_user(user, 'linkedin', access_token)
    session['email'] = user['email']
    return redirect('/')

def create_user(email, first_name, last_name, **kwargs):
    user_controller = UserController()
    user = user_controller.get_item(email)
    if not user:
        user = user_controller.create_item(email=email, first_name=first_name, last_name=last_name, **kwargs)
        RecurlyAPI().create_account(email, email, first_name, last_name)
        CobotAPI().create_membership(("%s %s")%(first_name, last_name), 'USA')
    return user

def create_third_party_user(user, network, access_token, **kwargs):
    third_party_user_controller = ThirdPartyUserController()
    tp_user = third_party_user_controller.get_item(user['email'], network)
    if not tp_user:
        third_party_user = third_party_user_controller.create_item(email=user['email'], network=network, access_token=access_token, **kwargs)

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
