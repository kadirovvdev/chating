# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from users.models import CustomUser


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages
    }
    return render(request, 'direct/inbox.html', context)


def directs(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'active_direct': active_direct,
        'messages': messages
    }
    return render(request, 'direct/directs.html', context)


def send__message(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        try:
            to_user = CustomUser.objects.get(username=to_user_username)
        except CustomUser.DoesNotExist:
            return redirect('inbox')
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')


def user_search(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = CustomUser.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
        context = {
            'users': users_paginator
        }

    return render(request, 'direct/inbox.html', context)


def new_message(request, username):
    from_user = request.user
    body = 'hello'
    try:
        to_user = CustomUser.objects.get(username=username)
    except Exception as e:
        return redirect('inbox')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')


