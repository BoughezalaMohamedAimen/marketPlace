import re

from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from cart.models import *
from datetime import datetime, timedelta
from django.utils import timezone

class CartMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        try:
            Cart.objects.filter(created_at__lte=timezone.now() - timedelta(days=3),user='null').delete()
        except:
            pass

        if request.user.is_authenticated:
            try:
                cart=Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                cart = Cart(user=request.user)
                cart.save()
        else:
            if not request.session.session_key:
                request.session.save()
            try:
                cart=Cart.objects.get(session_key = request.session.session_key)
            except Cart.DoesNotExist:
                cart = Cart(session_key=request.session.session_key)
                cart.save()
