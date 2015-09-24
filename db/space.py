from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection

class SpaceController:
	def __init__(self, connection=setup_connection()):
		self.connection = connection
	
	def get_or_create_table(self): #fix this!
		try:
			status = self.connection.describe_table("Spaces")['Table']['TableStatus']
			if status == "ACTIVE":
				return Table("Spaces", connection=self.connection)
		except JSONResponseError:
			return Table.create('Spaces', schema=[HashKey('space_id')], connection=self.connection);
		
	def create_space(self, name):
		table = self.get_or_create_table()
		item = Item(table, data={'space_id': name.lower().replace(' ', '_'), 'name': name})
		item.save()

