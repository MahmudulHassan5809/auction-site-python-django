from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import datetime


from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import AictiveUserRequiredMixin, AictiveBidderRequiredMixin, AictiveSellerRequiredMixin, UserHasPaymentSystem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm

from accounts.models import Profile, PaymentCreditCard


from auction.models import Product, SubCategory, AuctionDate, AuctionSession
from auction.forms import ProductForm

from django.views import View, generic
# Create your views here.


def load_sub_categories(request):
    category_id = request.GET.get('category')
    sub_categories = SubCategory.objects.filter(
        category_id=category_id)
    return render(request, 'product/subcategories_dropdown_list_options.html', {'sub_categories': sub_categories})


def load_auction_session(request):
    auction_date_id = request.GET.get('auction_date')
    auction_session = AuctionSession.objects.filter(
        auction_date=auction_date_id)
    return render(request, 'product/auction_session_dropdown_list_options.html', {'auction_session': auction_session})


class ProductListView(AictiveSellerRequiredMixin, UserHasPaymentSystem, generic.ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'product/product_list.html'

    def get_queryset(self):
        qs = Product.objects.select_related(
            'category', 'sub_category', 'owner').filter(owner=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product List'
        return context


class AddProductView(AictiveSellerRequiredMixin, UserHasPaymentSystem, SuccessMessageMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/add_product.html'
    success_message = 'Product Added SuccessFully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Product'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EditProductView(AictiveSellerRequiredMixin, UserHasPaymentSystem, SuccessMessageMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/edit_product.html'
    success_message = 'Product Update SuccessFully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Product'
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeleteProductView(AictiveSellerRequiredMixin, UserHasPaymentSystem, SuccessMessageMixin, generic.edit.DeleteView):
    model = Product
    template_name = 'payment/delete_product.html'
    success_message = 'Product Deleted SuccessFully'
    success_url = reverse_lazy('auction:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Product'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteCreditCardView, self).delete(request, *args, **kwargs)
