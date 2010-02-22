from django.db import models
from composite_pk import composite


class Person(composite.CompositePKModel):
    first_name = models.CharField(max_length=50, primary_key=True)
    last_name = models.CharField(max_length=50, primary_key=True)
    cool = models.BooleanField()

    objects = composite.CompositePKManager()

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Auction(models.Model):
    name = models.CharField(max_length=100)


class Lot(composite.CompositePKModel):
    auction = models.ForeignKey(Auction, primary_key=True)
    lot_number = models.IntegerField(primary_key=True)
    description = models.TextField()

    objects = composite.CompositePKManager()
