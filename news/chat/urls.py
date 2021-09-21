from django.urls import path
from .views import ChatListView, ChatDetailView, ChatRoomCreateView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-list'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('create/', ChatRoomCreateView.as_view(), name='chat-create'),
]
