from django.urls import path
from .views import SearchRoutesView, SearchView, ResultView



app_name = 'article'

urlpatterns = [
    path('search/routes', SearchRoutesView.as_view(), name='search_routes'),
    path('search/', SearchView.as_view(), name='search'),
    path('result/', ResultView.as_view(), name='result'),
]
