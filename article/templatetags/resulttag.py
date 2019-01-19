from django import template
register = template.Library()

'''template内で
    value = 配列名,
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