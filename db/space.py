from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection

class SpaceController:
	def __init__(self, connection=setup_connection()):
		self.connection = connection
	
	def get_spaces_table(self):
		return Table("Spaces", connection=self.connection)

	def get_rooms_table(self):
		return Table("Rooms", connection=self.connection)

	def get_or_create_space(self): #fix this!
		try:
			status = self.connection.describe_table("Spaces")['Table']['TableStatus']
			if status == "ACTIVE":
				return self.get_spaces_table()
		except JSONResponseError:
			return Table.create('Spaces', schema=[HashKey('space_id')], connection=self.connection);
		
	def get_or_create_room(self): #fix this!
		try:
			status = self.connection.describe_table("Rooms")['Table']['TableStatus']
			if status == "ACTIVE":
				return self.get_rooms_table()
		except JSONResponseError:
			return Table.create('Rooms', schema=[HashKey('space_id'), RangeKey('room_id')], connection=self.connection);

	def create_space(self, name, address, city, state, zip, phone):
		table = self.get_or_create_space()
		item = Item(table, data={'space_id': name.lower().replace(' ', '_'), 'name': name, 'address': address, 'city': city, 'state': state, 'zip': zip, 'phone': phone})
		item.save()
		return item

	def create_room(self, space, name, size, amenities_list, price):
		table = self.get_or_create_room()
		space_id = space['space_id']
		item = Item(table, data={'space_id': space_id, 'room_id': name.lower().replace(' ', '_'), 'name': name, 'size': size, 'amenities': amenities_list, 'price': price})
		item.save()
		return item

	def get_spaces(self, space_id=None):
		if space_id:
			return self.get_spaces_table().query_2(space_id__eq=space_id).next()
		else:
			return self.get_spaces_table().scan()

	def get_rooms(self, space):
		return self.get_rooms_table().query_2(space_id__eq=space['space_id'])



