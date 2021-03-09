from django.test import SimpleTestCase
from django.urls import reverse, resolve
from deal.views import index,DealListView, SubscriptionsView


class TestUrls(SimpleTestCase):


    def test_index_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_deals_is_resolved(self):
        url = reverse('deals')
        self.assertEqual(resolve(url).func, DealListView)