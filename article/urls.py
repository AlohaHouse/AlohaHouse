from django.urls import path
from .views import SearchRoutesView, ResultView



app_name = 'article'

urlpatterns = [
    path('search/routes', SearchRoutesView.as_view(), name='search_routes'),
    path('result/', ResultView.as_view(), name='result'),
]
