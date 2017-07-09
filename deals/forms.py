from deals.models import PurchaseOrderLine, SupplyOffer, ProductionRecord
from directconnect.forms import BasicForm


class NewPurchaseOrderForm(BasicForm):
    class Meta:
        model = PurchaseOrderLine
        exclude = ('purchaser', 'purchase_order', )


class NewSupplyOfferForm(BasicForm):
    class Meta:
        model = SupplyOffer
        fields = ('price', )


class JoinPurchaseForm(BasicForm):
    class Meta:
        model = PurchaseOrderLine
        fields = ('amount', )


class ProductionRecordForm(BasicForm):
    class Meta:
        model = ProductionRecord
        exclude = ('production', )