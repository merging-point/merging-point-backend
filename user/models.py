from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from parkinglot.models import Parkinglot


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(max_length=30, null=False, unique=True)
    disability_grade = models.IntegerField(null=False)
    name = models.CharField(max_length=4, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    parked_at = models.IntegerField(default=-1, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('user')
        ordering = ('-date_joined', )

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_superuser
