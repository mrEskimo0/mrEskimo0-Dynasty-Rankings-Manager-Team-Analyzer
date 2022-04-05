from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from . import forms
from .models import *
from .functions import get_user_team, copy_default_rankings, get_team_ids, get_league
from .forms import Insert_ID, User_Ranking_Form, User_Insert_ID, Create_User_Form
from .filters import RankingFilter
from .serializers import *
from .chart_functions import league_df_todb, leaguetotals_df_todb
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import pandas as pd
from functools import reduce
from django.db.models import Q


def home(request):
    form = Insert_ID()

    if request.method == 'POST':
        form = forms.Insert_ID(request.POST)

        if form.is_valid():
            #call function to get team
            league_id = form.cleaned_data['id']
            display_name = form.cleaned_data['display_name']

            rankings = User_Ranking.objects.get(name="default_test")

            user_team, n_sums = get_user_team(league_id, display_name, rankings)

            context = {'user_team':user_team, 'n_sums':n_sums}

            return render(request, 'analyzer_main/team_view_sample.html', context)


    return render(request, 'analyzer_main/home.html', {'form':form})

@login_required(login_url='login')
def dashboard(request):
    request.session['rankings'] = None
    leagues = League.objects.filter(user__username=request.user.username)
    rankings = User_Ranking.objects.filter(Q(user__username=request.user.username) | Q(name='Consensus Superflex') | Q(name='Consensus Standard'))

    context = {'rankings':rankings, 'leagues':leagues}
    return render(request, 'analyzer_main/dashboard.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = Create_User_Form()

        if request.method == 'POST':
            form = Create_User_Form(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for'+user)

                return redirect('login')

    context = {'form':form}
    return render(request, 'analyzer_main/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'analyzer_main/login.html', context)

def logout_User(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def ranking_view(request, r_name):
    users_rank = User_Ranking.objects.get(name=r_name)
    rankings_set = Ranking.objects.filter(user_ranking__name=r_name).order_by('-value')
    tags = users_rank.tags.all()

    myfilter = RankingFilter(request.GET, queryset=rankings_set)
    rankings = myfilter.qs

    p = Paginator(rankings, 100)
    page = request.GET.get('page')
    rankings_list = p.get_page(page)

    #refresh players button
    if 'refresh_players' in request.POST and request.method == 'POST':
        #current ranks are rankings_set
        # current_set = Ranking.objects.filter(user_ranking__name=r_name).exclude(player__position='Pick')
        current_set = Ranking.objects.filter(user_ranking__name=r_name)
        current_ranks_list = set(current_set.values_list('player', 'player__position'))

        #pull most recent ktc
        # ktc_set = Ranking.objects.filter(user_ranking__name='Consensus Superflex').exclude(player__position='Pick')
        ktc_set = Ranking.objects.filter(user_ranking__name='Consensus Superflex')

        ktc_ranks_list = set(ktc_set.values_list('player', 'player__position'))

        take_aways = list(current_ranks_list - ktc_ranks_list)
        #delete take_aways from user's ranking set
        for player in take_aways:
            #Player.objects.get(id=player) <-- might have to get the player object to pass into delete method, same with create
            consensus_player = Ranking.objects.get(user_ranking__name='Consensus Superflex', player=player[0])
            Ranking.objects.filter(user_ranking=users_rank, player=consensus_player.player).delete()

        add_ins = list(ktc_ranks_list - current_ranks_list)
        #create these objects in user's ranking set
        for player in add_ins:
            consensus_player = Ranking.objects.get(user_ranking__name='Consensus Superflex', player=player[0])

            Ranking.objects.create(user_ranking=users_rank, player=consensus_player.player, user=request.user, value=consensus_player.value)
            # my_obj = Player.objects.get(id=player[0])
            # print(my_obj)
            # print(player)



        #call func to compare and add/delete

    if request.is_ajax and request.method == "POST" and 'refresh_players' not in request.POST:
        val = json.loads(request.POST.get('senddata'))

        for name, value in val.items():
            if type(float(value)) != float:
                print('no digit for ' + value)
                continue

            ranking_obj = Ranking.objects.get(user_ranking=users_rank, player__name=name)
            if ranking_obj.date_last_updated == datetime.date.today:
                ranking_obj.value = value
                ranking_obj.save()
            else:
                # player = ranking_obj.player
                today = datetime.date.today()
                ranking_obj.value = value
                ranking_obj.date_last_updated = today
                ranking_obj.save()

                #create instance in ranking history
                Ranking_History.objects.get_or_create(ranking=ranking_obj, date=today)
                # Ranking.objects.create(user_ranking=users_rank, user=request.user, player=player, value=value, date_last_updated=datetime.date.today())

    if r_name == 'Consensus Superflex' or r_name == 'Consensus Standard':
        if not request.user.is_superuser:
            context = {'rankings':rankings_list, 'users_rank':users_rank, 'myfilter':myfilter, 'tags':tags}

            return render(request, 'analyzer_main/ranking_view_noedit.html', context)
        else:
            context = {'rankings':rankings_list, 'users_rank':users_rank, 'myfilter':myfilter, 'tags':tags}
            return render(request, 'analyzer_main/ranking_view.html', context)
    else:
        context = {'rankings':rankings_list, 'users_rank':users_rank, 'myfilter':myfilter, 'tags':tags}
        return render(request, 'analyzer_main/ranking_view.html', context)



def team_view_sample(request, u_team):
    ranking_set = User_Ranking.objects.get(name="default_test")
    #assumes league id + team name are saved in database for user
    team_creds = Team.objects.filter(team=u_team)[0]
    user_team, n_sums = get_user_team(team_creds.league_id, team_creds.team_name, ranking_set)

    context ={'team_creds':team_creds, 'user_team':user_team, 'n_sums':n_sums}
    return render(request, 'analyzer_main/team_view.html', context)

@api_view(['GET'])
@login_required(login_url='login')
def league_view(request, league_id):
    if request.method == 'GET':

        c_user = User.objects.get(username=request.user.username)

        #delete any existing rows from table before hitting the sleeper api
        league_output.objects.filter(league_id=league_id, user=c_user).delete()
        table_league_total.objects.filter(league_id=league_id, user=c_user).delete()

        this_league = League.objects.get(league_id=league_id)
        #run func to get df of teams
        league_df = get_league(league_id, this_league)
        ranks_df = pd.DataFrame.from_records(Ranking.objects.filter(user_ranking=this_league.user_ranking).values())[['player_id', 'value', 'date_last_updated']]
        list_of_ids = league_df['players'].tolist()
        #get players in ranks by active ids
        players_df = pd.DataFrame.from_records(Player.objects.filter(id__in=list_of_ids).values())
        #make common name for player id
        league_df.rename(columns={'players':'player_id'}, inplace=True)
        players_df.rename(columns={'id':'player_id'}, inplace=True)
        #join dfs on player id
        # dfs = [league_df, players_df,  ranks_df]
        # df_final = reduce(lambda left,right: pd.merge(left, right, on='player_id'), dfs)
        df_temp = pd.merge(league_df, players_df)
        df_final = pd.merge(df_temp, ranks_df, how='left', on=['player_id'])
        df_final['value'] = df_final['value'].fillna(0)
        df_final['league_id'] = league_id
        df_final['user_id'] = c_user.id
        df_final.index.names = ['id']
        df_final = df_final.drop('owner_id', 1)
        df_final = df_final.drop('roster_id', 1)
        df_final['primary_id'] = df_final['league_id'] + df_final['display_name'] + df_final['name']
        # df_final.round({'value':1})
        league_df_todb(df_final)

        #GOOD JSON OUTPUT
        # output = df_final.to_dict('records')
        #league chart
        hello = df_final.groupby(['display_name'])['value'].sum()
        hello = hello.reset_index()
        hello['league_id'] = league_id
        hello['user_id'] = c_user.id
        hello.index.names = ['id']
        hello['primary_id'] = hello['league_id'] + hello['display_name'] + hello['user_id'].astype(str)
        leaguetotals_df_todb(hello)
        names = hello['display_name'].tolist()

        context = {'names':names,'league_id':league_id}

        return render(request, 'analyzer_main/league_view.html', context)

# @api_view(['GET'])
@login_required(login_url='login')
def team_view(request, league_id, display_name):

    if request.method == 'GET':

        context = {'league_id':league_id, 'display_name':display_name}

        return render(request, 'analyzer_main/team_view.html', context)

@login_required(login_url='login')
def make_ranking(request):
    form = User_Ranking_Form()
    if request.method == 'POST':
        #get user

        c_user = User.objects.get(username=request.user.username)

        form = User_Ranking_Form(request.POST)
        print(form.errors)
        if form.is_valid():
            new_rank = form.save(commit=False)
            template = form.cleaned_data['choose_ranks']
            new_rank.user = c_user
            new_rank.save()
            copy_default_rankings(new_rank, template)
            #function to get set rankings to default
            return redirect('/dashboard')

    context = {'form':form}
    return render(request, 'analyzer_main/ranking_form.html', context)

@login_required(login_url='login')
def make_team(request):
    c_user = User.objects.get(username=request.user.username)
    form = User_Insert_ID()
    form.fields["user_ranking"].queryset = User_Ranking.objects.filter(Q(user=request.user) | Q(name='Consensus Superflex') | Q(name='Consensus Standard'))


    if request.method == 'POST':

        form = User_Insert_ID(request.POST)
        if form.is_valid():
            new_team = form.save(commit=False)

            new_team.user = c_user
            #get player ids
            # this_teams_ids = get_team_ids(new_team.team_name, new_team.league_id)

            new_team.save()

            return redirect('/dashboard')

    context = {'form':form}
    return render(request, 'analyzer_main/team_form.html', context)

@login_required(login_url='login')
def update_team(request, league_id):
    user_team = League.objects.get(league_id=league_id)
    form = User_Insert_ID(instance=user_team)
    form.fields["user_ranking"].queryset = User_Ranking.objects.filter(Q(user=request.user) | Q(name='Consensus Superflex') | Q(name='Consensus Standard'))

    if request.method == 'POST':
        form = User_Insert_ID(request.POST, instance=user_team)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')

    context = {'form':form}
    return render(request, 'analyzer_main/team_form.html', context)

@login_required(login_url='login')
def update_ranking(request, r_name):
    user_ranking = User_Ranking.objects.get(name=r_name)
    form = User_Ranking_Form(instance=user_ranking)

    if request.method == 'POST':
        form = User_Ranking_Form(request.POST, instance=user_ranking)
        if form.is_valid():
            if not request.user.is_superuser and user_ranking.user.username == 'mrEskimo0':
                return redirect('/dashboard')
            else:
                form.save()
                return redirect('/dashboard')

    context = {'form':form}
    return render(request, 'analyzer_main/ranking_form.html', context)

@login_required(login_url='login')
def delete_team(request, league_id):
    user_team = League.objects.get(league_id=league_id)
    if request.method == 'POST':
        user_team.delete()
        return redirect('/dashboard')
    context = {'item':user_team}
    return render(request, 'analyzer_main/delete_team.html', context)

@login_required(login_url='login')
def delete_ranking(request, r_name):
    user_ranking = User_Ranking.objects.get(name=r_name)
    if request.method == 'POST':
        if not request.user.is_superuser and user_ranking.user.username == 'mrEskimo0':
            return redirect('/dashboard')
        else:
            user_ranking.delete()
            return redirect('/dashboard')
    context = {'item':user_ranking}
    return render(request, 'analyzer_main/delete_ranking.html', context)
