from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from .models import Order,Customer

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ('customer')
        
    def __init__(self, *args, **kwargs): 
        super(OrderForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):        
        return super(OrderForm, self).save(*args, **kwargs)

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        
    def __init__(self, *args, **kwargs): 
        super(CustomerForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):        
        return super(CustomerForm, self).save(*args, **kwargs)
        
        
        
        