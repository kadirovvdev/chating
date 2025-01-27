from django.db import models
# from django.contrib.auth.models import User
from django.db.models import Max
from users.models import CustomUser


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # Sender Message Function
    def send_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
            )
        # Reciepient Message Function
        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
            )
        recipient_message.save()

        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values("recipient").annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': CustomUser.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient_pk=message['recipient'], is_read=False).count()
            })
        return users

