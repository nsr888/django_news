from django.urls import path

from publications.views import ArticleListView, RegisterView, ArticleCreateView, MyArticleListView, ArticleDetailView, AddToFavorite, FavoritesListView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('articles/', permanent=False), name='home'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('publications/', MyArticleListView.as_view(), name='my-article-list'),
    path('register/', RegisterView.as_view(), name='registration'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('addtofavorite/', AddToFavorite.as_view(), name='add-to-favorite'),
    path('favorites/', FavoritesListView.as_view(), name='favorites'),
]
