from django.urls import path
from django.contrib.auth import views as auth_views
from analyzer_main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.loginPage,name='login'),
    path('logout',views.logout_User,name='logout'),
    path('register',views.register,name='register'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('ranking_view/<str:r_name>',views.ranking_view,name='ranking_view'),
    path('league_view/<str:league_id>',views.league_view,name='league_view'),
    path('team_view/<str:league_id>/<str:display_name>',views.team_view,name='team_view'),
    #dashboard crud paths
    path('make_ranking',views.make_ranking,name='make_ranking'),
    path('make_team',views.make_team,name='make_team'),
    path('update_team/<str:league_id>',views.update_team, name="update_team"),
    path('update_ranking/<str:r_name>',views.update_ranking, name="update_ranking"),
    path('delete_team/<str:league_id>',views.delete_team, name="delete_team"),
    path('delete_ranking/<str:r_name>',views.delete_ranking, name="delete_ranking"),

    #reset password
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="analyzer_main/password_reset/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/',
     auth_views.PasswordResetDoneView.as_view(template_name="analyzer_main/password_reset/password_reset_sent.html"),
     name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="analyzer_main/password_reset/password_reset_form.html"),
      name="password_reset_confirm"),

    path('reset_password_complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name="analyzer_main/password_reset/password_reset_done.html"),
      name="password_reset_complete"),


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
