from django.contrib import admin
from user.models import User
from user.forms import UserCreationForm

admin.site.register(User)