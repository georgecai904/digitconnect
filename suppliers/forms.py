from django import forms
from suppliers.models import Supplier


class BasicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            # print(self.fields[field].widget['class'])
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class NewSupplierForm(BasicForm):
    class Meta:
        model = Supplier
        # fields = '__all__'
        exclude = ('user',)

