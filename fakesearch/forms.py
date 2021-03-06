from django import forms
from fakesearch.models import Experiment, UserProfile, ResultList, Vote, EXPERTISE_CHOICES, LIST_PREFERENCE
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    expertise = forms.ChoiceField(widget=forms.RadioSelect, choices=EXPERTISE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ('expertise',)

class VoteForm(forms.ModelForm):
    preference = forms.ChoiceField(widget=forms.RadioSelect, choices=LIST_PREFERENCE)

    class Meta:
        model = Vote
        fields = ('preference',)

