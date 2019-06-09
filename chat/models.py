from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Chat(models.Model):
    chat_id = models.PositiveIntegerField(primary_key=True)
    chat_name = models.CharField(max_length=250, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, related_name='invited_users')
    date = models.DateTimeField(auto_now_add=True, null=True)
    private = models.BooleanField(default=True)

    def __str__(self):
        invited_users = '\n'.join(user.username for user in self.invited.all())
        # return f'Комната{self.chat_id}, {self.admin}, участники: {invited_users}'
        return str(self.chat_id)


class Message(models.Model):
    chatid = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def short_time(self):
        return self.date.strftime("%d.%m.%y %H:%M:%S")

    def __str__(self):
        return f'Сообщение от {self.user}'
