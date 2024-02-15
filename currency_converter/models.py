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


class CurrencyConversion(models.Model):
    from_currency = models.CharField(max_length=5)
    to_currency = models.CharField(max_length=5)
    rate = models.DecimalField(max_digits=32, decimal_places=2)
    name = models.CharField(max_length=25)

    def __lt__(self, other):
        return self.rate < other.rate

    def __eq__(self, other):
        return self.rate == other.rate
