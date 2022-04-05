
#pass league id into function
def get_user_team(league_id, display_name, ranking_name):
    import pandas as pd
    from analyzer_main.models import Player, Ranking
    from sleeper_wrapper import League, User, Players
    from django.db.models import Sum

    #get pd dataframe of user's team merged with player ids
    league = League(league_id)
    rosters = league.get_rosters()
    users = league.get_users()

    users = pd.DataFrame.from_dict(pd.json_normalize(users), orient='columns')
    roster_try = pd.DataFrame.from_records(rosters)

    roster_xplode = roster_try.explode('players')

    cols = ['players','owner_id', 'roster_id']
    rosters_cleaned = roster_xplode[cols]

    merged = pd.merge(rosters_cleaned, users, how='left', left_on=['owner_id'], right_on=['user_id'])

    merge_cols = ['players','display_name', 'roster_id']
    #col of players
    merged = merged[merge_cols]

    #merge draft picks to total assets dataframe
    def add_draft_picks(merged, league, rosters):
        traded_picks = league.get_traded_picks()
        league_data = league.get_league()

        #good: rosters, picks, traded_picks
        #need: num_teams, draft_rounds, in_season, season
        num_teams = league_data['settings']['num_teams']
        draft_rounds = league_data['settings']['draft_rounds']
        in_season = league_data['status']
        season = league_data['season']
        #input: league_type (for draft order, mpf or standings)
        #make standings for teams in league
        def make_standings(rosters, league_type=True):
            teams_list = []
            for team in rosters:
                teams_list.append([team['roster_id'], team['settings']['wins'], team['settings']['ppts'], team['settings']['fpts']])
            order_df = pd.DataFrame(data=teams_list, columns=['roster_id', 'wins', 'max_points_for', 'points_for'])
            if league_type:
                order_df = order_df.sort_values(['max_points_for'])
                order_df = order_df[['roster_id', 'max_points_for']]
            else:
                order_df = order_df.sort_values(['wins', 'points_for'])
                order_df = order_df[['roster_id', 'wins', 'points_for']]
            return order_df

        def build_from_scratch(num_teams, draft_rounds, in_season, season):
            #instanciate standard slate of picks for each team
            #were in 2021, we always go out 3 years, 2022, 2023, 2024
            max_season = int(season) + 3

            picks = []

            for year in range(int(season), max_season):
                for i in range(1, int(num_teams)+1):
                    for j in range(1, int(draft_rounds)+1):
                        picks.append([year, i, j, i])
            return picks

        def trade_picks(traded_picks, picks):
            df = pd.DataFrame(picks, columns = ['Year', 'Team', 'Round', 'roster_id'])
            for trade in traded_picks:
                season = int(trade['season'])
                d_round = trade['round']
                roster_id = trade['roster_id']
                owner_id = trade['owner_id']

                df.loc[(df['Year'] == season) & (df['Team'] == roster_id ) & (df['Round'] == d_round), "roster_id"] = owner_id
            return df

        def assign_pick_id(picks_df, order_df):
            team_order_list = order_df[['roster_id']].values.tolist()

            picks_df['Round_Position'] = ''

            for x, i in enumerate(team_order_list):
                team = i[0]
                picks_df.loc[(picks_df['Team'] == team), 'Round_Position'] = x+1

            def make_id(year, d_round, position, team_order_list):
                teams_num = len(team_order_list)
                pick = teams_num*d_round + position - teams_num
                return str(year) + '-' + str(pick)
            #year-round-pick
            picks_df['players'] = picks_df[['Year', 'Round', 'Round_Position']].apply(lambda picks_df: make_id(picks_df['Year'], picks_df['Round'], picks_df['Round_Position'], team_order_list), axis=1)

            return picks_df

        picks_df = build_from_scratch(num_teams, draft_rounds, in_season, season)
        picks_df = trade_picks(traded_picks, picks_df)
        order_df = make_standings(rosters)
        final_df = assign_pick_id(picks_df, order_df)

        picks_df_cleaned = picks_df[['players', 'roster_id']]
        picks_df_cleaned['display_name'] = ''

        team_order_list = order_df[['roster_id']].values.tolist()
        for i in team_order_list:
            team = i[0]
            picks_df_cleaned.loc[(picks_df_cleaned['roster_id'] == team), 'display_name'] = merged[merged['roster_id'] == team]['display_name'].values[0]

        return picks_df_cleaned

    #------------------ END FUNC --------------------------
    picks_df = add_draft_picks(merged, league, rosters)
    #ADD PICKS TO PLAYERS DF
    merged = merged.append(picks_df)

    #GET SUM OF TOTAL VALUE FOR EACH TEAM IN LEAGUE
    def team_sum_func(merged):
        sums = {}
        all_teams = list(set(merged['display_name'].tolist()))
        for team in all_teams:
            filtered_team = merged[merged['display_name'] == team]['players']
            this_team = filtered_team.values.tolist()
            this_team_query = Ranking.objects.filter(player__id__in=this_team, user_ranking__name=ranking_name)
            team_sum = this_team_query.aggregate(Sum('value'))
            sums[team] = team_sum['value__sum']
        #order dict from greatest to least
        n_sums = dict(sorted(sums.items(), key=lambda item: item[1], reverse=True))
        return n_sums

    n_sums = team_sum_func(merged)
    #GET ALL PLAYERS FOR USER'S TEAM
    filtered_user_team = merged[merged['display_name'] == display_name]['players']
    team = filtered_user_team.values.tolist()

    team_query = Ranking.objects.filter(player__id__in=team, user_ranking__name=ranking_name).order_by('player__position', '-value')

    print(ranking_name)

    return team_query, n_sums

def save_team_info(team_query, n_sums):
    from django.conf import settings

    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']

    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
    )

    engine = create_engine(database_url, echo=False)
    team_query.to_sql(My_Team, con=engine)
    n_sums.to_sql(My_League, con=engine)

def copy_default_rankings(user_ranking, template):
    from .models import User_Ranking, Ranking
    #take recently created user_ranking, and copy default ranking rankings to it
    default_rankings = Ranking.objects.filter(user_ranking__name=template)
    new_ranking = User_Ranking.objects.get(name=user_ranking)
    for ranking in default_rankings:
        n_user_ranking = user_ranking
        n_user = user_ranking.user
        n_player = ranking.player
        n_value = ranking.value
        Ranking.objects.create(user_ranking=n_user_ranking, user=n_user, player=n_player, value=n_value)

def get_team_ids(display_name, league_id):
    import pandas as pd
    from analyzer_main.models import Player
    from sleeper_wrapper import League, User, Players

    # team_ids = {} #might be []

    league = League(league_id)
    rosters = league.get_rosters()
    users = league.get_users()

    users = pd.DataFrame.from_dict(pd.json_normalize(users), orient='columns')
    roster_try = pd.DataFrame.from_records(rosters)

    roster_xplode = roster_try.explode('players')

    cols = ['players','owner_id', 'roster_id']
    rosters_cleaned = roster_xplode[cols]

    merged = pd.merge(rosters_cleaned, users, how='left', left_on=['owner_id'], right_on=['user_id'])

    merge_cols = ['players','display_name', 'roster_id']
    #col of players
    merged = merged[merge_cols]

    #add picks to this
    def add_draft_picks(merged, league, rosters):
        traded_picks = league.get_traded_picks()
        league_data = league.get_league()

        #good: rosters, picks, traded_picks
        #need: num_teams, draft_rounds, in_season, season
        num_teams = league_data['settings']['num_teams']
        draft_rounds = league_data['settings']['draft_rounds']
        in_season = league_data['status']
        season = league_data['season']
        #input: league_type (for draft order, mpf or standings)
        #make standings for teams in league
        def make_standings(rosters, league_type=True):
            teams_list = []
            for team in rosters:
                teams_list.append([team['roster_id'], team['settings']['wins'], team['settings']['ppts'], team['settings']['fpts']])
            order_df = pd.DataFrame(data=teams_list, columns=['roster_id', 'wins', 'max_points_for', 'points_for'])
            if league_type:
                order_df = order_df.sort_values(['max_points_for'])
                order_df = order_df[['roster_id', 'max_points_for']]
            else:
                order_df = order_df.sort_values(['wins', 'points_for'])
                order_df = order_df[['roster_id', 'wins', 'points_for']]
            return order_df

        def build_from_scratch(num_teams, draft_rounds, in_season, season):
            #instanciate standard slate of picks for each team
            #were in 2021, we always go out 3 years, 2022, 2023, 2024
            max_season = int(season) + 3

            picks = []

            for year in range(int(season), max_season):
                for i in range(1, int(num_teams)+1):
                    for j in range(1, int(draft_rounds)+1):
                        picks.append([year, i, j, i])
            return picks

        def trade_picks(traded_picks, picks):
            df = pd.DataFrame(picks, columns = ['Year', 'Team', 'Round', 'roster_id'])
            for trade in traded_picks:
                season = int(trade['season'])
                d_round = trade['round']
                roster_id = trade['roster_id']
                owner_id = trade['owner_id']

                df.loc[(df['Year'] == season) & (df['Team'] == roster_id ) & (df['Round'] == d_round), "roster_id"] = owner_id
            return df

        def assign_pick_id(picks_df, order_df):
            team_order_list = order_df[['roster_id']].values.tolist()

            picks_df['Round_Position'] = ''

            for x, i in enumerate(team_order_list):
                team = i[0]
                picks_df.loc[(picks_df['Team'] == team), 'Round_Position'] = x+1

            def make_id(year, d_round, position, team_order_list):
                teams_num = len(team_order_list)
                pick = teams_num*d_round + position - teams_num
                return str(year) + '-' + str(pick)
            #year-round-pick
            picks_df['players'] = picks_df[['Year', 'Round', 'Round_Position']].apply(lambda picks_df: make_id(picks_df['Year'], picks_df['Round'], picks_df['Round_Position'], team_order_list), axis=1)

            return picks_df

        picks_df = build_from_scratch(num_teams, draft_rounds, in_season, season)
        picks_df = trade_picks(traded_picks, picks_df)
        order_df = make_standings(rosters)
        final_df = assign_pick_id(picks_df, order_df)

        picks_df_cleaned = picks_df[['players', 'roster_id']]
        picks_df_cleaned['display_name'] = ''

        team_order_list = order_df[['roster_id']].values.tolist()
        for i in team_order_list:
            team = i[0]
            picks_df_cleaned.loc[(picks_df_cleaned['roster_id'] == team), 'display_name'] = merged[merged['roster_id'] == team]['display_name'].values[0]

        return picks_df_cleaned

    #------------------ END FUNC --------------------------
    picks_df = add_draft_picks(merged, league, rosters)
    #ADD PICKS TO PLAYERS DF
    merged = merged.append(picks_df)

    #get this users assets ids
    player_ids = merged[merged['display_name'] == display_name]['players'].values.tolist()

    # team_query = Player.objects.filter(id__in=player_ids).order_by('position')
    id_string = ''
    for id in player_ids:
        id_string += id + ' '

    return id_string

def get_league(league_id, this_league):
    import pandas as pd
    from analyzer_main.models import Player, Ranking
    from sleeper_wrapper import League, User, Players
    from functools import reduce

    # team_ids = {} #might be []

    league = League(league_id)
    rosters = league.get_rosters()
    users = league.get_users()

    users = pd.DataFrame.from_dict(pd.json_normalize(users), orient='columns')
    roster_try = pd.DataFrame.from_records(rosters)

    roster_xplode = roster_try.explode('players')

    cols = ['players','owner_id', 'roster_id']
    rosters_cleaned = roster_xplode[cols]

    merged = pd.merge(rosters_cleaned, users, how='left', left_on=['owner_id'], right_on=['user_id'])

    merge_cols = ['players','display_name','roster_id','owner_id']
    #col of players
    merged = merged[merge_cols]

    #add picks to this
    def add_draft_picks(merged, league, rosters):
        traded_picks = league.get_traded_picks()
        league_data = league.get_league()

        #good: rosters, picks, traded_picks
        #need: num_teams, draft_rounds, in_season, season
        num_teams = league_data['settings']['num_teams']
        draft_rounds = league_data['settings']['draft_rounds']
        season = league_data['season']
        #input: league_type (for draft order, mpf or standings)
        #make standings for teams in league
        def make_standings(rosters, league_type=True):
            teams_list = []
            for team in rosters:
                try:
                    teams_list.append([team['roster_id'], team['settings']['wins'], team['settings']['ppts'], team['settings']['fpts']])
                except KeyError:
                    teams_list.append([team['roster_id'], team['settings']['wins'], 0, team['settings']['fpts']])
            order_df = pd.DataFrame(data=teams_list, columns=['roster_id', 'wins', 'max_points_for', 'points_for'])
            if league_type:
                order_df = order_df.sort_values(['max_points_for'])
                order_df = order_df[['roster_id', 'max_points_for']]
            else:
                order_df = order_df.sort_values(['wins', 'points_for'])
                order_df = order_df[['roster_id', 'wins', 'points_for']]
            return order_df

        def build_from_scratch(num_teams, draft_rounds, season):
            #instanciate standard slate of picks for each team
            #were in 2021, we always go out 3 years, 2022, 2023, 2024
            max_season = int(season) + 3

            picks = []

            for year in range(int(season), max_season):
                for i in range(1, int(num_teams)+1):
                    for j in range(1, int(draft_rounds)+1):
                        picks.append([year, i, j, i])
            return picks

        def trade_picks(traded_picks, picks):
            df = pd.DataFrame(picks, columns = ['Year', 'Team', 'Round', 'roster_id'])
            for trade in traded_picks:
                season = int(trade['season'])
                d_round = trade['round']
                roster_id = trade['roster_id']
                owner_id = trade['owner_id']

                df.loc[(df['Year'] == season) & (df['Team'] == roster_id ) & (df['Round'] == d_round), "roster_id"] = owner_id
            return df

        def assign_pick_id(picks_df, order_df):
            team_order_list = order_df[['roster_id']].values.tolist()
            print(team_order_list)

            picks_df['Round_Position'] = ''

            for x, i in enumerate(team_order_list):
                team = i[0]
                picks_df.loc[(picks_df['Team'] == team), 'Round_Position'] = x+1

            def make_id(year, d_round, position, team_order_list):
                teams_num = len(team_order_list)
                pick = teams_num*d_round + position - teams_num
                return str(year) + '-' + str(pick)
            #year-round-pick
            picks_df['players'] = picks_df[['Year', 'Round', 'Round_Position']].apply(lambda picks_df: make_id(picks_df['Year'], picks_df['Round'], picks_df['Round_Position'], team_order_list), axis=1)

            return picks_df

        picks_df = build_from_scratch(num_teams, draft_rounds, season)
        picks_df = trade_picks(traded_picks, picks_df)

        #check if points scored == 0 for all the columns
        order_df = make_standings(rosters)
        drafts = league.get_all_drafts()
        if order_df['max_points_for'].sum() != 0:

            final_df = assign_pick_id(picks_df, order_df)

        #check for pre-draft draft in league
        elif drafts[0]['status'] == 'pre_draft' and drafts[0]['draft_order'] is not None:
            draft_order = drafts[0]['draft_order']

            ids = pd.Series(merged.roster_id.values, merged.owner_id).to_dict()

            existing_draft_order = {}
            for owner_id, roster_id in ids.items():
                spot = draft_order[owner_id]
                existing_draft_order[roster_id] = spot

            order_df = pd.DataFrame(existing_draft_order.items(), columns=['roster_id', 'draft_spot'])
            order_df = order_df.sort_values(by=['draft_spot'])

            final_df = assign_pick_id(picks_df, order_df)

        else:
            ranks_df = pd.DataFrame.from_records(Ranking.objects.filter(user_ranking=this_league.user_ranking).values())[['player_id', 'value', 'date_last_updated']]
            merged_copy = merged.copy()
            merged_copy.rename(columns={'players':'player_id'}, inplace=True)
            dfs = [merged_copy, ranks_df]
            mapped_vals = reduce(lambda left,right: pd.merge(left, right, on='player_id'), dfs)
            #groupby then sum players
            mapped_vals = mapped_vals.groupby(['roster_id'])['value'].sum()
            #order by value
            mapped_vals.sort_values(inplace=True)

            final_df = assign_pick_id(picks_df, order_df)


        picks_df_cleaned = picks_df[['players', 'roster_id']]
        picks_df_cleaned['display_name'] = ''

        team_order_list = order_df[['roster_id']].values.tolist()
        for i in team_order_list:
            team = i[0]
            picks_df_cleaned.loc[(picks_df_cleaned['roster_id'] == team), 'display_name'] = merged[merged['roster_id'] == team]['display_name'].values[0]

        return picks_df_cleaned

    #------------------ END FUNC --------------------------
    picks_df = add_draft_picks(merged, league, rosters)
    #ADD PICKS TO PLAYERS DF
    merged = merged.append(picks_df)
    # list_of_teams = list(set(merged['display_name'].tolist()))

    return merged
