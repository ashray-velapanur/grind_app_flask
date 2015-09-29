from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection

def setup_connection():
	return DynamoDBConnection(host='localhost', port=8000, aws_access_key_id='anything', aws_secret_access_key='anything', is_secure=False)
