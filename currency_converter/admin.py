from django.contrib import admin

from currency_converter.models import ConversionHistory, CurrencyConversion


# Register your models here.
class ConversionHistoryAdmin(admin.ModelAdmin):
    pass


class ConversionAdmin(admin.ModelAdmin):
    pass


admin.site.register(ConversionHistory, ConversionHistoryAdmin)
admin.site.register(CurrencyConversion, ConversionAdmin)
