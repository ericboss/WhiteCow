from django.test import TestCase, Client
from django.urls import reverse
from deal.models import Deals, ComputeDeals, Adress,AssetTypes
import json

class TestViews(TestCase):
    client = Client()
    response = client.get(reverse('index'))

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'deal/index.html')


