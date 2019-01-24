from django.contrib import admin
from .models import (
    Company,
    Route,
    Station,
    ConditionsGroup,
    Condition,
    ConditionValue
)


# 駅
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('route','name',)


# 追加条件グループ
@admin.register(ConditionsGroup)
class ConditionValueAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')


# 追加条件
@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('condition_group','input_name', 'name','is_active')


# 追加条件のvalue
@admin.register(ConditionValue)
class ConditionValueAdmin(admin.ModelAdmin):
    list_display = ('condition','name', 'code')


# class RouteAdmin(admin.ModelAdmin):
#     list_display = ('name','company')


admin.site.register(Company)
admin.site.register(Route)


