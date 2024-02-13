from django.db import models


# Create your models here.
class ConversionHistory(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=32, decimal_places=2)

    def __repr__(self):
        return f"{self.timestamp} - {self.currency} - {self.amount}"

    def __str__(self):
        return repr(self)
