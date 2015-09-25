from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError, ItemNotFound
from db.setup import setup_connection

class UserController:
	def __init__(self, connection=setup_connection()):
		self.connection = connection
	
	def get_users_table(self):
		return Table("Users", connection=self.connection)

	def get_or_create_user(self): #fix this!
		try:
			status = self.connection.describe_table("Users")['Table']['TableStatus']
			if status == "ACTIVE":
				return self.get_users_table()
		except JSONResponseError:
			return Table.create('Users', schema=[HashKey('email')], connection=self.connection);

	def create_user(self, email, name):
		table = self.get_or_create_user()
		item = Item(table, data={'email': email, 'name': name})
		item.save()
		return item

	def get_user(self, email):
		table = self.get_users_table()
		try:
			return table.get_item(email=email)
		except ItemNotFound:
			return None
