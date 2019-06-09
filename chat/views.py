import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from django.views import View

from chat.forms import ChatForm
from chat.models import Chat, Message


@login_required(login_url='/login/')
def index(request):
    return render(request, 'chat/index.html', {})

@login_required(login_url='/login/')
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

@login_required(login_url='/login/')
def showusers(request):
    users = User.objects.all().exclude(id=request.user.id)
    for user in users:
        chat = Chat.objects.filter(invited=user).filter(invited=request.user.id)
        if chat.values():
            user.chat_id = chat.values()[0]['chat_id']
    groups = Chat.objects.filter(invited=request.user.id).filter(private=False)
    return render(request, 'chat/index.html', {'users': users, 'groups': groups})


class CreateRoom(View):
    form_class = ChatForm
    template_name = 'chatapp/room.html'

    def get(self, request, user):
        form = self.form_class
        chat = Chat.objects.filter(invited=user).filter(invited=request.user.id)
        if chat.values():
            messages = Message.objects.filter(chat=chat.values()[0]['chat_id']).order_by('date')
        else:
            user1 = User.objects.get(pk=user)
            user2 = User.objects.get(pk=request.user.id)
            while True:
                id = random.randint(0, 999999)
                if not Chat.objects.filter(pk=id).exists():
                    chat = Chat(chat_id=id, admin=user2)
                    break
            print(chat.date)
            chat.save()
            chat.invited.add(user1)
            chat.invited.add(user2)
            messages = []
        return redirect(f'/chat/{chat.chat_id}')
        # return render(request, self.template_name, {'messages': messages, 'form': form, 'chat': chat})


class ShowRoom(View):
    form_class = ChatForm
    template_name = 'chat/room.html'

    def get(self, request, chatid):
        if Chat.objects.filter(chat_id=chatid).filter(invited=request.user.id).exists():
            form = self.form_class
            chat = Chat.objects.get(chat_id=chatid)
            print(chat)
            messages = Message.objects.filter(chatid=chatid).order_by('date')
            private_user = chat.invited.exclude(id=request.user.id)[0]
            return render(request, self.template_name, {'messages': messages, 'form': form, 'chat': chat, 'private':private_user, 'room_name_json': mark_safe(json.dumps(chatid)) })
        else:
            return HttpResponse('<h1> Access denied </h1>')

    def post(self, request, chatid):
        if request.POST['text'] != '':
            Message.objects.create(chatid=Chat.objects.get(chat_id=chatid),
                                   user_id=request.user.id,
                                   text=request.POST['text'],
                                   )
            return redirect(f'/chat/{chatid}')
        else:
            pass