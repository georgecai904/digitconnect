from deals.models import PurchaseOrderLine, SupplyOffer, ProductionRecord
from directconnect.forms import BasicForm


class PurchaseOrderForm(BasicForm):
    class Meta:
        model = PurchaseOrderLine
        exclude = ('purchaser', 'purchase_order', )


class SupplyOfferForm(BasicForm):
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