from django import forms
from products.models import Product


class BasicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class NewProductForm(BasicForm):
    class Meta:
        model = Product
        exclude = ('purchaser', )

