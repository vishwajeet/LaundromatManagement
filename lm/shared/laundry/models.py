from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime

ORDER_STATUS_CHOICES = (
    ('IQ', 'In Que'),
    ('IP', 'In Progress'),
    ('CO', 'Complete'),
    ('DE', 'Delivered'),
)

ORDER_TYPE_CHOICES = (
    ('IS', 'In Store'),
    ('PU', 'Pickup')
)

class Customer(models.Model):
    store = models.ForeignKey('Store', verbose_name=_('Store'),blank=True, null=True)
    mobile_number = models.BigIntegerField(verbose_name=_('Mobile Number'),
                                           help_text=_("Enter mobile number 10 digits"))
    name = models.CharField(verbose_name=_('Customer Name'), max_length=100,help_text=_("Name of Customer"))
    email = models.EmailField(verbose_name=_('E-mail address:'),blank=True, null=True)
    alt_contact_number = models.BigIntegerField(verbose_name=_('Alternate Contact Number'),
                                             help_text=_("Enter alternate contact number"),blank=True, null=True)
    address = models.CharField(verbose_name=_('Address'), max_length=255,help_text=_("Address of Customer"),
                               blank=True, null=True)
    
    class Meta:
        verbose_name = 'Customer'
        app_label = 'laundry'
        
    def __unicode__(self):
        return "%s(%d)"%(self.name,self.mobile_number)
    
    @property
    def last_visit(self):
        last_visit = "No Visits"
        orders = Order.objects.filter(customer=self).order_by('-date')
        if len(orders) > 0:
            last_visit_date = orders[0].date.date()
            last_visit = (datetime.date.today() - last_visit_date).days
            
        return last_visit
    
    @property
    def orders(self):
        orders = Order.objects.filter(customer=self).count()
        return orders

class Order(models.Model):
    store = models.ForeignKey('Store', verbose_name=_('Store'),blank=True, null=True)
    customer = models.ForeignKey('Customer', verbose_name=_('Customer'))
    order_type = models.CharField(verbose_name=_('Order Type'), max_length=20,
                              help_text=_("Type of Order"), choices=ORDER_TYPE_CHOICES, default='IS')
    date = models.DateTimeField(verbose_name=_('Order Date'))
    wash_load = models.DecimalField(verbose_name=_('Wash Load'),decimal_places=1,max_digits=10,
                                             help_text=_("Wash Load in Kgs"),blank=True, null=True)
    
    wash_price = models.IntegerField(verbose_name=_('Wash Price'),help_text=_("Wash Price"),
                                     blank=True, null=True)
    
    iron_load = models.IntegerField(verbose_name=_('Iron Load'),
                                             help_text=_("Iron Load in pieces"),blank=True, null=True)
    
    iron_price = models.IntegerField(verbose_name=_('Iron Price'),help_text=_("Iron Price"),
                                     blank=True, null=True)
    discount =  models.IntegerField(verbose_name=_('Discount'),help_text=_("Discount"),
                                    blank=True, null=True)
    
    billed_amount = models.IntegerField(verbose_name=_('Billed Amount'),
                                             help_text=_("Total Billed Amount"))
    
    bill_no = models.IntegerField(verbose_name=_('Bill No'),blank=True, null=True,
                                             help_text=_("Bill No"))
    status = models.CharField(verbose_name=_('Status of Order'), max_length=20,
                              help_text=_("Current Status of Order"), choices=ORDER_STATUS_CHOICES, default='IQ')
    payment_status = models.BooleanField(verbose_name=_('Payment Status:'), default=False)
    
    class Meta:
        verbose_name = 'Order'
        app_label = 'laundry'
        
            
    def __unicode__(self):
        return "%s-%d(%s Kgs,%s pcs)"%(self.customer.name,self.customer.mobile_number,self.wash_load,self.iron_load)

class Pickup(models.Model):
    pass


class Store(models.Model):
    name = models.CharField(verbose_name=_('Store Name'), max_length=128,help_text=_("Store Name"))
    code = models.CharField(verbose_name=_('Store Code'), max_length=5,help_text=_("Store Code"))
    email = models.EmailField(verbose_name=_('Store Email'),blank=True, null=True)
    address = models.CharField(verbose_name=_('Address'), max_length=255,help_text=_("Address of Store"),
                               blank=True, null=True)
    phone = models.CharField(verbose_name=_('Store Phone'), max_length=15,help_text=_("Store Phone"))

    def __unicode__(self):
        return self.name


class Rates(models.Model):    
    store = models.ForeignKey('Store', verbose_name=_('Store'))
    iron_rate = models.IntegerField(verbose_name=_('Iron Rate'),help_text=_("Per piece iron rate"))
    siron_rate = models.IntegerField(verbose_name=_('Steam Iron Rate'),help_text=_("Per piece steam iron rate"))
    wr_upto_4kg = models.IntegerField(verbose_name=_('4kg Rate'),help_text=_("Upto 4kg rate"))
    wr_upto_5kg = models.IntegerField(verbose_name=_('5kg Rate'),help_text=_("Upto 5kg rate"))
    wr_upto_6kg = models.IntegerField(verbose_name=_('6kg Rate'),help_text=_("Upto 6kg rate"))
    wr_upto_7kg = models.IntegerField(verbose_name=_('7kg Rate'),help_text=_("Upto 7kg rate"))
    wr_per_kg = models.IntegerField(verbose_name=_('1kg Rate'),help_text=_("Per kg rate"))
    premium = models.IntegerField(verbose_name=_('Premium Rate'),help_text=_("Premium Rate"))

    def __unicode__(self):
        return self.store.name

