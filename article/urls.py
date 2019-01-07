from django.urls import path
from .views import SearchView


app_name = 'article'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    # path('list/', ArticleListView.as_view(), name='article_list'),
]
