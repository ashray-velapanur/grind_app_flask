from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
from boto.dynamodb2.exceptions import JSONResponseError
from db.setup import setup_connection

class DbController(object):
	def __init__(self, table_name, hash_key, range_key=None, index=None, connection=setup_connection()):
		print 'In DbController __init__'
		print index
		self.connection = connection
		self.table_name = table_name
		self.hash_key = hash_key
		self.range_key = range_key
		self.index = index
		self.table = self.get_or_create_table()
		print self.table

	def get_or_create_table(self):
		try:
			tdescr = self.connection.describe_table(self.table_name)
			print "%s" % ((tdescr['Table'])['TableStatus'])
			t = Table(self.table_name, connection=self.connection)
			return t
		except JSONResponseError:
			schema = [HashKey(self.hash_key), RangeKey(self.range_key)] if self.range_key else [HashKey(self.hash_key)]
			global_indexes = []
			if self.index:
				global_indexes = [
					GlobalAllIndex(self.index['name'], 
						parts=[HashKey(self.index['attribute'])],
						throughput={'read': 1,'write': 1}
					)
				]
			return Table.create(self.table_name, schema=schema, global_indexes=global_indexes, connection=self.connection)

	def create_item(self, **kwargs):
		item = Item(self.table, data=kwargs)
		item.save()
		return item
	
	def get_item(self):
		pass

	def all(self):
		return self.get_table().scan()
