from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection

class SpaceController:
	def __init__(self, connection=setup_connection()):
		self.connection = connection
	
	def get_or_create_space(self): #fix this!
		try:
			status = self.connection.describe_table("Spaces")['Table']['TableStatus']
			if status == "ACTIVE":
				return Table("Spaces", connection=self.connection)
		except JSONResponseError:
			return Table.create('Spaces', schema=[HashKey('space_id')], connection=self.connection);
		
	def get_or_create_room(self): #fix this!
		try:
			status = self.connection.describe_table("Rooms")['Table']['TableStatus']
			if status == "ACTIVE":
				return Table("Rooms", connection=self.connection)
		except JSONResponseError:
			return Table.create('Rooms', schema=[HashKey('space_id'), RangeKey('room_id')], connection=self.connection);

	def create_space(self, name):
		table = self.get_or_create_space()
		item = Item(table, data={'space_id': name.lower().replace(' ', '_'), 'name': name})
		item.save()

	def create_room(self, space, name, price):
		table = self.get_or_create_room()
		space_id = space['space_id']
		item = Item(table, data={'space_id': space_id, 'room_id': name.lower().replace(' ', '_'), 'name': name, 'price': price})
		item.save()

