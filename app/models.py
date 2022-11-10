from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
PW_TYPES = [('confidential', 'confidential'), ('sharable', 'sharable')]

class UserPW(models.Model):
    title = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=PW_TYPES, max_length=20)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    

    def __str__(self):
        return self.title


