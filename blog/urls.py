from django.urls import path

from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('create/', views.ArticleCreateView.as_view(), name='article-create'),
]
