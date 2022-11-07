import django_filters
from django_filters import CharFilter, NumberFilter, MultipleChoiceFilter
from django import forms
from .models import *

class Position(models.TextChoices):
    QB = 'QB'
    WR = 'WR'
    RB = 'RB'
    TE = 'TE'
    Pick = 'Pick'

CHOICES = (
    ('QB', 'QB'),
    ('WR', 'WR'),
    ('RB', 'RB'),
    ('TE', 'TE'),
    ('Pick', 'Pick'),
)

class RankingFilter(django_filters.FilterSet):
    position = MultipleChoiceFilter(field_name='player__position', choices=CHOICES, widget=forms.CheckboxSelectMultiple(attrs={'class':'try_checkbox'}), initial=[c[0] for c in CHOICES])

    name = CharFilter(field_name='player__name', lookup_expr='icontains')

    value = NumberFilter(field_name='value', lookup_expr='gte')

    class Meta:
        model = Ranking
        fields = '__all__'
        exclude = ['player','user','user_ranking', 'date_last_updated']
        
