import requests
from bitpay.client import Client
from bitpay.exceptions import *
from django.conf import settings
from apps.web.models import WebConfigModel


class BitpayClient(Client):
    def __init__(self, api_uri="https://bitpay.com", insecure=False, pem='', tokens={}, bitpay_data=None):
        web = WebConfigModel.objects.get()
        bitpay_url = settings.BITPAY_URL
        if web.bitpay_mode == WebConfigModel.TEST:
            bitpay_url = settings.BITPAY_TEST_URL
        bitpay = bitpay_data
        self.tokens = ({
            'merchant': bitpay.token_merchant,
            'payroll': bitpay.token_payroll
        })
        self.pem = bitpay.pem
        self.client_id = bitpay.client_id
        self.uri = bitpay_url
        self.verify = not (insecure)
        self.user_agent = 'bitpay-python'

    def get_rates(self):
        uri = settings.BITPAY_URL + "/rates"
        try:
            response = requests.get(uri)
        except Exception as pro:
            raise BitPayConnectionError(pro.args)
        if response.ok:
            return response.json()['data']
        self.response_error(response)

    def get_rate(self, currency):
        uri = settings.BITPAY_URL + "/rates/" + currency
        try:
            response = requests.get(uri)
        except Exception as pro:
            raise BitPayConnectionError(pro.args)
        if response.ok:
            return response.json()['data']
        self.response_error(response)
