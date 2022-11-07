from django.test import TestCase
from analyzer_main.models import *
from django.contrib.auth.models import User
import time

class ViewsTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_superuser(username='test_run',
                                        email='testemail@test.com',
                                        password='Example1!')
        user_ranking = User_Ranking.objects.create(name='test_rankings',
                                                    user=test_user)
        player = Player.objects.create(name='test_player',
                                        id='1234',
                                        position='QB')
        ranking = Ranking.objects.create(user_ranking=user_ranking,
                                        user=test_user,
                                        player=player,
                                        value=6500)
        tags = Tag.objects.create(name='testtag')

        league = League.objects.create(name='test_league',
                                        league_id='784628582977802240',
                                        user=test_user,
                                        user_ranking=user_ranking,
                                        draft_order='Standings')


    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post('/register', {'username':'test_run',
                                        'email':'testemail@test.com',
                                        'password':'Example1!'})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', {'username':'test_run',
                                    'password':'Example1!'}, follow=True)
        #if we reach dashboard then login worked
        self.assertTemplateUsed(response, 'analyzer_main/dashboard.html')


    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_dashboard(self):
        user = User.objects.get(username='test_run')
        self.client.login(username='test_run', password='Example1!')
        response = self.client.get('/dashboard', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyzer_main/dashboard.html')

    def test_make_ranking(self):
        self.client.login(username='test_run', password='Example1!')
        page = self.client.get('/make_ranking')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'analyzer_main/ranking_form.html')
        tag = Tag.objects.get(name='testtag')
        response = self.client.post('/make_ranking', {'name':'test_ranks',
                                                'tags':tag.id,
                                                'choose_ranks':'Consensus Superflex'},
                                                follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyzer_main/dashboard.html')

    def test_ranking_view(self):
        self.client.login(username='test_run', password='Example1!')
        rankings = User_Ranking.objects.get(name='test_rankings')
        page = self.client.get('/ranking_view/test_rankings')
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'analyzer_main/ranking_view.html')

    def test_ranking_update(self):
        self.client.login(username='test_run', password='Example1!')
        rankings = User_Ranking.objects.get(name='test_rankings')
        response = self.client.get('/update_ranking/'+rankings.name, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_ranking(self):
        self.client.login(username='test_run', password='Example1!')
        rankings = User_Ranking.objects.get(name='test_rankings')
        response = self.client.get('/delete_ranking/'+rankings.name, follow=True)
        self.assertEqual(response.status_code, 200)
