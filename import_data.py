from app import db
from models import *

import csv

from datetime import datetime, date


db.drop_all()
db.create_all()

''' Import Clothing Items '''
wardrobe_csv = "/Users/melissagarcia/Desktop/Clothes (Responses) - Wardrobe.csv"
outfit_csv = "/Users/melissagarcia/Desktop/Outfits.csv"

with open(wardrobe_csv, 'r') as infile:
	reader = csv.DictReader(infile)
	for idx,row in enumerate(reader):
		row['price'] = float(row['price'][1:])
		try:
			row['date_bought'] = datetime.strptime(row['date_bought'], '%m/%d/%y')
		except:
			row['date_bought'] = None

		color = row.pop('color')
		pattern = row.pop('pattern')

		# Parse colors
		color = color.split(" and ")

		color_objs = []
		for c in color:
			new_color_obj = Color.query.filter_by(desc=c).first()
			if new_color_obj is None:
				new_color_obj = Color(desc=c)
				db.session.add(new_color_obj)

			color_objs.append(new_color_obj)

		# Parse pattern
		pattern_obj = Pattern.query.filter_by(desc=pattern).first()
		if pattern_obj is None:
			pattern_obj = Pattern(desc=pattern)
			db.session.add(pattern_obj)


		# Parse type
		type_obj = Tag.query.filter_by(desc=row['type']).first()
		if type_obj is None:
			type_obj = Tag(desc=row['type'])
			db.session.add(type_obj)

		db.session.commit()



		row['colors'] = color_objs
		row['pattern'] = pattern_obj
		row['type'] = type_obj

		obj = Item(**row)
		db.session.add(obj)


''' Import logs and outfits '''
with open(outfit_csv, 'r') as infile:
	reader = csv.reader(infile)

	next(reader,None)

	for row in reader:
		date = row[0]

		items = [Item.query.filter_by(desc=d).first() for d in row[1:] if d != '']

		if None in items or len(items) == 0: continue

		outfit = Outfit.getOutfitFromItems(*items)

		if not outfit:
			outfit = Outfit(*items)
			db.session.add(outfit)
			db.session.commit()

		if not Log.query.filter_by(date=date).first():
			log_record = Log(date=date,rating=None,notes=None,occasion=None,outfit_id=outfit.id)
			db.session.add(log_record)
			db.session.commit()


db.session.commit()