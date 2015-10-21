from flask import Flask, render_template, request, redirect, json, session, jsonify
import requests

def linkedin_auth_handler():
	access_token = request.args.get('access_token','')
	linkedin_id = request.args.get('id','')
	profile_response = requests.get('https://api.linkedin.com/v1/people/~:(id,email-address)?format=json', headers={"Authorization" : "Bearer "+access_token}, verify = False)
	profile = profile_response.json()
	for key in profile:
		print key, profile[key]
	if 'id' in profile:
		profile_id = profile['id']
		if profile_id==linkedin_id:
			profile_email = profile['emailAddress']
			session["email"] = profile_email
			return jsonify({'success':True, 'email': profile_email})
		else:
			return jsonify({'success':False,'error':'LinkedIn ID could not be verified'})
	elif 'message' in profile:
		return jsonify({'success':False,'error':profile['message']})

def logout():
	session.pop("email", None)
	return redirect('/')