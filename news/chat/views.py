from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import ChatRoom, Message
from django.urls import reverse_lazy


class ChatListView(ListView):
    model = ChatRoom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ChatDetailView(DetailView):
    model = ChatRoom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages_out'] = reversed(Message.objects.filter(chatroom=self.object).order_by('-created')[:3])
        return context


class ChatRoomCreateView(CreateView):
    model = ChatRoom
    fields = ["title"]
    success_url = reverse_lazy("chat-list")
