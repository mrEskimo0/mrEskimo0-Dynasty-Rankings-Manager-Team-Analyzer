from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class Insert_ID(forms.Form):
    Sleeper_League_ID = forms.CharField()
    Sleeper_Display_Name = forms.CharField()

class User_Ranking_Form(ModelForm):

    rank_choices = (
        ('Consensus Superflex', 'Consensus Superflex'),
        ('Consensus Standard', 'Consensus Standard')
    )

    choose_ranks = forms.ChoiceField(choices=rank_choices)
    tags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Tag.objects.all())
    class Meta:
        model = User_Ranking
        fields = ['name','tags','choose_ranks']


class User_Insert_ID(ModelForm):
    class Meta:
        model = League
        fields = ['name','league_id','user_ranking','draft_order']

    # def __init__(self, *args, **kwargs):
    #     # print(kwargs)
    #     user = kwargs.pop('user', None)
    #
    #     super(User_Insert_ID, self).__init__(*args, **kwargs)

        # if user is not None:
        #     self.fields['user_ranking'].queryset = User_Ranking.objects.filter(user=user)
        # else:
        #     self.fields['user_ranking'].queryset = User_Ranking.objects.none()
        # self.fields['user_ranking'].queryset = User_Ranking.objects.filter(user=user)

class Create_User_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
        'required':'',
        'class':'form-control',
        'placeholder':'john dice'
        })
        self.fields['email'].widget.attrs.update({
        'required':'',
        'class':'form-control',
        'placeholder':'johndice16@gmail.com'
        })
        self.fields['password1'].widget.attrs.update({
        'required':'',
        'class':'form-control',
        'placeholder':'password'
        })
        self.fields['password2'].widget.attrs.update({
        'required':'',
        'class':'form-control',
        'placeholder':'password'
        })


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
