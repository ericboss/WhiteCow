from django.test import TestCase, Client
from deal.models import Deals, ComputeDeals, Adress,AssetTypes
import json
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.address1 = Adress.objects.create(city="New York City", state_code="NY")
        self.asset1 = AssetTypes.objects.create()
        self.compute1 = ComputeDeals.objects.create(period='1 month', compare='below', percentage_compare_average_price=0)
        self.user = User.objects.create_user(username='testuser', email='test@company.com', password='12345')
        self.deal1 = Deals.objects.create(user=self.user, name='deal1', property_status='For Rent', adress=self.address1, assets=self.asset1, computeDeal=self.compute1)
        
        self.pk = self.deal1.pk
    
    def test_get_query_params(self):
        print("#######################")
        print(self.deal1.get_query_params())