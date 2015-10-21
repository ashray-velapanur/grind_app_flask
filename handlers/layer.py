from flask import request, jsonify
from third_party.layer import generate_identity_token

def get_identity_token():
	user_id = request.args.get('user_id', '')
	nonce = request.args.get('nonce', '')

	if not (user_id and nonce):
		return "Invalid Request."

	# Create the token
	identityToken = generate_identity_token(user_id, nonce)

	# Return our token with a JSON Content-Type
	return jsonify({"identity_token": identityToken})