from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import AuthenticationForm

from .models import Order,Customer,Store

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ('customer','store')
        
    def __init__(self, *args, **kwargs): 
        super(OrderForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):        
        return super(OrderForm, self).save(*args, **kwargs)

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        exclude = ('store',)
        
    def __init__(self, *args, **kwargs): 
        super(CustomerForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):        
        return super(CustomerForm, self).save(*args, **kwargs)

class CustomLoginForm(AuthenticationForm):
    store = forms.ChoiceField(label='Store', required=False)

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm,self).__init__(*args, **kwargs)
        stores = Store.objects.all()
        choices = [(store.code, store.name) for store in stores]
        self.fields['store'].choices = choices




        
        
        