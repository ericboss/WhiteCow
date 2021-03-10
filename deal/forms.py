from django.forms import ModelForm
from .models import Adress, AssetTypes, ComputeDeals, Deals

class DealAddressForm(ModelForm):
    """
    Address form
    """
    
    class Meta:
        model = Adress
        fields = ['city', 'state_code','postal_code']


class DealComputeDealForm(ModelForm):
    """
    Compute deals form
    """
    
    class Meta:
        model = ComputeDeals
        fields = ['period', 'compare','percentage_compare_average_price']


class DealAssetTypeForm(ModelForm):
    """
    Assets type form
    """
    
    class Meta:
        model = AssetTypes
        fields = ['baths_min', 'beds_min','radius']


class DealsForm(ModelForm):
    """
    Deals form
    """
    
    class Meta:
        model = Deals
        fields = ['name', 'property_status','days','time']