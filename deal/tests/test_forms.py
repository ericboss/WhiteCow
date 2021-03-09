from deal.forms import DealAddressForm, DealAssetTypeForm, DealComputeDealForm, DealsForm
from django.test import SimpleTestCase


def setUp(self):
        self.address1 = Adress.objects.create(city="New York City", state_code="NY")
        self.asset1 = AssetTypes.objects.create()
        self.compute1 = ComputeDeals.objects.create(period='1 month', compare='below', percentage_compare_average_price=0)
        self.user = User.objects.create_user(username='testuser', email='test@company.com', password='12345')
        self.deal1 = Deals.objects.create(user=self.user, name='deal1', property_status='For Rent', adress=self.address1, assets=self.asset1, computeDeal=self.compute1)
        
        self.pk = self.deal1.pk


        self.deal = Deals.objects.get(pk = self.pk)
        self.address = Adress.objects.get(pk = self.pk) 
        self.asset = AssetTypes.objects.get(pk = self.pk) 
        self.compute = ComputeDeals.objects.get(pk = self.pk)



def test_adress_form_valid_data(self):
    form_adress = DealAddressForm(instance=self.address)
    self.assertTrue(form_adress.is_valid()) 