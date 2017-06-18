from django import forms
from suppliers.models import Supplier


class NewSupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewSupplierForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            # print(self.fields[field].widget['class'])
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


