from django import forms
from purchasers.models import Purchaser


class BasicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            # print(self.fields[field].widget['class'])
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class NewPurchaserForm(BasicForm):
    class Meta:
        model = Purchaser
        # fields = '__all__'
        exclude = ('user',)

