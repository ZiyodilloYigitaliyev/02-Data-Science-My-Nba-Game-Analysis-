from utilits import get_actions, get_names, separate_team, loader_action, calculate, box, column, series


def print_nba_game_stats(team_dict):
    for home_or_away, team_data in team_dict.items():
        print(f">>> \n{home_or_away}\n")
        n = 0
        # print(team_data)
        totals = {"player_name": 'Total:',  'FG':0, 'FGA':0, 'FG%':0, '3P':0, '3PA':0, '3P%':0, 'FT':0, 'FTA':0, 'FT%':0, 'ORB':0, 'DRB':0, 'TRB':0, 'AST':0, 'STL':0, 'BLK':0, 'TOV':0, 'PF':0, 'PTS' : 0}
        print(team_data['name'])
        for player in team_data['players_data']:
            n+=1
            if n == 1:
                column(player)
            series(player)
            for key, value in player.items():
                if "player_name" != key:
                    totals[key] += value
        
        series(totals)


def analyse_nba_game(data):
    actions = get_actions(data.split('\n'))
    names = get_names(data.split('\n'))
    
    teams_data = separate_team(names, data)
    team_data = loader_action(teams_data, actions)
    team_data = calculate(team_data)
    
    return teams_data



if __name__ == '__main__':
    data =  open('nba_game_blazers_lakers_20181018.txt', 'r').read()
    
    team_data = analyse_nba_game(data)
    print_nba_game_stats(team_data)