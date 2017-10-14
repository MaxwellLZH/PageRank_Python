import os
import sys


class Page:


	def __init__(self, p_id):
		self._id = str(p_id)
		self.weight = 1
		self.n_outlink = 0
		self.n_inlink = 0
		self.outlinks = set()
		self.inlinks = set()

	def add_outlink(self, link):
		if not isinstance(link, BaseLink):
			raise ValueError('Can only add objects that are subclasses of BaseLink.')
		self.outlinks.add(link)
		self.n_outlink += 1

	def add_inlink(self, link):
		if not isinstance(link, BaseLink):
			raise ValueError('Can only add objects that are subclasses of BaseLink.')
		self.inlinks.add(link)
		self.n_inlink += 1

	def __repr__(self):
		return '<Page: {}, n_out: {}, n_in: {}, weight: {}>'.format(self._id, self.n_outlink, self.n_inlink, self.weight)

	def __eq__(self, other):
		return self._id == other._id

	def __hash__(self):
		# just so the Page class can be stored in a set
		return hash(self._id)

	@property
	def id(self):
		return self._id

	@property
	def weight(self):
		return self._weight

	@weight.setter
	def weight(self, value):
		if value < 0:
			raise ValueError("Page weight should be a non-negative number.")
		else:
			self._weight = value



class BaseLink:
	"""
	Base class for Link and Teleporting
	"""

	def __init__(self, from_page, to_page):
		attrs = ['weight', 'id', 'n_inlink', 'n_outlink']
		self._from = _hasattrs(from_page, attrs)
		self._to = _hasattrs(to_page, attrs)
		self.weight = 0

	def update_weight(self):
		raise NotImplementedError('Base classes should implement this method.')

	@property
	def start(self):
		return self._from

	@property
	def end(self):
		return self._to

	@property
	def id(self):
		return self._from.id + '-' + self._other.id

	def __eq__(self, other):
		return self.id == other.id

	def __hash__(self):
		return hash(self._from.id + self._to.id)


class Link(BaseLink):
	"""
	Link is an page walk that follows the outlink
	"""
	def update_weight(self):
		"""
		The weight of a Link equals to from_page.weight / from_page.n_outlink
		Returns:
			The absolute value of the incremental amount.
		"""
		old_weight = self.weight
		if self._from.n_outlink == 0:
			self.weight = 0
		else:
			self.weight = self._from.weight / self._from.n_outlink
		return abs(old_weight - self.weight)



class Graph:

	def __init__(self, nodes, edges):
		"""Both nodes and edges are set"""
		self._nodes = nodes
		self._edges = edges

	def get_node(self, n_id):
		# TODO: need a better structure
		# same with get_edge
		for node in self._nodes:
			if node.id == n_id:
				return node
		else:
			return None

	def get_edge(self, e_id):
		for edge in self._edges:
			if edge.id == e_id:
				return edge
		else:
			return None

	def add_node(self, node):
		"""if the node already exists return exising node"""
		if node not in self._nodes:
			self._nodes.add(node)
			return node
		else:
			return self.get_node(node.id)

	def add_edge(self, edge):
		"""if the edge already exists return existing edge"""
		if not edge in self._edges:
			self._edges.add(edge)
			return edge
		else:
			self.get_edge(edge.id)





def _hasattrs(obj, attrs):
	if not all([hasattr(obj, attr) for attr in attrs]):
		raise ValueError('The object doesn\'t implement all the attributes: {}'.format(attrs))
	return obj