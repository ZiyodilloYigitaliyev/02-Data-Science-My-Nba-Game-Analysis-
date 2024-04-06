import re

def action_catch(match, data):
    respons = []
    for action in data:
        n = re.compile(match).search(action)
        if n: 
            respons.append(action[n.span()[0] : n.span()[1]])
    return respons


def get_actions(data):
    mept3 = action_catch(r'([\S]. [\S]*) makes 3-pt jump shot from', data)   # 3P
    mispt3 = action_catch(r'([\S]. [\S]*) misses 3-pt jump shot from', data) # 3PA

    mept2 = action_catch(r'([\S]. [\S]*) makes 2-pt', data)   # 2P
    mispt2 = action_catch(r'([\S]. [\S]*) misses 2-pt', data) # 2PA

    ft = action_catch(r'([\S]. [\S]*) makes free throw', data)   # FT
    fta = action_catch(r'([\S]. [\S]*) misses free throw', data) # FTA

    orb = action_catch(r'Offensive rebound by ([\S]. [\S]*)', data)    # ORB
    drb =  action_catch(r'Defensive rebound by ([\S]. [\S]*)', data)   # DRB

    ast = action_catch(r'assist by ([\S]. [\S]*[^)])', data) # AST

    stl = action_catch(r'steal by ([\S]. [\S]*[^)])', data) # STL
    blk = action_catch(r'block by ([\S]. [\S]*[^)])', data) # BLK

    tov =  action_catch(r'Turnover by ([\S]. [\S]*)', data) # TOV
    pf = action_catch(r'Personal foul by ([\S]. [\S]*)', data) # PF

    return {'3P' : mept3, '3PA' : mispt3, '2P' : mept2, '2PA' : mispt2, 'FT' : ft, 'FTA' : fta, 'ORB' : orb, 'DRB' : drb, 'AST' : ast, 'STL' : stl, 'BLK' : blk, 'TOV' : tov, 'PF' :pf}



def get_names(data):
    players_name = []
    for action in data:
            n = re.compile(r'([\S]\. [\S]*[^)])').search(action)
            if n: 
                players_name.append(action[n.span()[0] : n.span()[1]].strip())
    return list(dict.fromkeys(players_name))


def split(csv_data):
    table = []
    for data in csv_data.split("\n"):
        series_list = []
        for series in data.split("|"):
            series_list.append(series)
        table.append(series_list)
    return table


def makes(series, match):
    respons = re.search(match, series[-1])
    if respons:
        return True
    return False



def wher_play(nba_data, names):
    players = {nba_data[0][4] : [], nba_data[0][3] : []}
    for name in names:
        for series in nba_data:
            if makes(series, f"{name} makes 3-pt"):
                players[series[2]].append(name)
                break
            elif makes(series, f"{name} makes 2-pt"):
                players[series[2]].append(name)
                break
            elif makes(series, f"{name} misses 3-pt"):
                players[series[2]].append(name)
                break
            elif makes(series, f"{name} misses 2-pt"):
                players[series[2]].append(name)
                break
            elif makes(series, f"Defensive rebound by {name}"):
                players[series[2]].append(name)
                break
            elif makes(series, f"Offensive rebound by {name}"):
                players[series[2]].append(name)
                break
    return players



def separate_team(names, nba_data):
    nba_data = split(nba_data)
    respons = {"home_team": {"name": nba_data[0][4], "players_data": None}, "away_team": {"name": nba_data[0][3], "players_data": None}}

    players = wher_play(nba_data, names)

    teams = {nba_data[0][4] : [], nba_data[0][3] : []}
    for team, players in players.items():
        n = 0
        for player in players:
            z = {"player_name": player, "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
            # print(z)
            teams[team].append(z)
            # n+=1
            # print(f'{n}. {player}')
    for key, value in teams.items():
        team = {"name": key, "players_data": value}
        if respons["home_team"]["name"] == key:
            respons["home_team"]["players_data"] = team["players_data"]
        if respons["away_team"]["name"] == key:
            respons["away_team"]["players_data"] = team["players_data"]
    return respons



def count(nba_game, action, n_key, a_key):
    for home_or_away, team in nba_game.items():
        # print(home_or_away)
        # print(team)
        stop = len(team['players_data'])
        for player in range(stop):
            # print(team['players_data'][player]['player_name'])
            # team['players_data'][player][nbkey]
            for series in action[a_key]:
                if re.search(team['players_data'][player]['player_name'], series):
                    team['players_data'][player][n_key] = team['players_data'][player][n_key] + 1
    
    return nba_game
    


def loader_action(nba_game, action):
    nba_game = count(nba_game, action, '3P', '3P')
    nba_game = count(nba_game, action, '3PA', '3PA')
    nba_game = count(nba_game, action, 'FG', '2P')
    nba_game = count(nba_game, action, 'FGA', '2PA')
    nba_game = count(nba_game, action, 'FT', 'FT')
    nba_game = count(nba_game, action, 'FTA', 'FTA')
    nba_game = count(nba_game, action, 'ORB', 'ORB')
    nba_game = count(nba_game, action, 'DRB', 'DRB')
    nba_game = count(nba_game, action, 'AST', 'AST')
    nba_game = count(nba_game, action, 'STL', 'STL')
    nba_game = count(nba_game, action, 'BLK', 'BLK')
    nba_game = count(nba_game, action, 'TOV', 'TOV')
    nba_game = count(nba_game, action, 'PF', 'PF')
    


    # print_nba_game_stats(nba_game)
    return nba_game


def do_it(nba_data, lable):
    lable = lable.split(".")
    equal, key1, do, key2 = lable[0], lable[1], lable[2], lable[3]
    for home_or_away, team_data in nba_data.items():
        for player_index in range(len(team_data['players_data'])):
            if key2.isnumeric():
                if do == "+":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] + int(key2)
                elif do == "-":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] - int(key2)
                elif do == "*":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] * int(key2)
                elif do == "/":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] / int(key2)
                # print(nba_data[home_or_away]['players_data'][player_index])
            else:
                if do == "+":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] + nba_data[home_or_away]['players_data'][player_index][key2]
                elif do == "-":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] - nba_data[home_or_away]['players_data'][player_index][key2]
                elif do == "*":
                    nba_data[home_or_away]['players_data'][player_index][equal] += nba_data[home_or_away]['players_data'][player_index][key1] * nba_data[home_or_away]['players_data'][player_index][key2]
                elif do == "/":
                    if nba_data[home_or_away]['players_data'][player_index][key1] != 0 and nba_data[home_or_away]['players_data'][player_index][key2] != 0:
                        nba_data[home_or_away]['players_data'][player_index][equal] = nba_data[home_or_away]['players_data'][player_index][key1] / nba_data[home_or_away]['players_data'][player_index][key2]
                # print(nba_data[home_or_away]['players_data'][player_index])
    return nba_data

         
def calculate(respons):
    respons = do_it(respons, "PTS.3P.*.3")
    respons = do_it(respons, "PTS.FG.*.2")
    respons = do_it(respons, "PTS.FT.+.0")

    respons = do_it(respons, "FGA.FG.+.0")
    respons = do_it(respons, "3PA.3P.+.0")
    respons = do_it(respons, "FGA.3PA.+.0")
    respons = do_it(respons, "FG.3P.+.0")

    respons = do_it(respons, "FG%.FG./.FGA")
    respons = do_it(respons, "FTA.FT.+.0")

    respons = do_it(respons, "FT%.FT./.FTA")
    respons = do_it(respons, "TRB.ORB.+.DRB")

    respons = do_it(respons, "3P%.3P./.3PA")
    return respons



def box(word, size):
    box = str(word)
    while len(box) != size:
        if len(box) < size:
            box = box + " "
        elif len(box) > size:
            box = box[0:-2]

    return box


def column(series):
    n=0
    for key in series.keys():
        n+=1
        if n == 1:
            print(box(key, 15), end = "|")
        else:
            print(box(key, 5), end = "|")
    print()


def series(series):
    n = 0
    for key, value in series.items():
        # print(type(value), end = " ")
        n+=1
        if n == 1:
            print(box(value, 15), end = "|")
        else:
            print(box(value, 5), end = "|")
    print()