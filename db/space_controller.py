from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError, ItemNotFound
from db.setup import setup_connection
from db.db_controller import DbController

class SpaceController(DbController):
	def __init__(self):
		DbController.__init__(self, "Spaces", "space_id")

	def get_item(self, space_id):
		table = self.get_table()
		try:
			return table.query_2(space_id__eq=space_id).next()
		except ItemNotFound:
			return None

	def get_items(self):
		return self.get_table().scan()

class RoomController(DbController):
	def __init__(self):
		DbController.__init__(self, "Rooms", "space_id", range_key="room_id")

	def get_item(self, space_id, room_id):
		table = self.get_table()
		try:
			return table.query_2(space_id__eq=space_id, room_id__eq=room_id).next()
		except ItemNotFound:
			return None

	def get_items(self, space_id, room_id=None):
		return self.get_table().query_2(space_id__eq=space_id)
