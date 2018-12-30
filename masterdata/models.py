from django.db import models

class Company(models.Model):
    name = models.CharField('企業名', max_length=20, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    company = models.ForeignKey(
        Company, verbose_name='企業名', on_delete=models.PROTECT,
    )
    name = models.CharField('路線名', max_length=20, blank=True)
    color_code = models.CharField('カラーコード', max_length=20, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.name

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
