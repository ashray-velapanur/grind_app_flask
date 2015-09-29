from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection
from db.db_controller import DbController

class BookingController(DbController):
	def __init__(self):
		DbController.__init__(self, "Bookings", "space_id", range_key="room_id")
	
	def get_items(self):
		return self.get_table().scan()
