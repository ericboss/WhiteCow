from django.db import models
import pandas as pd
import numpy as np
import requests
from .config import *
import json
from django.contrib.auth.models import User

class Adress(models.Model):
    city = models.CharField(max_length = 40)
    state_code = models.CharField(max_length = 10)
    postal_code = models.CharField(max_length = 10, blank = True, default = '')

    def __str__(self):
        return "{}, {}".format(self.city, self.state_code)



class AssetTypes(models.Model):

    PROP_TYPE_CHOICES = [('single_family','single_family') ,('multi_family','multi_family'),
                          ('condo','condo'), ('mobile','mobile'),
                          ('land','land'),('farm','farm'),('other','other')]
    SORT_CHOICES = [('sold_date','sold_date'),('beds_high','beds_high'),
                       ('price_low','price_low'), ('price_high','price_high'),('lot_sqft_high','lot_sqft_high')]


    
    offset = models.CharField(max_length = 10, default = "0")
    limit = models.IntegerField(default=10)
    baths_min = models.IntegerField( blank=True, null=True)
    beds_min = models.IntegerField( blank=True, null=True)
    radius = models.IntegerField(blank=True, null=True)
    price_min = models.IntegerField(blank=True, null=True)

    sqft_min = models.IntegerField(blank=True, null=True)
    age_min = models.IntegerField(blank=True, null=True)
    lot_sqft_max = models.IntegerField(blank=True, null=True)
    price_max = models.IntegerField(blank=True, null=True)
    lot_sqft_min = models.IntegerField(blank=True, null=True)
    prop_type = models.CharField(max_length = 20,choices = PROP_TYPE_CHOICES, blank = True, default = '')
    age_max = models.IntegerField(blank=True, null=True)
    sort = models.CharField(max_length = 20,choices = SORT_CHOICES, blank = True, default = '')
    sqft_max = models.IntegerField(blank=True, null=True)



class ComputeDeals(models.Model):
    PERIOD_CHOICES = [('1 month', '1 month'), ('3 months','3 months'),('6 months','6 months'),('One year','One year')]
    COMPARE_CHOICES = [('below','below'),('above','above'),('equals','equals')]

    
    period =  models.CharField(max_length = 20,choices = PERIOD_CHOICES,default = None)
    compare = models.CharField(max_length = 20,choices = COMPARE_CHOICES,default = None)
    percentage_compare_average_price =  models.IntegerField(default = 0)

    def get_percentage_compare_average_price(self):
        return self.percentage_compare_average_price

class Deals(models.Model):
    PROPERTY_STATUS_CHOICES = [ ('For Rent', 'For Rent'), ('For Sale','For Sale')
    ]
    DAY_CHOICES = [('mon,tue,wed,thu,fri,sat,sun', 'Daily'), ('sat,sun', 'Weekends')]
    TIME_CHOICES = [(5, '5:00am'), (6, '6:00am'), (7, '7:00am'), 
                   (8, '8:00am'), (17, '5:00pm'), (21, '9:00pm'),(22, '10:00pm')]


    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Deals", null=True)
    name = models.CharField(max_length=20)
    property_status = models.CharField(max_length = 20,choices = PROPERTY_STATUS_CHOICES, default = 'For Rent')
    adress = models.ForeignKey('Adress', on_delete=models.CASCADE)
    assets = models.ForeignKey('AssetTypes', on_delete=models.CASCADE)
    computeDeal = models.ForeignKey('ComputeDeals', on_delete=models.CASCADE)
    ReceveEmail = models.BooleanField(default=True)
    days = models.CharField(max_length=100, choices=DAY_CHOICES, blank = True, default = '')
    time = models.IntegerField(choices = TIME_CHOICES, blank = True, null = True)


    

    def __str__(self):
        return self.name
   
    def get_query_params(self):
        address_params = vars(self.adress)
        #address_params.pop('_state')
        #address_params.pop('id')

        asset_params = vars(self.assets)
        #asset_params.pop('_state')
        #asset_params.pop('id')

        query_params = {}
        query_params.update(address_params)
        query_params.update(asset_params)
        query_params.pop('_state')
        query_params.pop('id')
        #query_params = json.dumps(query_params)
        #query_params = query_params.replace('"', "")
        #query_params.update(compute_params)
    
        return query_params

    
    def search_query(self):
    
        if self.property_status=='For Rent':
            url = url_for_rent
        else :
            url = url_for_sale

        # header
        headers = {
          "x-rapidapi-host": host,
           "x-rapidapi-key": api_key
          }
        query_params = self.get_query_params()
       
        # response
        er = {'city': 'Washington', 'state_code': 'WA', 'postal_code': '', 'offset': '0', 'limit': 200, 'baths_min': 1, 'beds_min': 1, 'radius': 5, 'price_min': 0, 'sqft_min': 0, 'age_min': 0, 'lot_sqft_max': 800, 'price_max': 100000, 'lot_sqft_min': 0, 'prop_type': 'single_family', 'age_max': 10, 'sort': 'sold_date', 'sqft_max': 1000}
        response = requests.request("GET", url, headers=headers, params=query_params)
        return response

    def get_historic_data_similar_asset(self):
        query_params = self.get_query_params()
        
            # header
        headers = {
          'x-rapidapi-host': host,
           'x-rapidapi-key': api_key
          }
        url= url_historic

        # response
        response = requests.request("GET", url, headers=headers, params=query_params)
        return response
    @staticmethod
    def response_json(response):
        return response.json()

    
    def process_json_response(self,response_json):
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

   
    def filter_month(self):
        """
        Filter dataframe to return values for the last x months.

        Gets the current data, and computes the months difference date bwtween current and what values entered as argument(by), then filters the data to return the desired dataframe

        Parameters
        ----------
    

        Returns
        -------
        [dataframe] Filtered Dataframe

        """
        # Get historic similar assets data in json
        hist = self.get_historic_data_similar_asset()
        to_json = Deals.response_json(hist)

        df = self.process_json_response(to_json)
        #Grap the last_update column
        df["last_update"] = pd.to_datetime(df["last_update"], utc = True)

        #Get the current time"
        now = pd.to_datetime("now", utc=True)
        #Compute the diffrence in month between current and dates in the last update column and create a new column
        df["monthDiff"] = abs((now - df["last_update"]) /np.timedelta64(1,'M'))
    
        # Filters he dataframe based on monthDiff column
        if self.computeDeal.period =="1 month":
            df_new= df[df["monthDiff"] <= 1]
        elif self.computeDeal.period =="3 months":
            df_new= df[df["monthDiff"] <= 3 ]
        elif self.computeDeal.period =="6 months":
            df_new= df[df["monthDiff"] <= 6 ]
        elif self.computeDeal.period =="One year":
            df_new= df[df["monthDiff"] <= 12 ]
        else:
            df_new = df
        return df_new
    

   
    def average_price_hist(self):

        """
        Computes Average Sold price
        """
        df_hist = self.filter_month()

        return df_hist['price'].mean()

    def convert_add_price(self,data):
        data['community'] = data['community'].astype('str')
        data['community']=data.community.apply(eval)
        price = []
        for i in range(data['community'].size):
            price.append(data['community'][i]['price_max'])
        
        data['price'] = pd.DataFrame(price)
        return data
    
    def percentage_average_market_data(self):
        """
        Filters dataframe to return a new data frame based on below/above/equals average market price of sold properties
        Parameters
        ----------
        
        Returns
        -------
        [dataframe] Filtered Dataframe
        """
        data= self.search_query()
        data_json =Deals.response_json(data)

        data = self.process_json_response(data_json)
        data = self.convert_add_price(data)
        #Computes the percentage value of the avp
        average_price = self.average_price_hist()
        compare_value = self.computeDeal.compare

        p_value =  average_price - ((self.computeDeal.get_percentage_compare_average_price()/100)* average_price )
        #Filters data based on p_value
        if compare_value  =="below":

            df = data[data["price"]< p_value ]
        elif compare_value =="above":
            df = data[data["price"]> p_value ]
        elif compare_value =="equals":
            df = data[data["price"] ==  p_value ]
        else:
            df = data
        return df.to_json(orient='split')
        




        


    

    


    

    
    



