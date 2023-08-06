from rest_framework import viewsets, response, permissions, exceptions, views
from revpayment.carts import Cart
from rest_framework.decorators import action
from revpayment.settings import api_settings
from revpayment.models import RedirectState
from django.shortcuts import redirect
from django.contrib.auth.models import User
import jwt
import json
from revpayment.checkout import check_certificate

verify_token_method = api_settings.VERIFY_METHOD


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    add_item_path = 'item/add'
    edit_item_path = 'item/edit'
    delete_item_path = 'item/delete'
    edit_config_path = 'config/edit'
    clear_path = 'clear'
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def list(self, request):
        cart = self.get_cart()
        return response.Response(cart.cart, 200)

    @action(detail=False, url_path=clear_path, methods=['POST'])
    def clear(self, request):
        cart = self.get_cart()
        cart.clear_cart()
        return response.Response(cart.cart, 200)

    @action(detail=False, url_path=add_item_path, methods=['POST'])
    def add_item(self, request):
        cart = self.get_cart()
        item = self.request.data
        cart.add_item(item)
        return response.Response(cart.cart, 200)

    @action(detail=False, url_path=edit_item_path, methods=['POST'])
    def edit_item(self, request):
        cart = self.get_cart()
        data = self.request.data
        if 'index' not in data:
            raise exceptions.ValidationError(
                code='index_is_required', detail='index is required')
        if not data.get('config'):
            raise exceptions.ValidationError(
                code='config_is_required', detail='config is required')
        cart.edit_item(index=data['index'], config=data['config'])
        return response.Response(cart.cart, 200)

    @action(detail=False, url_path=delete_item_path, methods=['POST'])
    def delete_item(self, request):
        cart = self.get_cart()
        data = self.request.data
        if 'index' not in data:
            raise exceptions.ValidationError(
                code='index_is_required', detail='index is required')
        cart.delete_item(index=data['index'])
        return response.Response(cart.cart, 200)

    @action(detail=False, url_path=edit_config_path, methods=['POST'])
    def edit_config(self, request):
        cart = self.get_cart()
        data = self.request.data
        cart.edit_config(data)
        return response.Response(cart.cart, 200)


class CheckoutView(views.APIView):
    permission_classes = []
    redirect_base = api_settings.WEB_HOST
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get(self, request):
        token = self.request.query_params.get('token')
        token_type = self.request.query_params.get('token_type')
        payment_type = self.request.query_params.get('payment_type', 'neweb')
        payment_subtype = self.request.query_params.get(
            'payment_subtype', 'default')
        if not token:
            raise exceptions.ValidationError(code='token_required')
        if token_type == 'token':
            try:
                user = User.objects.get(auth_token__key=token)
                profile = user.profile
            except:
                raise exceptions.PermissionDenied
        else:
            profile = verify_token_method(token)
        state = RedirectState.objects.create(
            buyer_id=profile.id,
            redirect_url=self.redirect_base,
            payment_type=payment_type,
            payment_subtype=payment_subtype,
            cart=profile.payment.cart
        )
        sdk = self.sdk_class(state=state)
        return sdk.checkout()


class CallbackView(views.APIView):
    permission_classes = []
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def post(self, request):
        data = request.data
        state, data = check_certificate(data['certificate'])
        sdk = self.sdk_class(state=state)
        return sdk.callback(data)


class ClientRedirect(views.APIView):
    permission_classes = ()
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get(self, request):
        cert = request.query_params.get('certificate')
        state, data = check_certificate(cert)
        client = self.sdk_class(state=state)
        url = client.customer_redirect(data)
        return url

    def post(self, request):
        state, data = check_certificate(request.data['certificate'])
        client = self.sdk_class(state=state)
        url = client.customer_redirect(data)
        return url


class CartView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def get(self, request):
        cart = self.get_cart()
        return response.Response(cart.cart, 200)


class ClearCartView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def post(self, request):
        cart = self.get_cart()
        cart.clear_cart()
        return response.Response(cart.cart, 200)


class AddItemView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def post(self, request):
        cart = self.get_cart()
        cart.add_item(request.data)
        return response.Response(cart.cart, 200)


class EditItemView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def post(self, request):
        cart = self.get_cart()
        data = self.request.data
        if 'index' not in data:
            raise exceptions.ValidationError(
                code='index_is_required', detail='index is required')
        if not data.get('config'):
            raise exceptions.ValidationError(
                code='config_is_required', detail='config is required')
        cart.edit_item(index=data['index'], config=data['config'])
        return response.Response(cart.cart, 200)


class DeleteItemView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def post(self, request):
        cart = self.get_cart()
        data = self.request.data
        if 'index' not in data:
            raise exceptions.ValidationError(
                code='index_is_required', detail='index is required')
        cart.delete_item(index=data['index'])
        return response.Response(cart.cart, 200)


class EditConfigView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get_cart(self):
        return self.cart_class(self.request.user.profile)

    def post(self, request):
        cart = self.get_cart()
        data = self.request.data
        cart.edit_config(data)
        return response.Response(cart.cart, 200)


class CreditView(views.APIView):
    permission_classes = ()
    item_class = api_settings.ITEM_CLASS
    calc_class = api_settings.CALC_CLASS
    redirect_base = api_settings.WEB_HOST
    cart_class = api_settings.DEFAULT_CART_CLASS
    sdk_class = api_settings.DEFAULT_SDK_CLASS

    def get(self, request):
        credit = self.request.query_params.get('credit')
        token_type = self.request.query_params.get('token_type')
        token = self.request.query_params.get('token')
        payment_type = self.request.query_params.get('payment_type', 'neweb')
        payment_subtype = self.request.query_params.get('payment_subtype', 'credit')
        if token_type == 'token':
            try:
                user = User.objects.get(auth_token__key=token)
                profile = user.profile
            except:
                raise exceptions.PermissionDenied
        else:
            profile = verify_token_method(token)

        credit = int(credit) if type(credit) is str else credit
        item = self.item_class.get_credit_item(credit)
        cart = self.cart_class(profile)
        config = cart.cart['config']
        calc = self.calc_class(items=[item], profile=profile, config=cart.cart['config'])

        cart_data = {'config': config, 'calculations': calc.get_calc_dict(), 'items': [item]}
        state = RedirectState.objects.create(
            order_type='credit',
            cart=json.dumps(cart_data, ensure_ascii=False),
            buyer=profile,
            payment_type=payment_type,
            payment_subtype=payment_subtype
        )

        sdk = self.sdk_class(state=state)
        return sdk.checkout()
