from deals.models import PurchaseOrderLine
from directconnect.forms import BasicForm


class NewPurchaseOrderForm(BasicForm):
    class Meta:
        model = PurchaseOrderLine
        exclude = ('purchaser', 'purchase_order', )