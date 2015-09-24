from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection

class BookingController:
	def __init__(self, connection=setup_connection()):
		self.connection = connection
	
	def get_bookings_table(self):
		return Table("Bookings", connection=self.connection)

	def get_or_create_booking(self): #fix this!
		try:
			status = self.connection.describe_table("Bookings")['Table']['TableStatus']
			if status == "ACTIVE":
				return self.get_bookings_table()
		except JSONResponseError:
			return Table.create('Bookings', schema=[HashKey('space_id'), RangeKey('room_id')], connection=self.connection);

	def create_booking(self, space_id, room_id):
		table = self.get_or_create_booking()
		item = Item(table, data={'space_id': space_id, 'room_id': room_id})
		item.save()

	def get_bookings(self):
		return self.get_bookings_table().scan()
