from django.urls import path
from . import views

urlpatterns = [
    path('', views.league_overview,name='home'),
    path('league_totalval/<str:league_id>', views.league_totalval,name='league_totalval'),
    path('playertotal/<str:league_id>', views.playertotal,name='playertotal'),
    path('position_view_pick/<str:league_id>', views.position_view_pick,name='position_view_pick'),
    path('position_view_qb/<str:league_id>', views.position_view_qb,name='position_view_qb'),
    path('position_view_wr/<str:league_id>', views.position_view_wr,name='position_view_wr'),
    path('position_view_rb/<str:league_id>', views.position_view_rb,name='position_view_rb'),
    path('position_view_te/<str:league_id>', views.position_view_te,name='position_view_te'),
    path('team_specific/<str:league_id>/<str:display_name>', views.team_specific,name='team_specific'),
    path('team_positionchart/<str:league_id>/<str:display_name>', views.team_positionchart,name='team_positionchart'),
    path('team_vs_median/<str:league_id>/<str:display_name>', views.team_vs_median,name='team_vs_median'),
    path('run_ktc_scrape', views.run_ktc_scrape,name='run_ktc_scrape'),
    path('run_sleeper_pull', views.run_sleeper_pull,name='run_sleeper_pull'),
]
