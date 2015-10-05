from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError, ItemNotFound
from db.setup import setup_connection
from db.db_controller import DbController

class BookingController(DbController):
	def __init__(self):
		DbController.__init__(self, "Bookings", "booking_id", range_key="start_time")
	
	def get_items(self):
		return self.table.scan()

	def delete_item(self, boking_id, start_time):
		table = self.get_table()
		try:
			return table.delete_item(booking_id__eq=booking_id, start_time__eq=start_time)
		except (ItemNotFound):
			return None

class SlotsController(DbController):
	def __init__(self):
		DbController.__init__(self, "Slots", "slot_id", range_key="start_time")

	def get_item(self, slot_id, start_time):
		try:
			return self.table.query_2(slot_id__eq=slot_id, start_time__eq=start_time).next()
		except (ItemNotFound, StopIteration):
			return None

	def delete_item(self, slot_id, start_time):
		table = self.get_table()
		try:
			return table.delete_item(slot_id__eq=slot_id, start_time__eq=start_time)
		except (ItemNotFound):
			return None
