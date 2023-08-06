from revpayment.settings import api_settings
from revpayment.models import RedirectState
from revpayment import exceptions
from django.shortcuts import redirect
from rest_framework import response
from django.conf import settings
import requests
import json
import jwt
from revjwt import decode


class CheckoutSDK:
    payment_classes = (
        ('neweb', api_settings.DEFAULT_NEWEB_CLASS),
        ('ecpay', api_settings.DEFAULT_ECPAY_CLASS),
        ('credit', api_settings.DEFAULT_CREDIT_CLASS),
    )
    handler_class = api_settings.HANDLER_CLASS
    fail_url = api_settings.DEFAULT_CHECKOUTFAIL_URL
    redirect_url = api_settings.DEFAULT_REDIRECT_URL
    redirect_query = api_settings.DEFAULT_REDIRECT_QUERY

    def __init__(self, state):
        self.state = state
        if type(state.cart) is str:
            self.cart = json.loads(state.cart)
        elif type(state.cart) is dict:
            self.cart = state.cart
        else:
            raise TypeError
        self.payment_type = state.payment_type
        self.payment_subtype = state.payment_subtype
        self.buyer = state.buyer

    def get_payment_class(self):
        try:
            payment_class = [
                c[1] for c in self.payment_classes if c[0] == self.payment_type][0]
            return payment_class
        except IndexError:
            valids = [payment[0] for payment in self.payment_classes]
            raise exceptions.InvalidPaymentType(valids=valids, invalid=self.payment_type)

    def get_payment(self):
        payment_class = self.get_payment_class()
        return payment_class(buyer=self.buyer, payment_subtype=self.payment_subtype, cart=self.cart, order_id=self.state.order_id, order_type=self.state.order_type)

    def checkout(self):
        try:
            payment = self.get_payment()
            result = payment.checkout()
            return redirect(result['url'])
        except exceptions.PaymentException as e:
            return redirect(f'{self.fail_url}?error={e.error}&error_detail={e.error_detail}')

    def callback(self, data):
        payment = self.get_payment()
        payment.callback(data)
        return response.Response({}, 200)

    def customer_redirect(self, data):
        payment = self.get_payment()
        order = payment.customer_redirect(data)
        return redirect(f'{self.redirect_url}?{self.redirect_query}={order.id}')


class BaseCertificate:
    default_aud = settings.CLIENT_ID

    def __init__(self, cert):
        self.cert = cert

    def get_order_id(self, sub):
        raise NotImplementedError

    def verify(self):
        decoded = decode(self.cert, verify=True, audience=self.default_aud)
        if decoded['typ'] != 'certificate':
            raise

        sub = decoded['sub']
        order_id = self.get_order_id(sub)
        state = RedirectState.objects.get(order_id=order_id)
        return state, sub


class NewebCertificate(BaseCertificate):
    def get_order_id(self, sub):
        return sub['Result']['MerchantOrderNo']


class EcpayCertificate(BaseCertificate):
    def get_order_id(self, sub):
        return sub['MerchantTradeNo']


def check_certificate(cert):
    unverified = decode(cert, verify=False)
    provider = unverified['provider']
    if provider == 'ecpay':
        cert_class = EcpayCertificate
    elif provider == 'neweb':
        cert_class = NewebCertificate

    certificate = cert_class(cert)
    return certificate.verify()
