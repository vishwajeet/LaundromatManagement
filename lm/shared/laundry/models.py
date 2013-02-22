from django.db import models
from django.utils.translation import ugettext_lazy as _

ORDER_STATUS_CHOICES = (
    ('IQ', 'In Que'),
    ('IP', 'In Progress'),
    ('CO', 'Complete'),
    ('DE', 'Delivered'),
)

class Customer(models.Model):
    
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

class Order(models.Model):
    customer = models.ForeignKey('Customer', verbose_name=_('Customer'))
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
    