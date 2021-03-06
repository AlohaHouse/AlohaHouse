from django import template
import pdb

register = template.Library()

'''template内で
    value = 配列名,c

    arg = 配列番号
    を引数とする配列の値を返す
'''
@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

'''for文を配列の回数分回すために必要'''
@register.filter(name='range')
def filter_range(start, array):
    return range(start, len(array))

'''for文（2回目）を配列の回数分回すために必要'''
@register.filter(name='range2')
def filter_range2(array,i):
    return range(0, len(array[i]))

'''template内で
    value = 配列名,
    arg1 = 配列番号1,
    arg2 = 配列番号2
    を引数とする配列の値を返す(2次元配列)'''
@register.simple_tag
def lookup2(value, arg1, arg2):
    return value[arg1][arg2]