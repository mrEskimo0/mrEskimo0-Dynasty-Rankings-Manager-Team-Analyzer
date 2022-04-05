from django.shortcuts import render
from django.db.models import Sum
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from analyzer_main.models import *
from .serializers import *
from get_default_rankings import run_the_scrape
from populate_players import get_data, populate_players, populate_picks
from django.db.models import Q
from decimal import *

@api_view(['GET'])
def league_overview(request):

    return Response()

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def league_totalval(request, league_id):
    this_leaguetotal = table_league_total.objects.filter(league_id=league_id)

    serializer = League_Table_Serializer(this_leaguetotal, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def playertotal(request, league_id):

    total_players = league_output.objects.filter(Q(position='QB') | Q(position='RB') | Q(position='WR') | Q(position='TE'), league_id=league_id).values('display_name').annotate(value=Sum('value'))

    serializer = Total_Value_Serializer(total_players, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def position_view_pick(request, league_id):

    picks = league_output.objects.filter(position='Pick', league_id=league_id).values('display_name').annotate(value=Sum('value'))

    serializer = Total_Value_Serializer(picks, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def position_view_qb(request, league_id):

    players = league_output.objects.filter(position='QB', league_id=league_id).values('display_name').annotate(value=Sum('value'))

    serializer = Total_Value_Serializer(players, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def position_view_wr(request, league_id):

    players = league_output.objects.filter(position='WR', league_id=league_id).values('display_name').annotate(value=Sum('value'))

    serializer = Total_Value_Serializer(players, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def position_view_rb(request, league_id):

    players = league_output.objects.filter(position='RB', league_id=league_id).values('display_name').annotate(value=Sum('value'))

    serializer = Total_Value_Serializer(players, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def position_view_te(request, league_id):

    players = league_output.objects.filter(position='TE', league_id=league_id).values('display_name').annotate(value=Sum('value'))

    serializer = Total_Value_Serializer(players, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def team_specific(request, league_id, display_name):

    my_team = league_output.objects.filter(league_id=league_id, display_name=display_name).order_by('-value')

    serializer = League_Output_Serializer(my_team, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def team_positionchart(request, league_id, display_name):

    my_team = league_output.objects.filter(league_id=league_id, display_name=display_name).values('position').annotate(value=Sum('value'))

    serializer = Position_Serializer(my_team, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def team_vs_median(request, league_id, display_name):

    def median_value(queryset):
        term = 'value'
        count = queryset.count()
        values = queryset.values_list(term, flat=True).order_by(term)
        if count % 2 == 1:
            return values[int(round(count/2))]
        else:
            return sum(values[count/2-1:count/2+1])/float(2.0)

    my_team = league_output.objects.filter(league_id=league_id, display_name=display_name).values('position').annotate(value=Sum('value')).order_by('position')

    serializer = Position_Serializer(my_team, many=True)

    #then get the league median for all the positions
    picks = league_output.objects.filter(position='Pick', league_id=league_id).values('display_name').annotate(value=Sum('value'))
    qbs = league_output.objects.filter(position='QB', league_id=league_id).values('display_name').annotate(value=Sum('value'))
    wrs = league_output.objects.filter(position='WR', league_id=league_id).values('display_name').annotate(value=Sum('value'))
    rbs = league_output.objects.filter(position='RB', league_id=league_id).values('display_name').annotate(value=Sum('value'))
    tes = league_output.objects.filter(position='TE', league_id=league_id).values('display_name').annotate(value=Sum('value'))
    #get medians
    picks_median = median_value(picks)
    qbs_median = median_value(qbs)
    wrs_median = median_value(wrs)
    rbs_median = median_value(rbs)
    tes_median = median_value(tes)

    league_vals = [
        {
            'position':'Pick',
            'value':picks_median
        },
        {
            'position':'QB',
            'value':qbs_median
        },
        {
            'position':'RB',
            'value':rbs_median
        },
        {
            'position':'TE',
            'value':tes_median
        },
        {
            'position':'WR',
            'value':wrs_median
        },
    ]

    total_response = {
        'league_median':league_vals,
        'team_vals':serializer.data
    }

    return Response(total_response)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def run_ktc_scrape(request):
    run_the_scrape()

    return Response({'message':'hey it works'})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def run_sleeper_pull(request):
    get_data()
    populate_players()
    populate_picks()

    return Response({'message':'hey it works'})
