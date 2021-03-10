from django.db import models
import pandas as pd
import numpy as np
import requests
from .config import *
import json
from django.contrib.auth.models import User

class Adress(models.Model):
    """
    Addres Class contains attributes necessary for saving the Adress of a deal.
    """
    city = models.CharField(max_length = 40)
    state_code = models.CharField(max_length = 10)
    postal_code = models.CharField(max_length = 10, blank = True, default = '')

    def __str__(self):
        return "{}, {}".format(self.city, self.state_code)



class AssetTypes(models.Model):
    """
    AssetTypes Class contains attributes for the assets of a real esate property.Deal Class will use
     these assets along side with Adress,Computedeals class in order to comeout with  a deal.
    """

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
    """
    Compute Deals Class contains attributes for making some computations for the deal.
    - period: The user might want to compare data against average market price for the last x period( 1 month, 3 months etc)
    - compare: The user might want to get data that are above/below average market price
    - percentage_compare_average_price: The user might want to get data that are X% above/below average market price.
    """
    PERIOD_CHOICES = [(1, '1 month'), (3,'3 months'),(6,'6 months'),(12,'One year')]
    COMPARE_CHOICES = [('below','below'),('above','above'),('equals','equals')]

    
    period =  models.IntegerField(choices = PERIOD_CHOICES, blank = True, null = True)
    compare = models.CharField(max_length = 20,choices = COMPARE_CHOICES,default = None)
    percentage_compare_average_price =  models.IntegerField(default = 0)

    def get_percentage_compare_average_price(self):
        return self.percentage_compare_average_price

class Deals(models.Model):
    """
    Deals class is for coming up with real estate deals. As atttributes, it contains a foreignkey to adress, ComputeDeals and 
    AssetTypes class. Aded to that the deal has a name,
    - property_status: whether the property if for rent or for sale
    - user: We want to compute and store deals per user
    - ReceiveEmail: option for whether the user  wants to receive email notifications
    - days: The user has a soption to receive emails daily or during weekends
    - time: The user can have as option to choose at what time he/she will like to receive notifications 
    """
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
        """
        This method is to get the user's query parameters. It will be later used to make a get request to the realestate API
        to get data.
        """
        address_params = vars(self.adress)

        asset_params = vars(self.assets)
    
        query_params = {}
        query_params.update(address_params)
        query_params.update(asset_params)
        query_params.pop('_state')
        query_params.pop('id')
        #query_params = json.dumps(query_params)
        #query_params = query_params.replace('"', "")
        #query_params.update(compute_params)
    
        return query_params

    #url_for_rent
    #url_for_sale
    #url_historic
    def property_search_query(self, url):
    
        # header
        headers = {
          "x-rapidapi-host": host,
           "x-rapidapi-key": api_key
          }
        query_params = self.get_query_params()
       
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

    def get_sold_data_properties(self):
         # Get historic similar assets data in json
        hist = self.property_search_query(url = url_historic)
        to_json = Deals.response_json(hist)

        df = self.process_json_response(to_json)
        return df

    def filter_sold_data(self, df):
        """
        Filter dataframe to return values for the last x months.

        Gets the current data, and computes the months difference date bwtween current and what values entered as argument(by), then filters the data to return the desired dataframe

        Parameters
        ----------
    

        Returns
        -------
        [dataframe] Filtered Dataframe

        """
       
        #Grap the last_update column
        df["last_update"] = pd.to_datetime(df["last_update"], utc = True)

        #Get the current time"
        now = pd.to_datetime("now", utc=True)
        #Compute the diffrence in month between current and dates in the last update column and create a new column
        df["monthDiff"] = abs((now - df["last_update"]) /np.timedelta64(1,'M'))
    
        # Filters he dataframe based on monthDiff column
        if self.computeDeal.period is not None:

            df_new= df[df["monthDiff"] <= self.computeDeal.period ]
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
        




        


    

    


    

    
    



