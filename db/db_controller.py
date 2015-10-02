from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection

class DbController(object):
	def __init__(self, table_name, hash_key, range_key=None, connection=setup_connection()):
		self.connection = connection
		self.table_name = table_name
		self.hash_key = hash_key
		self.range_key = range_key

	def get_table(self):
		return Table(self.table_name, connection=self.connection)

	def get_or_create_table(self):
		try:
			self.connection.describe_table(self.table_name)
			return self.get_table()
		except JSONResponseError:
			schema = [HashKey(self.hash_key), RangeKey(self.range_key)] if self.range_key else [HashKey(self.hash_key)]
			return Table.create(self.table_name, schema=schema, connection=self.connection);

	def create_item(self, **kwargs):
		table = self.get_or_create_table()
		item = Item(table, data=kwargs)
		item.save()
		return item
	
	def get_item(self):
		pass

	def all(self):
		return self.get_table().scan()
