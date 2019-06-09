from django import forms
from django.contrib.auth.models import User
from django.forms import CheckboxSelectMultiple


class ChatForm(forms.Form):
    print(User.objects.all().values_list('username'))
    text = forms.CharField(max_length=500)

class CreateConferenceForm(forms.Form):
    # An initial queryset is required, this is overwritten in the view
    chatname = forms.CharField(max_length=500)
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all())