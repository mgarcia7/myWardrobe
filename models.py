from app import db
from datetime import datetime

import uuid

outfit_items = db.Table('outfit_items',
	db.Column('item_id', db.String(36), db.ForeignKey('item.id')),
	db.Column('outfit_id', db.String(36), db.ForeignKey('outfit.id')),
	db.PrimaryKeyConstraint('item_id', 'outfit_id'))

color_items = db.Table('color_items',
	db.Column('item_id', db.String(36), db.ForeignKey('item.id')),
	db.Column('color_id', db.String(36), db.ForeignKey('color.id')),
	db.PrimaryKeyConstraint('item_id','color_id'))

pattern_items = db.Table('pattern_items',
	db.Column('item_id', db.String(36), db.ForeignKey('item.id')),
	db.Column('pattern_id', db.String(36), db.ForeignKey('pattern.id')),
	db.PrimaryKeyConstraint('item_id','pattern_id'))

tag_items = db.Table('tag_items',
	db.Column('item_id', db.String(36), db.ForeignKey('item.id')),
	db.Column('tag_id', db.String(36), db.ForeignKey('tag.id')),
	db.PrimaryKeyConstraint('item_id','tag_id'))

class Item(db.Model):
	id = db.Column(db.String(36), primary_key=True)
	category = db.Column(db.String(7))
	desc = db.Column(db.String(120), unique=True) 
	date_bought = db.Column(db.DateTime)
	price = db.Column(db.Float)
	store_bought = db.Column(db.String(50))
	size = db.Column(db.String(20))

	# right side entity = the other class that you're getting info from
	# left side entity = parent (class you're currently defining relationship for)
	# backref = how relationship will be accessed from right side entity
	# secondary = association table
	# lazy=dynamic returns query obj vs the actual info

	outfits_in = db.relationship("Outfit", secondary=outfit_items,
		backref=db.backref('items', lazy='dynamic'), lazy='dynamic')

	colors = db.relationship("Color", secondary=color_items,
		backref=db.backref('items', lazy='dynamic'), lazy='dynamic')

	patterns = db.relationship("Pattern", secondary=pattern_items,
		backref=db.backref('items', lazy='dynamic'), lazy='dynamic')

	tags = db.relationship("Tag", secondary=tag_items,
		backref=db.backref('items', lazy='dynamic'), lazy='dynamic')

	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())

		self.addColor(kwargs.pop('colors'))
		self.addPattern(kwargs.pop('pattern'))
		self.addTag(kwargs.pop('type'))


		self.__dict__.update(kwargs)


	def __repr__(self):
		return '<Item Desc %r>' % self.desc

	def addColor(self, color):
		for c in color:
			self.colors.append(c)

		return self

	def addPattern(self, pattern):
		self.patterns.append(pattern)
		return self

	def addTag(self, tag):
		self.tags.append(tag)
		return self

class Log(db.Model):
	id = db.Column(db.String(36), primary_key=True)
	rating = db.Column(db.Integer)
	date = db.Column(db.DateTime)
	notes = db.Column(db.String(150))
	occasion = db.Column(db.String(50)) 

	outfit_id = db.Column(db.String(36), db.ForeignKey('outfit.id'))

	# backref fields = outfit

	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self.__dict__.update(kwargs)

	def __repr__(self):
		return '<Date %r>' % self.date


class Outfit(db.Model):
	id = db.Column(db.String(36), primary_key=True)

	worn = db.relationship("Log", backref=db.backref('outfit', lazy='joined'), lazy='dynamic')
	# backref fields = items

	def __init__(self, *argv):
		self.id = str(uuid.uuid4())
		for arg in argv:
			self.items.append(arg)

	def __repr__(self):
		item_string = ','.join([it.desc for it in self.items])
		return ' '.join(['<Item List ', item_string,' >'])

	@staticmethod
	def getOutfitFromItems(*args):
		outfits = set(Outfit.query.filter(Outfit.items.any(id=args[0].id)).all())
		for idx,it in enumerate(args[1:]):
			potential = set(Outfit.query.filter(Outfit.items.any(id=it.id)).all())
			outfits = potential & outfits

		return list(outfits)[0] if outfits else None


class Color(db.Model):
	id = db.Column(db.String(36), primary_key=True)
	desc = db.Column(db.String(120), unique=True) 
	# backref field = items

	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self.__dict__.update(kwargs)

	def __repr__(self):
		return '<Item Desc %r>' % self.desc

class Pattern(db.Model):
	id = db.Column(db.String(36), primary_key=True)
	desc = db.Column(db.String(120), unique=True) 
	# backref field = items

	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self.__dict__.update(kwargs)

	def __repr__(self):
		return '<Item Desc %r>' % self.desc

class Tag(db.Model):
	id = db.Column(db.String(36), primary_key=True)
	desc = db.Column(db.String(120), unique=True) 
	# backref field = items

	def __init__(self, **kwargs):
		self.id = str(uuid.uuid4())
		self.__dict__.update(kwargs)

	def __repr__(self):
		return '<Item Desc %r>' % self.desc


