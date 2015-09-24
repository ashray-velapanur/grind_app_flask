from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.layer1 import DynamoDBConnection

def setup_connection():
	return DynamoDBConnection(host='localhost', port=8000, aws_access_key_id='anything', aws_secret_access_key='anything', is_secure=False)

'''
def setup_test_data():
	connection = setup_connection()
	test_table = Table.create('test_table', schema=[HashKey('key')], connection=connection);
	test_item = Item(test_table, data={'key': 'this_key', 'field_1': 'field_1_data'})
	test_item.save()

def get_data():
	connection = setup_connection()
	table = Table('test_table', connection=connection)
	item = table.get_item(key='this_key')
	return item
'''