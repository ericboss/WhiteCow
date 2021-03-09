from django.test import SimpleTestCase
from django.urls import reverse, resolve
from deal.views import index,manage_subscriptions,deal_diaply_on_search,create_deal,edit, delete, deal_diaplay_specific_search_id


class TestUrls(SimpleTestCase):


    def test_index_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_deals_is_resolved(self):
        url = reverse('subscriptions')
        self.assertEqual(resolve(url).func, manage_subscriptions)
    
    def test_deal_diaply_on_search_is_resolved(self):
        url = reverse('display')
        self.assertEqual(resolve(url).func, deal_diaply_on_search)
    
    def test_create_deal_is_resolved(self):
        url = reverse('deals-new')
        self.assertEqual(resolve(url).func, create_deal)
    
    def test_edit_deal_is_resolved(self):
        url = reverse('edit', args=[1])
        self.assertEqual(resolve(url).func, edit)
    
    def test_delete_deal_is_resolved(self):
        url = reverse('delete', args=[1])
        self.assertEqual(resolve(url).func, delete)
    
    def test_deal_diaplay_specific_search_id_resolved(self):
        url = reverse('display_specific', args=[1])
        self.assertEqual(resolve(url).func, deal_diaplay_specific_search_id)

    