from django.urls import path
from . import views


def get_urlpatterns(name_map):
	return [
		path(name_map['login'], views.LoginView.as_view(), name='login'),
		path(name_map['register'], views.RegisterView.as_view(), name='register'),
		path(name_map['set-password'], views.SetPasswordView.as_view(), name='set-password'),
		path(name_map['reset-password'], views.ResetPasswordView.as_view(), name='reset-password'),
		path(name_map['logout'], views.LogoutView.as_view(), name='logout'),
	]


urlpatterns = get_urlpatterns({
	'login': 'login/',
	'register': 'register/',
	'set-password': 'set-password/<str:token>/',
	'reset-password': 'reset-password/',
	'logout': 'logout/'
})
