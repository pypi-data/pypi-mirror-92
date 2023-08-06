from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages


class AccountManagement:
	ACCOUNT_CONFIRMATION_SUBJECT = ugettext_lazy('Account Confirmation')
	USER_ALREADY_EXISTS_MESSAGE = ugettext_lazy('User with this email already exists.')
	OVERRIDE_STRINGS = {}
	DEFAULT_STRINGS = {
		'ACCOUNT_CONFIRMATION_EMAIL_SUBJECT': lambda params: ugettext_lazy('Account Confirmation' % params),
		'ACCOUNT_CONFIRMATION_EMAIL_TEXT': lambda params: ugettext_lazy('Welcome! You can activate your account and log in at this link: %(link)s' % params),
		'ACCOUNT_CONFIRMATION_SUCCESS_MESSAGE': lambda params: ugettext_lazy('Your account has been created. Please check your email for instructions on how to log in.'),
		'PASSWORD_RESET_EMAIL_SUBJECT': lambda params: ugettext_lazy('Password Reset'),
		'PASSWORD_RESET_EMAIL_TEXT': lambda params: ugettext_lazy('You can reset your password at this link: %(link)s' % params),
		'PASSWORD_RESET_SUCCESS_MESSAGE': lambda params: ugettext_lazy('Please check your email to continue with your password reset'),
	}
	URL_NAMESPACE = 'account_management'

	def __init__(self):
		# SANITY CHECK !!!!
		if not hasattr(settings, 'BASE_URL'):
			raise Exception('settings.py must set BASE_URL')

	def _get_string(self, key, params=None):
		if params is None: params = {}
		if key in type(self).OVERRIDE_STRINGS:
			return type(self).OVERRIDE_STRINGS[key](params)
		else:
			return type(self).DEFAULT_STRINGS[key](params)
	
	def _get_full_name_from_namespace(self, name):
		return type(self).URL_NAMESPACE + ':' + name
	
	def get_password_set_link(self, account_info):
		""" returns the link where a user should go to set their password """
		return settings.BASE_URL + reverse(self._get_full_name_from_namespace('set-password'), kwargs={'token': account_info.password_token})
	
	def get_password_reset_link(self):
		""" returns the link where a user should go to reset their password """
		return settings.BASE_URL + reverse(self._get_full_name_from_namespace('reset-password'))
	
	def get_password_set_success_url(self):
		""" where do we send the user after they set their password? """
		return reverse(self._get_full_name_from_namespace('login'))
	
	def get_password_reset_success_url(self):
		""" where do we send the user after they submit a password reset request? """
		return reverse(self._get_full_name_from_namespace('reset-password'))
	
	def get_register_success_url(self):
		""" where do we send the user after they submit their registration? """
		return reverse(self._get_full_name_from_namespace('login'))
	
	def get_login_success_url(self, request):
		""" where do we send the user after they successfully login? """
		if 'next' in request.GET:
			return request.GET.get('next')
		return reverse(self._get_full_name_from_namespace('login'))
	
	def get_logout_success_url(self):
		""" where do we send the user after they successfully logout? """
		return reverse(self._get_full_name_from_namespace('login'))
	
	def get_default_authenticated_url(self):
		""" if the user visits an auth page (like login) while they're authenticated, where do we send them? """
		raise Exception('This must be implemented!')

	def pre_logout_hook(self, request):
		""" executed before the user is logged out """
		pass
	
	def post_logout_hook(self, request):
		""" executed after the user is logged out """
		pass
	
	def post_register_hook(self, request, form, account_info):
		""" executed after the user is registered
		- account_info: account_management.models.UserAccountInfo """
		subject = self._get_string('ACCOUNT_CONFIRMATION_EMAIL_SUBJECT')
		from_email = None # uses settings.DEFAULT_FROM_EMAIL by default
		text_content = self._get_string('ACCOUNT_CONFIRMATION_EMAIL_TEXT', {
			'link': self.get_password_set_link(account_info)
		})
		html_content = render_to_string('account_management/emails/account_confirmation.html', {
			'link': self.get_password_set_link(account_info)
		})
		email = account_info.user.email
		message = EmailMultiAlternatives(subject, text_content, from_email, [email])
		message.attach_alternative(html_content, 'text/html')
		message.send()
		messages.add_message(request, messages.INFO, self._get_string('ACCOUNT_CONFIRMATION_SUCCESS_MESSAGE'))
	
	def post_password_reset_hook(self, request, account_info):
		""" executed after a successful password reset (this is where the email would be delivered """
		# send password reset email
		subject = self._get_string('PASSWORD_RESET_EMAIL_SUBJECT')
		from_email = None # uses settings.DEFAULT_FROM_EMAIL by default
		text_content = self._get_string('PASSWORD_RESET_EMAIL_TEXT', {
			'link': self.get_password_set_link(account_info)
		})
		html_content = render_to_string('account_management/emails/password_reset.html', {
			'link': self.get_password_set_link(account_info)
		})
		email = account_info.user.email
		message = EmailMultiAlternatives(subject, text_content, from_email, [email])
		message.attach_alternative(html_content, 'text/html')
		message.send()
		messages.add_message(request, messages.INFO, self._get_string('PASSWORD_RESET_SUCCESS_MESSAGE'))


def get_lib():
	if hasattr(settings, 'MXIO_ACCOUNT_MANAGEMENT_CLASS'):
		return import_string(settings.MXIO_ACCOUNT_MANAGEMENT_CLASS)()
	return AccountManagement()
