from django.urls import path
from .views import ChatListView, ChatDetailView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
]

