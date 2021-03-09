from django.test import TestCase, Client
from django.urls import reverse
from deal.models import Deals, ComputeDeals, Adress,AssetTypes
import json
from django.contrib.auth.models import User
from deal.forms import DealAddressForm, DealAssetTypeForm, DealComputeDealForm, DealsForm

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
        self.user = User.objects.create_user(username='testuser', email='test@company.com', password='12345')
        self.deal1 = Deals.objects.create(user=self.user, name='deal1', property_status='For Rent', adress=self.address1, assets=self.asset1, computeDeal=self.compute1)
        
        self.pk = self.deal1.pk

        self.edit_deal_url = reverse('edit', args=[self.pk])
        self.delete_url = reverse('delete', args = [self.pk])
        self.display_specific_url = reverse('display_specific', args=[self.pk])

    def test_index(self):

        
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/index.html')

    def test_subscriptions(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.subscriptions_url)
        

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/subscriptions.html')

    def test_display(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.display_url)
        


        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/display.html')

    def test_deals_new(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.deals_new_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/deal-form.html')

    def test_edit(self):
        
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get(self.edit_deal_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/edit.html')

    
    def test_delete(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.delete_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/delete.html')

    def test_display_specific(self):
        login = self.client.login(username='testuser', password='12345')

        response = self.client.get(self.display_specific_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deal/display_specific.html')
    
    def test_edit_POST(self):
        login = self.client.login(username='testuser', password='12345')

        deal = Deals.objects.get(pk = self.pk)
        deal_form = DealsForm( instance=deal)
        response = self.client.post(self.edit_deal_url, {'edit_form':deal_form, 'deal':deal})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.deal1.name, 'deal1')

    def test_specific_deal_POST(self):
        login = self.client.login(username='testuser', password='12345')

        deal = Deals.objects.get(pk = self.pk)
        address = Adress.objects.get(pk = self.pk) 
        asset = AssetTypes.objects.get(pk = self.pk) 
        compute = ComputeDeals.objects.get(pk = self.pk)


        deal_form = DealsForm( instance=deal)
        form_adress = DealAddressForm(instance=address)
        form_compute = DealComputeDealForm(instance=compute)
        form_asset = DealAssetTypeForm(instance=asset)

        response = self.client.post(self.display_specific_url, {'deal':deal,'deal_form': deal_form,'adress':form_adress, 'compute':form_compute, 'asset':form_asset})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.deal1.name, 'deal1')


    def test_create_deal_POST(self):
        login = self.client.login(username='testuser', password='12345')

        deal = Deals.objects.get(pk = self.pk)
        address = Adress.objects.get(pk = self.pk) 
        asset = AssetTypes.objects.get(pk = self.pk) 
        compute = ComputeDeals.objects.get(pk = self.pk)


        deal_form = DealsForm( instance=deal)
        form_adress = DealAddressForm(instance=address)
        form_compute = DealComputeDealForm(instance=compute)
        form_asset = DealAssetTypeForm(instance=asset)

        response = self.client.post(self.deals_new_url, {'deal':deal,'deal_form': deal_form,'adress':form_adress, 'compute':form_compute, 'asset':form_asset})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.deal1.name, 'deal1')
    
    def test_delete_POST(self):
        login = self.client.login(username='testuser', password='12345')

        deal = Deals.objects.get(pk = self.pk)
        
        response = self.client.post(self.delete_url, {'deal':deal})

        self.assertEquals(response.status_code, 320)
        