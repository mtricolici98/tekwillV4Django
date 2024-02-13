from django.contrib import admin

from currency_converter.models import ConversionHistory


# Register your models here.
class ConversionHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(ConversionHistory, ConversionHistoryAdmin)
