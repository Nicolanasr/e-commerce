from django.forms import ModelForm
from django import forms
from .models import ShippingAddress, Product


class CreateShippingAddress(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class NewProduct(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['multiple'] = True
        self.fields['qty'].widget.attrs.update({'class' : 'w-25'})
        self.fields['qty'].widget.attrs['value'] = 0
        self.fields['price'].widget.attrs.update({'class' : 'w-25'})
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('seller', 'in_stock', )
    

# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields['username'].widget.attrs['autofocus'] = False

# def clean(self):
#     email = self.cleaned_data.get('email')
#     username = self.cleaned_data.get('username')
#     if User.objects.filter(email=email).exists():
#         raise ValidationError("Email Already exists")
#     elif User.objects.filter(username=username).exists():
#         raise ValidationError("Username Already exists")
#     return self.cleaned_data
