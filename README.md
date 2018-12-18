django-compositepk
==================

A Django application that provides a ``CompositePKModel``, allowing for basic
retrieval and saving of models with composite keys.

It is limited to the above tasks, and any use of the model past this is not
guaranteed to work.


Example usage
=============

A model with composite PK should look something like this:

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


Cloned from the original repo https://bitbucket.org/smileychris/django-compositepk
