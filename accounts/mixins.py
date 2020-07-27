from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json


class AictiveUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_profile.active and request.user.user_profile.email_confirmed:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Login Or May Be Your Account Is Not Active Or Not A Valid User'))
            return redirect('home_login')


class AictiveBidderRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_profile.active and request.user.user_profile.email_confirmed and request.user.user_profile.user_type == '1':
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('You Are Not Bidder'))
            return redirect('home_login')


class AictiveSellerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_profile.active and request.user.user_profile.email_confirmed and request.user.user_profile.user_type == '2':
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Login Or May Be Your Account Is Not Active Or Not A Valid User'))
            return redirect('You Are Not Seller')


class UserHasPaymentSystem:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_payment_credit_card.all().count() != 0:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Add Payment'))
            return redirect('accounts:add_credit_card')
