import praw
from pmaw import PushshiftAPI
import pandas as pd
from datetime import datetime

from app.models import TradingDay, Comment
from django.core.management.base import BaseCommand, CommandError
import requests, os

class Command(BaseCommand):

    def get_total_cap_data(self):
        total_data = pd.read_csv('./app/data/CRYPTOCAP_TOTAL.csv')
        total_data["time"]= pd.to_datetime(total_data['time'],unit='s').apply(lambda x: str(x)[:10])
        return total_data

    def get_price_data(self):
        btc_data = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=max').json()['prices']
        btc_price = pd.DataFrame(data=btc_data, columns=['time','btc_price'])
        btc_price["time"]= btc_price["time"].apply(pd.to_datetime, unit='ms').apply(lambda x: str(x)[:10])
        btc_price = btc_price.drop_duplicates(subset=['time'])
        eth_data = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=max').json()['prices']
        eth_price = pd.DataFrame(data=eth_data, columns=['time','eth_price'])
        eth_price["time"]= eth_price["time"].apply(pd.to_datetime, unit='ms').apply(lambda x: str(x)[:10])
        eth_price = eth_price.drop_duplicates(subset=['time'])

        return (btc_price, eth_price)
    
    def aggregate_data(self):
        total_data = self.get_total_cap_data()
        data_tuple = self.get_price_data()
        btc_price, eth_price = data_tuple[0], data_tuple[1]
        total_df = total_data.merge(btc_price, how='inner', on='time').sort_values(by='time', axis=0)
        total_df = total_df.merge(eth_price, how='inner', on='time').sort_values(by='time', axis=0)
        return total_df
    
    def add_data(self):
        total_df = self.aggregate_data()
        print(total_df)
        print("4")
        for i in total_df.iterrows():
            trading_day = TradingDay(date=i[1]['time'],
                                    crypto_cap=i[1]['open'],
                                    ethereum_price=i[1]['eth_price'],
                                    bitcoin_price=i[1]['btc_price']
                                    )
            trading_day.save()
    
    def handle(self, *args, **options):
        try:
            self.add_data()
        except:
            raise CommandError('An error has occurred.')