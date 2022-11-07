from django.test import TestCase
from analyzer_main.models import *

class modelsTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(username='test_run',
                                                email='testemail@test.com',
                                                password='Example1!')
        user_ranking = User_Ranking.objects.create(name='test_rankings',
                                                    user=test_user)
        player = Player.objects.create(name='test_player',
                                        id='1',
                                        position='QB')
        ranking = Ranking.objects.create(user_ranking=user_ranking,
                                        user=test_user,
                                        player=player,
                                        value=6500)

    def test_User(self):
        t_user = User.objects.create(username='user_test',
                                        email='usertest@test.com',
                                        password='newExample1!')
        self.assertEqual(t_user.username, 'user_test')
        self.assertEqual(t_user.email, 'usertest@test.com')

    def test_Tag(self):
        tag = Tag.objects.create(name='testtag')
        self.assertEqual(tag.name, 'testtag')

    def test_player(self):
        player = Player.objects.create(name='player_test',id='123',position='QB')
        self.assertEqual(player.name, 'player_test')
        self.assertEqual(player.id, '123')
        self.assertEqual(player.position, 'QB')

    def test_user_ranking(self):
        test_user = User.objects.get(username='test_run')
        user_ranking = User_Ranking.objects.create(name='user_ranking_test_ranking',
                                                    user=test_user)
        self.assertEqual(user_ranking.name, 'user_ranking_test_ranking')

    def test_ranking(self):
        test_user = User.objects.get(username='test_run')
        test_user_ranking = User_Ranking.objects.get(name='test_rankings')
        test_player = Player.objects.get(id='1')

        ranking = Ranking.objects.create(user_ranking=test_user_ranking,
                                        user=test_user,
                                        player=test_player,
                                        value=4031)
        self.assertEqual(ranking.value, 4031)

    def test_league(self):
        test_user = User.objects.get(username='test_run')
        test_user_ranking = User_Ranking.objects.get(name='test_rankings')

        league = League.objects.create(name='test_league',
                                            league_id='afjn13123',
                                            user=test_user,
                                            user_ranking=test_user_ranking,
                                            draft_order='Standings')
        self.assertEqual(league.name, 'test_league')
        self.assertEqual(league.league_id, 'afjn13123')
        self.assertEqual(league.draft_order, 'Standings')
        self.assertEqual(league.user_ranking.name, 'test_rankings')
        self.assertEqual(league.user.username, 'test_run')



    def test_league_output(self):
        test_user = User.objects.get(username='test_run')
        t_league_output = league_output.objects.create(player_id='2',
                                    name='random_player',
                                    value=4500,
                                    position='WR',
                                    display_name='my_name',
                                    league_id='1234556677',
                                    user=test_user,
                                    primary_id='test_league')
        self.assertEqual(t_league_output.player_id, '2')
        self.assertEqual(t_league_output.name, 'random_player')
        self.assertEqual(t_league_output.value, 4500)
        self.assertEqual(t_league_output.position, 'WR')
        self.assertEqual(t_league_output.display_name, 'my_name')
        self.assertEqual(t_league_output.league_id, '1234556677')
        self.assertEqual(t_league_output.user.username, 'test_run')
        self.assertEqual(t_league_output.primary_id, 'test_league')

    def test_table_league_total(self):
        test_user = User.objects.get(username='test_run')
        t_table_league_total = table_league_total.objects.create(display_name='my_name',
                                                                value=10000,
                                                                league_id='adaidf23231',
                                                                user=test_user,
                                                                primary_id='testoutput')
        self.assertEqual(t_table_league_total.display_name, 'my_name')
        self.assertEqual(t_table_league_total.value, 10000)
        self.assertEqual(t_table_league_total.league_id, 'adaidf23231')
        self.assertEqual(t_table_league_total.user.username, 'test_run')
        self.assertEqual(t_table_league_total.primary_id, 'testoutput')

    def test_Ranking_History(self):
        test_ranking = Ranking.objects.get(value=6500)
        ranking_history = Ranking_History.objects.create(ranking=test_ranking)
