from django.contrib import admin
from analyzer_main.models import Player, Tag, Ranking, User_Ranking, Team, League
# Register your models here.
admin.site.register(Player)
admin.site.register(Tag)
admin.site.register(Ranking)
admin.site.register(User_Ranking)
admin.site.register(Team)
admin.site.register(League)
