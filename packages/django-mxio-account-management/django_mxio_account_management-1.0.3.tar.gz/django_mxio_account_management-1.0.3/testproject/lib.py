from account_management.lib import AccountManagement
from django.urls import reverse


class CustomAccountManagement(AccountManagement):
	def get_default_authenticated_url(self):
		return reverse('auth')
