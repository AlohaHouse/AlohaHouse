from django.db import models
from AlohaHouse.constants import INPUT_TYPE


# 路線企業
class Company(models.Model):
    name = models.CharField('企業名', max_length=20, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name


# 路線
class Route(models.Model):
    company = models.ForeignKey(
        Company, verbose_name='企業名', on_delete=models.PROTECT,
    )
    name = models.CharField('路線名', max_length=20, blank=True)
    color_code = models.CharField('カラーコード', max_length=20, blank=True)
    eng_name = models.CharField('英語名', max_length=20, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name


# 駅
class Station(models.Model):
    route = models.ForeignKey(
        Route, verbose_name='路線名', on_delete=models.PROTECT,
    )
    name = models.CharField('駅名', max_length=20, blank=True)
    code = models.CharField('駅コード', max_length=20, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name


# こだわり条件グループ
class ConditionsGroup(models.Model):
    name = models.CharField('グループ名', max_length=20)
    sort = models.IntegerField('ソート順')
    is_active = models.BooleanField('使用中', default=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name


# こだわり条件
class Condition(models.Model):
    name = models.CharField('条件名', max_length=20)
    # HTML表示のinputのtype属性
    input_type = models.IntegerField('inputのtype属性', choices=INPUT_TYPE)
    input_name = models.CharField('inputのname属性', max_length=10)
    sort = models.IntegerField('ソート順')
    is_active = models.BooleanField('使用中', default=True)
    condition_group = models.ForeignKey(
        ConditionsGroup, verbose_name='グループ名', on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    
    def __str__(self):
        return self.name


# こだわり条件の値
class ConditionValue(models.Model):
    name = models.CharField('値の名称', max_length=20)
    code = models.code = models.CharField('コード', max_length=20)
    input_name = models.CharField('inputのname属性', max_length=10)
    is_default = models.IntegerField('デフォルト設定', default=0)
    sort = models.IntegerField('ソート順')
    condition = models.ForeignKey(
        Condition, verbose_name='条件名', on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name
