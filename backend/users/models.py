from django.contrib.auth.models import AbstractUser
from django.db import models as m

# Create your models here.

class Role(m.Model):
    name = m.CharField('Role', max_length=10)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = m.ForeignKey(Role, on_delete=m.CASCADE, default=1)

