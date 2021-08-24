from django.utils import timezone
from django.views.generic.list import ListView
from publications.models import Article, UserFavouriteArticle
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import forms as auth_forms, views as auth_views
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.db.models import F, Value, ExpressionWrapper, fields
from django.db.models.functions import Now
from django.db.models.fields import DateTimeField, DurationField, BooleanField



class ArticleListView(ListView):
    model = Article
    def get_queryset(self):
        now = timezone.now()
        queryset = super(ArticleListView, self).get_queryset()
        duration = ExpressionWrapper(Value(now, DateTimeField()) - F('created'), output_field=fields.DurationField())
        queryset = queryset.annotate(duration=duration)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ArticleDetailView(DetailView):
    model = Article
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MyArticleListView(ListView):
    model = Article
    template_name = 'publications/article_list_my.html'
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publications'] = True
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy( 'login' )


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'synopsis', 'content']
    success_url = reverse_lazy( 'article-list' )
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddToFavorite(CreateView):
    model = UserFavouriteArticle
    fields = ['user', 'article']
    success_url = reverse_lazy( 'favorites' )
    
    def form_valid(self, form):
        return super().form_valid(form)


class FavoritesListView(ListView):
    model = UserFavouriteArticle
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
