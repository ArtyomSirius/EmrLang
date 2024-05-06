class UseNode:
	def __init__(self, name, connect=None):
		if connect:
			self.connect_name = name

			self.pos_start = self.connect_name.pos_start
			self.pos_end = self.connect_name.pos_end
			self.status = "connect"
		else:
			self.modl_name = name

			self.pos_start = self.modl_name.pos_start
			self.pos_end = self.modl_name.pos_end
			self.status = "modl"

	def __repr__(self):
		return f'{self.modl_name}'