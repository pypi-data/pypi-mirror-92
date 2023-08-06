import requests
import json
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime
from revpayment.settings import api_settings
from revpayment.logistics import LogisticsSDK
from django.conf import settings
from revpayment import actions
import copy


class BasePaymentMeta(type):
    def __new__(cls, names, bases, attrs):
        attrs['_declared_actions'] = {}
        for v in bases:
            _declared = getattr(v, '_declared_actions', {})
            declared = copy.deepcopy(_declared)
            attrs['_declared_actions'] = {
                **declared,
                **attrs['_declared_actions']
            }
        for k, v in attrs.items():
            if isinstance(v, type) and issubclass(v, actions.BaseAction):
                attrs['_declared_actions'][k] = v
        return super().__new__(cls, names, bases, attrs)


class BasePayment(metaclass=BasePaymentMeta):
    def __init__(self, cart, buyer, order_id, payment_subtype='default', order_type='default'):
        self.cart = cart
        self.payment_subtype = payment_subtype
        self.buyer = buyer
        self.order_id = order_id
        self.order_type = order_type

        for k, v in self.__class__._declared_actions.items():
            use_action = getattr(self, f'use_{k}', None)
            action = v(cart=cart, buyer=buyer, payment_subtype=payment_subtype, order_type=order_type, order_id=order_id)
            if use_action and callable(use_action):
                setattr(self, f'_{k}', action.perform)
                setattr(self, k, use_action)
            else:
                setattr(self, k, action.perform)


class NewebPayment(BasePayment):
    checkout = actions.NewebCheckout
    callback = actions.NewebCallback
    customer_redirect = actions.NewebCusRedirect


class EcpayPayment(BasePayment):
    checkout = actions.EcpayCheckout
    callback = actions.EcpayCallback
    customer_redirect = actions.EcpayCusRedirect


class CreditPayment(BasePayment):
    checkout = actions.CreditCheckout
    callback = actions.CreditCallback

    def use_checkout(self):
        data = self._checkout()
        order = self.callback(data)
        return {'url': f'{api_settings.DEFAULT_REDIRECT_URL}?{api_settings.DEFAULT_REDIRECT_QUERY}={order.id}'}
