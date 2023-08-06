from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth import get_user_model, login, logout
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib import messages
from . import forms, models, lib


LIB = lib.get_lib()


class NoLoginFormView(FormView):
	""" if the user is logged in, redirect them! """
	def dispatch(self, *args, **kwargs):
		if not self.request.user.is_anonymous:
			return redirect(LIB.get_default_authenticated_url())
		return super().dispatch(*args, **kwargs)



class RegisterView(NoLoginFormView):
	template_name = 'account_management/register.html'
	form_class = forms.CreateAccountForm

	def form_valid(self, form):
		data = form.cleaned_data
		email = data.get('email')
		user = get_user_model().objects.create(email=email, username=email)
		acc_info = models.UserAccountInfo.objects.create(user=user)
		acc_info.generate_password_token()
		acc_info.save()
		LIB.post_register_hook(self.request, form, acc_info)
		return super().form_valid(form)
	
	def get_success_url(self):
		return LIB.get_register_success_url()
		

class LoginView(NoLoginFormView):
	template_name = 'account_management/login.html'
	form_class = forms.LoginForm

	def form_valid(self, form):
		data = form.cleaned_data
		email = data.get('email')
		user = get_user_model().objects.get(email=email)
		login(self.request, user)
		return super().form_valid(form)
	
	def get_success_url(self):
		return LIB.get_login_success_url(self.request)


class LogoutView(View):
	def get(self, *args, **kwargs):
		LIB.pre_logout_hook(self.request)
		logout(self.request)
		LIB.post_logout_hook(self.request)
		return redirect(LIB.get_logout_success_url())
		

class SetPasswordView(NoLoginFormView):
	template_name = 'account_management/set_password.html'
	form_class = forms.SetPasswordForm

	def dispatch(self, *args, **kwargs):
		reset_password_link = LIB.get_password_reset_link()
		if self.kwargs.get('token') is None:
			messages.add_message(self.request, messages.INFO, _('Unable to set your password.'))
			return redirect(reset_password_link)
		matches = models.UserAccountInfo.objects.filter(password_token=self.kwargs.get('token'))
		if not matches.exists():
			messages.add_message(self.request, messages.INFO, _('Unable to set your password.'))
			return redirect(reset_password_link)
		account_info = matches.first()
		if account_info.password_token is None or account_info.is_password_token_expired():
			messages.add_message(self.request, messages.INFO, _('Unable to set your password.'))
			return redirect(reset_password_link)
		return super().dispatch(*args, **kwargs)

	def get_form_kwargs(self, *args, **kwargs):
		account_info = get_object_or_404(models.UserAccountInfo, password_token=self.kwargs.get('token'))
		user = account_info.user
		kwargs = super().get_form_kwargs(*args, **kwargs)
		kwargs['instance'] = user
		return kwargs

	def form_valid(self, form):
		data = form.cleaned_data
		account_info = get_object_or_404(models.UserAccountInfo, password_token=self.kwargs.get('token'))
		user = account_info.user
		user.set_password(data['password'])
		user.save()
		account_info.password_token = None
		account_info.save()
		login(self.request, user)
		messages.add_message(self.request, messages.INFO, _('Your password has been saved.'))
		return super().form_valid(form)

	def get_success_url(self):
		return LIB.get_password_set_success_url()


class ResetPasswordView(NoLoginFormView):
	template_name = 'account_management/reset_password.html'
	form_class = forms.ResetPasswordForm

	def form_valid(self, form):
		data = form.cleaned_data
		email = data.get('email')
		user_matches = get_user_model().objects.filter(email=email)
		if user_matches.exists():
			user = user_matches.first()
			acc_info_matches = models.UserAccountInfo.objects.filter(user=user)
			if acc_info_matches.exists():
				acc_info = acc_info_matches.get()
			else:
				acc_info = models.UserAccountInfo.objects.create(user=user)
			acc_info.generate_password_token()
			LIB.post_password_reset_hook(self.request, acc_info)
			acc_info.save()

		return super().form_valid(form)
	
	def get_success_url(self):
		return LIB.get_password_reset_success_url()

