from django.forms import ModelForm
from .models import Adress, AssetTypes, ComputeDeals, Deals

class DealAddressForm(ModelForm):
    #adress= forms.ModelChoiceField(queryset=Adress.objects.all())
    class Meta:
        model = Adress
        fields = ['city', 'state_code','postal_code']


class DealComputeDealForm(ModelForm):
    #compute= forms.ModelChoiceField(queryset=ComputeDeals.objects.all())
    class Meta:
        model = ComputeDeals
        fields = ['period', 'compare','percentage_compare_average_price']


class DealAssetTypeForm(ModelForm):
    
    class Meta:
        model = AssetTypes
        fields = ['baths_min', 'beds_min','radius']


class DealsForm(ModelForm):
    
    class Meta:
        model = Deals
        fields = ['name', 'property_status']