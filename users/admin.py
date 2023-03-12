from django.contrib import admin
from .models import User, Address, Country, Province, City, RequestLog, Notification
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    exclude = ('password',)


class CityAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]
    list_display = [
        "name",
    ]


admin.site.register(Address)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(RequestLog)
admin.site.register(Notification)
admin.site.register(City, CityAdmin)

admin.site.register(User, UserAdmin)
