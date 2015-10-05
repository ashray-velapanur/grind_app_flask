from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError, ItemNotFound
from db.setup import setup_connection
from db.db_controller import DbController

class UserController(DbController):
	def __init__(self):
		DbController.__init__(self, "Users", "email", index = {'name':'IndustryIndex', 'attribute':'industry'})

	def get_item(self, email):
		try:
			res = self.table.query_2(email__eq=email)
			return res.next() if res else None
		except (ItemNotFound, StopIteration):
			return None

	def get_items_for_industry(self, industry):
		try:
			return self.table.query_2(industry__eq=industry, index='IndustryIndex')
		except (ItemNotFound):
			return None