from flask import Flask, render_template, request, redirect, json, session, jsonify

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
