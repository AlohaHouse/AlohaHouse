from django.urls import path
from .views import SearchRoutesView, SearchView, ArticleListView


app_name = 'article'

urlpatterns = [
    path('search/routes', SearchRoutesView.as_view(), name='search_routes'),
    path('search/', SearchView.as_view(), name='search'),
    path('list/', ArticleListView.as_view(), name='list'),
]
