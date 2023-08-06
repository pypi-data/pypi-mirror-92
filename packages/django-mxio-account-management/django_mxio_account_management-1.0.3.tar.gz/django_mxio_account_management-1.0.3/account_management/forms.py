from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy
from django.core.exceptions import ValidationError
from . import lib


LIB = lib.get_lib()


class CreateAccountForm(forms.ModelForm):
	def clean_email(self):
		email = self.cleaned_data.get('email').lower()

		if get_user_model().objects.filter(email__iexact=email).exists():
			raise forms.ValidationError(LIB.USER_ALREADY_EXISTS_MESSAGE)

		return email
	
	class Meta:
		fields = [
			'email',
		]
		model = get_user_model()


class LoginForm(forms.Form):
	email = forms.EmailField(label=ugettext_lazy('Email'))
	password = forms.CharField(
		label=ugettext_lazy('Password'),
		widget=forms.PasswordInput()
	)

	def clean(self):
		cleaned_data = super().clean()
		matches = get_user_model().objects.filter(email__iexact=cleaned_data['email'].lower())
		if not matches.exists():
			raise ValidationError(ugettext_lazy('Please enter a valid email / password combination'))
		user = matches.first()
		if not user.check_password(cleaned_data['password']):
			raise ValidationError(ugettext_lazy('Please enter a valid email / password combination'))


class SetPasswordForm(forms.ModelForm):
	password_confirm = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = get_user_model()
		fields = [
			'password',
		]
		widgets = {
			'password': forms.PasswordInput()
		}
	
	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data['password'] != cleaned_data['password_confirm']:
			raise forms.ValidationError(ugettext_lazy('Passwords must match'))
		return cleaned_data


class ResetPasswordForm(forms.Form):
	email = forms.EmailField()
