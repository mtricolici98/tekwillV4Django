from django.db import models

# Create your models here.


class Product(models.Model):

    code = models.BigIntegerField()
    name = models.TextField()
    quantity = models.IntegerField()

