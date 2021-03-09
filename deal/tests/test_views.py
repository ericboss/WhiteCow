from django.test import TestCase, Client
from django.urls import reverse
from deal.models import Deals, ComputeDeals, Adress,AssetTypes
import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.subscriptions_url = reverse('subscriptions')
        self.display_url = reverse('display')
        self.deals_new_url = reverse('deals-new')
        self.address1 = Adress.objects.create(city="New York City", state_code="NY")
        self.asset1 = AssetTypes.objects.create()
        self.compute1 = ComputeDeals.objects.create(period='1 month', compare='below', percentage_compare_average_price=0)
        self.deal1 = Deals.objects.create(name='deal1', property_status='For Rent', adress=self.address1, assets=self.asset1, computeDeal=self.compute1)
        
        self.pk = self.deal1.pk

        self.edit_deal_url = reverse('edit', args=[self.pk])

    def test_index(self):

        
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/index.html')

    def test_subscriptions(self):

        response = self.client.get(self.subscriptions_url)
        print(response.text)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/subscriptions.html')

    def test_display(self):

        response = self.client.get(self.display_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/display.html')

    def test_deals_new(self):

        response = self.client.get(self.deals_new_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/deal-form.html')

    def test_edit(self):

        response = self.client.get(self.edit_deal_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/edit.html')


