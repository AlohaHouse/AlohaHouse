from django.contrib import admin
from .models import Company, Route, Station

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('route','name',)

# class RouteAdmin(admin.ModelAdmin):
#     list_display = ('name','company')


admin.site.register(Company)
admin.site.register(Route)
