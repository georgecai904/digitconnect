from directconnect.forms import BasicForm
from stocks.models import Product


class ProductForm(BasicForm):
    class Meta:
        model = Product
        exclude = ('purchaser', )

