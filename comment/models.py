from django.db import models
from login.models import Users

class Posting(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    comments = models.CharField(max_length=700)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='comments'
# Create your models here.
