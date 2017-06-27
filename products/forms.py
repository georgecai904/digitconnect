from django import forms
from products.models import Product


class NewProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('purchaser', )

    def __init__(self, *args, **kwargs):
        super(NewProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })