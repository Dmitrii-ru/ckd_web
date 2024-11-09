import math
from distutils.command.install import value

import requests
import json
import re

from core_app.redis_cli import RedisClientMain
from stock.utils.consts_all import time_cache_rates, redis_db_rates
from datetime import datetime
import locale


class RequestsApi:
    def __init__(self,
                 api_url = None
                 ):
        self.api_url = api_url


    def get_jsonp_response(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response
        else:
            return None



class RatesCbr(RequestsApi):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    def __init__(self):
        super().__init__(
            api_url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        )

        self.rm = RedisClientMain(
            time_cache=time_cache_rates,
            db = redis_db_rates
        )
        self.key_rates_in_rub = 'rates_in_rub'
        self.object=None
        self.new_object={}
        self.date_list_keys = ['Date','PreviousDate']
        self.curr_list_keys = ['Name','Value','Previous','Nominal']

    def format_object_time(self):
        odj = self.object

        for date in self.date_list_keys:
            if d:= odj.get(date,None):
                d= datetime.fromisoformat(d)
                d =d.strftime('%d %B %Y, %H:%M')
                self.new_object[date] = d

    def format_object_currency(self):
        odj_valute = self.object['Valute']
        dict_rates={}
        for k,v in odj_valute.items():
            curr_dict = {k:v[k] for k in self.curr_list_keys}
            curr_dict = self.dynamics(curr_dict)
            dict_rates[k] = curr_dict

        self.new_object['rates'] = dict_rates

    @staticmethod
    def custom_round(value):

            return value



    def dynamics(self,curr_dict):
        value_d = float(curr_dict['Value'])
        previous_d = float(curr_dict['Previous'])
        dynamics = value_d - previous_d
        curr_dict['Dynamics'] = self.custom_round(dynamics)
        curr_dict['DynamicsMarker'] = True if dynamics >0 else False

        return curr_dict


    def format_data(self,response):
        jsonp_str = response.text
        json_str = re.sub(r'^CBR_XML_Daily_Ru\((.*)\);$', r'\1', jsonp_str)
        data = json.loads(json_str)
        self.object = data
        self.format_object_time()
        self.format_object_currency()

        self.rm.create_key(self.key_rates_in_rub,self.new_object)



    def get_rates(self):
        rates = self.rm.get_key_values(self.key_rates_in_rub)
        if not rates:
            response = self.get_jsonp_response()
            if response:
                self.format_data(response)
                rates = self.rm.create_key(
                    key_name=self.key_rates_in_rub,
                    data=self.new_object
                )
            return None
        return rates






