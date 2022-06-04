from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_basic, name='search_basic'),
    path('recommend', views.search_recommend, name='search_recommend'),
    path('search-by-case', views.search_by_case, name='search_by_case'),
]