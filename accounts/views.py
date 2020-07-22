from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
import datetime

from django.contrib.auth import get_user_model
from .mixins import AictiveUserRequiredMixin, AictiveBidderRequiredMixin, AictiveSellerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import SignUpForm, UserForm, ProfileForm
from accounts.models import Profile


from django.views import View, generic

# Create your views here.


class HomeLoginView(LoginView):
    template_name = 'landing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AuctionBd'
        return context

    def render_to_response(self, context):
        if self.request.user.is_authenticated and self.request.user.user_profile.active and self.request.user.user_profile.email_confirmed and (self.request.user.user_profile.user_type == '1' or self.request.user.user_profile.user_type == '2'):
            return redirect('accounts:dashboard_view')
        return super().render_to_response(context)


class RegisterView(View):
    def get(self, request, *args, **kwrags):
        signup_form = SignUpForm()
        context = {
            'signup_form': signup_form,
            'title': 'Register'
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwrags):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.refresh_from_db()
            user.user_profile.phone_number = signup_form.cleaned_data.get(
                'phone_number')
            user.user_profile.user_type = request.POST.get('user_type')
            user.save()
            user.user_profile.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(
                request, ('Registration Completed.Please Confirm Your Email Address'))
            return redirect('home_login')
        else:
            context = {
                'signup_form': signup_form,
                'title': 'Register'
            }
            return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.user_profile.email_confirmed = True
        user.user_profile.save()
        messages.success(
            request, ('Thank You For Confirm The Email.Your Account Will Be Activated Soon'))
        return redirect('home_login')
    else:
        messages.success(request, ('Activation link is invalid!'))
        return redirect('home_login')


class MyProfileView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.user_profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'My Profile'
        }
        return render(request, 'accounts/my_profile.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST,
                             instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:my_profile')
        else:

            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'title': 'My Profile'
            }
            return render(request, 'accounts/my_profile.html', context)


class ChangePasswordView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        password_changeform = PasswordChangeForm(request.user)
        context = {
            'chanage_password_form': password_changeform,
            'title': 'Change Password'
        }
        return render(request, 'accounts/change_password.html', context)

    def post(self, request, *args, **kwargs):
        chanage_password_form = PasswordChangeForm(
            data=request.POST, user=request.user)
        context = {
            'chanage_password_form': chanage_password_form,
            'title': 'Change Password'
        }
        if chanage_password_form.is_valid():
            chanage_password_form.save()
            update_session_auth_hash(request, chanage_password_form.user)
            messages.success(request, 'You have Changed Your Password...')
            return redirect('accounts:change_password')
        else:
            return render(request, 'accounts/change_password.html', context)


class DashboardView(View):
    def get(self, request, *args, **kwrags):
        """
        Redirects users based on whether they are in the admins group
        """
        if request.user.user_profile.user_type == '1':
            return redirect("accounts:bidder_dashboard")
        elif request.user.user_profile.user_type == '2':
            return redirect("accounts:seller_dashboard")
        elif request.user.is_superuser:
            return redirect('admin:login')
        else:
            return redirect("home_login")


class BidderDashboardView(AictiveBidderRequiredMixin, View):
    def get(self, request, *args, **kwrags):
        user_obj = get_object_or_404(get_user_model(), id=request.user.id)
        user_profile = user_obj.user_profile

        context = {
            'title': 'Bidder Dashboard',
            'user_obj': user_obj,
            'user_profile': user_profile,
        }

        return render(request, 'accounts/bidder_dashboard.html', context)


class SellerDashboardView(AictiveSellerRequiredMixin, View):
    def get(self, request, *args, **kwrags):
        user_obj = get_object_or_404(get_user_model(), id=request.user.id)
        user_profile = user_obj.user_profile

        context = {
            'title': 'Bidder Dashboard',
            'user_obj': user_obj,
            'user_profile': user_profile,
        }

        return render(request, 'accounts/seller_dashboard.html', context)
