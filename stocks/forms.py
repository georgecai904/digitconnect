from directconnect.forms import BasicForm
from stocks.models import Product


class NewProductForm(BasicForm):
    class Meta:
        model = Product
        exclude = ('purchaser', )

