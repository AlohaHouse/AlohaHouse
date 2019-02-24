from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class History(models.Model):
    url = models.CharField('スーモのURL',max_length=250)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    user = models.ForeignKey(
        User, verbose_name='企業名', on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.url


class Favorite(models.Model):
    url = models.CharField('スーモの詳細URL',max_length=150)
    name = models.CharField('物件名', max_length=50)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    user = models.ForeignKey(
        User, verbose_name='企業名', on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name