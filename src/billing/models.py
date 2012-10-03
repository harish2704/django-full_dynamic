from django.db import models
from eav.models import BaseEntity,BaseAttribute,BaseChoice,BaseSchema
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

class Entity(models.Model):
    """docstring"""
    title = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        app_label = 'billing'
        # abstract = True


class Schema(BaseSchema):
    entity = models.ManyToManyField(Entity)
    
    class Meta:
        app_label = 'billing'


class Choice(BaseChoice):
    schema = models.ForeignKey(Schema, related_name='choices')
    
    class Meta:
        app_label = 'billing'


class Attribute(BaseAttribute):
    schema = models.ForeignKey(Schema, related_name='attrs')
    choice = models.ForeignKey(Choice, blank=True, null=True )
    
    class Meta:
        app_label = 'billing'


class Thread(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        app_label = 'billing'


class Customer(models.Model):
    """docstring"""
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50,unique=True)
    
    class Meta:
        app_label = 'billing'


class Order(models.Model):
    """An Order representing a complete order"""
    date = models.DateField(auto_now_add=True, auto_now=True, blank=True,)
    customer = models.ForeignKey(Customer,)
    deliver = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'billing'


class OrderedItem(models.Model):
    """An ordered item (item x quantity)"""
    
    order = models.ForeignKey(Order)
    quantity = models.IntegerField()
    # note = models.CharField(max_length=255)

    class Meta:
        app_label = 'billing'


class Item(BaseEntity):
    """docstring"""
    
    ordered_item = models.ForeignKey(OrderedItem,)
    entity = models.ForeignKey(Entity)
    
    @classmethod
    def get_schemata_for_model(self):
        # import ipdb ; ipdb.set_trace()
        return Schema.objects.none()
        # return QuerySet()
    
    def get_schemata_for_instance(self,qa):
        # import ipdb ; ipdb.set_trace()
        if hasattr(self, 'entity'):
            schematas = Schema.objects.filter(entity = self.entity)
        else :
            schematas = qa
        return schematas  
    
    class Meta:
        app_label = 'billing'








# vim: set ft=python.django:
