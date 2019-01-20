from django.contrib import admin
from .models import (
    Company,
    Route,
    Station,
    ConditionsGroup,
    Condition,
    ConditionValue
)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('route','name',)


@admin.register(ConditionsGroup)
class ConditionValueAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('condition_group','name','is_active')


@admin.register(ConditionValue)
class ConditionValueAdmin(admin.ModelAdmin):
    list_display = ('condition','name', 'input_name','code')


# class RouteAdmin(admin.ModelAdmin):
#     list_display = ('name','company')


admin.site.register(Company)
admin.site.register(Route)


