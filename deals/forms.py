from deals.models import PurchaseOrderLine, SupplyOffer
from directconnect.forms import BasicForm


class NewPurchaseOrderForm(BasicForm):
    class Meta:
        model = PurchaseOrderLine
        exclude = ('purchaser', 'purchase_order', )


class NewSupplyOfferForm(BasicForm):
    class Meta:
        model = SupplyOffer
        fields = ('price', )