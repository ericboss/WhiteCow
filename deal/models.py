from django.db import models
import pandas as pd
import requests
from config import *

class Adress(models.Model):
    city = models.CharField(max_length = 40)
    state_code = models.CharField(max_length = 10)
    postal_code = models.CharField(max_length = 10, blank = True)

    def __str__(self):
        return "{}, {}".format(self.city, self.state_code)



class AssetTypes(models.Model):

    PROP_TYPE_CHOICES = [('single_family','single_family') ,('multi_family','multi_family'),
                          ('condo','condo'), ('mobile','mobile'),
                          ('land','land'),('farm','farm'),('other','other')]
    SORT_CHOICES = [('sold_date','sold_date'),('beds_high','beds_high'),
                       ('price_low','price_low'), ('price_high','price_high'),('lot_sqft_high','lot_sqft_high')]


    
    offset = models.CharField(max_length = 10, default = "0")
    limit = models.IntegerField(default=200)
    baths_min = models.IntegerField(default= None)
    beds_min = models.IntegerField(default = None)
    radius = models.IntegerField(default = None)
    price_min = models.IntegerField(default = None)

    sqft_min = models.IntegerField(default = None)
    age_min = models.IntegerField(default = None)
    lot_sqft_max = models.IntegerField(default = None)
    price_max = models.IntegerField(default = None)
    lot_sqft_min = models.IntegerField(default = None)
    prop_type = models.CharField(max_length = 20,choices = PROP_TYPE_CHOICES,default = None)
    age_max = models.IntegerField(default = None)
    sort = models.CharField(max_length = 20,choices = SORT_CHOICES,default = None)
    sqft_max = models.IntegerField(default = None)



class ComputeDeals(models.Model):
    PERIOD_CHOICES = [('1 month', '1m'), ('3 months','3m'),('6 months','6m'),('One year','12m')]
    COMPARE_CHOICES = [('below','below'),('above','above'),('equals','equals')]

    
    period =  models.CharField(max_length = 20,choices = PERIOD_CHOICES,default = None)
    compare = models.CharField(max_length = 20,choices = COMPARE_CHOICES,default = None)
    percentage_compare_average_price =  models.IntegerField(default = None)

class Deals(models.Model):
    PROPERTY_STATUS_CHOICES = [ ('For rent', 'rent'), ('For Sale','sale')

    ]
    name = models.CharField(max_length=20)
    property_status = models.CharField(max_length = 20,choices = PROPERTY_STATUS_CHOICES)
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE)
    assets = models.ForeignKey('AssetTypes', on_delete=models.CASCADE)
    computeDeal = models.ForeignKey('ComputeDeals', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    @staticmethod
    def get_query_params():
        adress_params = vars(Adress.objects.all().last())
        address_params.pop('_state')
        address_params.pop('id')

        asset_params = vars(AssetTypes.objects.all().last())
        asset_params.pop('_state')
        asset_params.pop('id')

        query_params = {}
        query_params.update(adress_params)
        query_params.update(asset_params)
        #query_params.update(compute_params)
    
         return query_params

    @staticmethod
    def search_query(prop_status, query_params):
        url = ''
        if prop_status=='rent':
            url = url_for_rent
        if prop_status == 'sale':
            url = url_for_sale

        # header
        headers = {
          'x-rapidapi-host': host,
           'x-rapidapi-key': api_key
          }

        # response
        response = requests.request("GET", url, headers=headers, params=query_params)
        return response.json()

    @staticmethod
    def get_historic_data_similar_asset(url= url_historic,query_params = Deals.get_query_params()):
            # header
        headers = {
          'x-rapidapi-host': host,
           'x-rapidapi-key': api_key
          }

        # response
        response = requests.request("GET", url, headers=headers, params=query_params)
        return response.json()

    @staticmethod
    def process_json_response(response_json):
        """
        Process the list for sale API response.
        Convert each listing to a dataframe, append to a list, and concatenate to one dataframe.

        Parameters
        ----------
        @response_json [dictionary]: API response from search_query

        Returns
        -------
        [dataframe] Dataframe of all list for responses

        """

        # empty dataframe
        dataframe_list = []

        # iterate through each for sale listing
        for l in response_json['properties']:

            # convert each listing to dataframe
            _temp_df = pd.DataFrame.from_dict(l, orient='index').T

            # append to dataframe list for all listings
            dataframe_list.append(_temp_df)

        # concatenate all dataframes, for missing col values enter null value
        return pd.concat(dataframe_list, axis=0, ignore_index=True, sort=False)

    @staticmethod
    def average_price_sold():

        """
        Computes Average Sold price
        """
        hist = Deals.get_historic_data_similar_asset()

        df_sold = Deals.process_json_response(hist)

        return df_sold["price"].mean()
    
    def percentage_average_market_data(self,p, data, avp,compare="below" ):
        """
        Filters dataframe to return a new data frame based on below/above/equals average market price of sold properties
        Parameters
        ----------
        data [dataframe]: dataframe for properties
        p[int]: Represent percentage number from 0 to 100
        avp [float]: Average Market Price
        compare[String]: Get the compare mode used during filtering.Three modes available: above, below and equals

        Returns
        -------
        [dataframe] Filtered Dataframe
        """
    
        #Computes the percentage value of the avp
        p_value = avp - (p/100 * avp)
        #Filters data based on p_value
        if compare =="below":
            df = data[data["price"]< p_value ]
        elif compare =="above":
            df = data[data["price"]> p_value ]
        elif compare == "equals":
            df = data[data["price"] ==  p_value ]
        else:
            df = data
        return df
        




        


    

    


    

    
    



