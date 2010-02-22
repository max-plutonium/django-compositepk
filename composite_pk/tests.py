"""
>>> from composite_pk.models import *

>>> joe = Person(first_name='Joe', last_name='Bloggs')
>>> joe_u = Person(first_name='Joe', last_name='User')
>>> jane = Person(first_name='Jane', last_name='Bloggs')


# Try saving these fields.

>>> joe.save()
>>> joe_u.save()
>>> jane.save()

>>> Person.objects.count()
3


# Check the primary keys

>>> joe.pk
{'first_name': 'Joe', 'last_name': 'Bloggs'}

>>> joe_u.pk
{'first_name': 'Joe', 'last_name': 'User'}

>>> jane.pk
{'first_name': 'Jane', 'last_name': 'Bloggs'}


# Try retrieving first / last names to ensure that everything was saved
# correctly.

>>> first_names = Person.objects.values_list('first_name', flat=True)
>>> last_names = Person.objects.values_list('last_name', flat=True)

>>> sorted(first_names)
[u'Jane', u'Joe', u'Joe']

>>> sorted(last_names)
[u'Bloggs', u'Bloggs', u'User']


# Now try retrieving the individual people.

>>> unicode(Person.objects.get(last_name='User'))
u'Joe User'

>>> unicode(Person.objects.get(first_name='Joe', last_name='Bloggs'))
u'Joe Bloggs'

>>> unicode(Person.objects.get(first_name='Jane'))
u'Jane Bloggs'


# To use a ``pk`` filter, you need to pass a dictionary containing all the
# primary keys.

>>> unicode(Person.objects.get(pk={'first_name': 'Joe', 'last_name': 'Bloggs'}))
u'Joe Bloggs'


# Foreign keys can be used as part of the composite primary key.

>>> a = Auction.objects.create(name='Art auction')  
>>> b = Auction.objects.create(name='Bike auction')  
>>> lot1 = Lot.objects.create(auction=a, lot_number=1, description='Monet')
>>> lot2 = Lot.objects.create(auction=a, lot_number=2, description='Picasso')
>>> lot3 = Lot.objects.create(auction=b, lot_number=1,
...                           description='Old Raleigh')


# The primary keys use the field name as opposed to the attribute name.

>>> bike = Lot.objects.get(auction=b)
>>> bike.pk
{'auction': 2, 'lot_number': 1}


# Ensure saving an existing instance works correctly.

>>> bike.description = 'Vintage Raleigh'
>>> bike.save()
>>> Lot.objects.count()
3
>>> Lot.objects.values_list('description', flat=True)
[u'Monet', u'Picasso', u'Vintage Raleigh']

"""