from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError, ItemNotFound
from db.setup import setup_connection
from db.db_controller import DbController

class UserController(DbController):
	def __init__(self):
		DbController.__init__(self, "Users", "email")

	def get_item(self, email):
		table = self.get_table()
		try:
			return table.query_2(email__eq=email).next()
		except ItemNotFound:
			return None