from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets, time


class UserAccountInfo(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	password_token = models.CharField(max_length=32, null=True, blank=True, unique=True)
	password_token_created_at = models.IntegerField(null=True, blank=True)

	def generate_password_token(self):
		self.password_token = secrets.token_hex(16)
		self.password_token_created_at = int(time.time())
	
	def is_password_token_expired(self):
		if self.password_token_created_at is None: return True
		curr_time = int(time.time())
		seconds_elapsed = curr_time - self.password_token_created_at
		return seconds_elapsed > 60 * 60 * 24
