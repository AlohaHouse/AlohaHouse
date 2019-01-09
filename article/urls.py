from django.urls import path
from .views import SearchView, ResultView


app_name = 'article'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    # path('list/', ArticleListView.as_view(), name='article_list'),
    path('result/', ResultView.as_view(), name='result'),
]
