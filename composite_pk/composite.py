"""
This module provides a ``CompositePKModel`` which allows for basic retrieval
and saving of models with composite keys.

It is limited to the above tasks, and any use of the model past this is not
guaranteed to work.

A model with composite PK should look something like this::

    from composite_pk import composite

    class Lot(composite.CompositePKModel):
        auction = models.ForeignKey(Auction, primary_key=True)
        lot_number = models.IntegerField(primary_key=True)
        objects = composite.CompositePKManager()

So it must:

    * subclass the ``CompositePKModel``,

    * have two or more fields which set the ``primary_key`` attribute to True,
      and

    * use the ``CompositePKManager`` as the initial manager.

"""
from django.db import models
from django.db.models.base import ModelBase


class CompositePKModelBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        cls = super(CompositePKModelBase, cls).__new__(cls, name, bases, attrs)
        if hasattr(cls, '_meta'):
            if hasattr(cls, '_primary_keys'):
                cls._primary_keys = cls._primary_keys[:]
            else:
                cls._primary_keys = []
            for field in cls._meta.fields:
                if not field.primary_key:
                    continue
                field.primary_key = False
                cls._primary_keys.append(field.name)
            # While setting the meta PK to none seems like a good idea, it is
            # necessary in a lot of places, hence why the following line is
            # commented.
            #cls._meta.pk = None
        return cls


class CompositePKModel(models.Model):
    __metaclass__ = CompositePKModelBase

    class Meta:
        abstract = True

    def _get_pk_val(self, *args, **kwargs):
        if self._primary_keys:
            pk = {}
            for field_name in self._primary_keys:
                attr = self._meta.get_field(field_name).attname
                pk[field_name] = getattr(self, attr)
            return pk
        return super(CompositePKModel, self)._get_pk_val(*args, **kwargs)

    def _set_pk_val(self, *args, **kwargs):
        return super(CompositePKModel, self)._set_pk_val(*args, **kwargs)

    pk = property(_get_pk_val, _set_pk_val)


class CompositePKQuerySet(models.query.QuerySet):

    def _expand_pk(self, kwargs):
        """
        Expand a composite primary key into the fields it represents into a
        kwargs dictionary.
        
        The dictionary is modified inline rather than a modified copy returned.
        """
        for key, value in kwargs.items():
            if '__' in key:
                field, remainder = key.split('__', 1)
            else:
                field, remainder = key, ''
            if field != 'pk':
                continue
            if isinstance(value, dict):
                del kwargs['pk']
                for pk_field in self.model._primary_keys:
                    kwargs['%s%s' % (pk_field, remainder)] = value[pk_field]


    def filter(self, *args, **kwargs):
        """
        Returns a new QuerySet instance with the args ANDed to the existing
        set.
        """
        self._expand_pk(kwargs)
        return self._filter_or_exclude(False, *args, **kwargs)

    def exclude(self, *args, **kwargs):
        """
        Returns a new QuerySet instance with NOT (args) ANDed to the existing
        set.
        """
        self._expand_pk(kwargs)
        return self._filter_or_exclude(True, *args, **kwargs)


class CompositePKManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        """Returns a new QuerySet object.  Subclasses can override this method
        to easily customize the behavior of the Manager.
        """
        return CompositePKQuerySet(self.model, using=self._db)
