from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class AuthView(TemplateView):
	template_name = 'auth.html'

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_anonymous:
			return redirect(reverse('account_management:login'))
		return super().dispatch(*args, **kwargs)
	
	def get_context_data(self, *args, **kwargs):
		ctx = super().get_context_data(*args, **kwargs)
		ctx['user'] = self.request.user
		return ctx

