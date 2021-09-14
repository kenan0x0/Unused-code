@bp.route("switch-teams", methods=["POST", "GET"])
def switch_team():

    # Get all the players from the database
    available_players = (
        db.session.query(DmPlayer.username, DmPlayer.player_id)
        .all()
        )
    
    # Get all the teams from the database
    available_teams = (
    db.session.query(FfStagingTeam.name)
    .all()
    )
    
    # To remove the teams from the () and make them all one big list
    all_teams = []
    for i in range(len(available_teams)):
        all_teams.append(available_teams[i][0])

    # To know how many rows to make in the table
    nr_rows = len(available_players)

    nr_teams = len(all_teams)

    players = []
    teams = []

    # nr_rows_to_add = []
    # diff_list = []

    for i in range(nr_rows):
        query_teams = db.session.execute(f"SELECT name FROM ff_staging_team AS t INNER JOIN player_team AS pt ON t.id=pt.team_id INNER JOIN dm_user AS u ON u.player_id=pt.player_id WHERE pt.player_id='{available_players[i][1]}';")
        res = [row[0] for row in query_teams]

        # This will return a list with the teams in which a player isn't
        # first_diff = set(all_teams).difference(set(res))
        # second_diff = set(res).difference(set(all_teams))
        # list_difference = list(first_diff.union(second_diff))
        
        # nr_rows_to_add.append(len(list_difference))
        # diff_list.append(list_difference)

        # Fill the players list with the available players
        players.append(available_players[i][0])

        # If the query returns empty that means that a player isn't in any team currently
        if len(res) == 0:
            teams.append("No teams to show")
        else:   
            teams.append(", ".join(res))

    if request.method == "POST":
        player = request.form.get("user-name")
        if player is None:
            player = request.form.get("user-name2")
        action = request.form.get("action")
        team_name = request.form.get("team_name")

        player_id = ""
        for x in available_players:
            if player in x:
                player_id = x[1]


        team_id = FfStagingTeam.query.filter_by(name=team_name).first()
        team_id = team_id.team_id

        
        # # TODO automate the retreival of the access token
        headers2 = {"Content-Type": "application/json", "Authorization":f"Bearer 21927de80a19733eeb156dd5c99c175e"}
        data_join_group = [player_id]

        if action == "add":
            ENDPOINT_GENGEE_JOIN_GROUP = f"https://insait-api-eu.gengee.com/joy-club/groups/{team_id}/bulk"
            join_group_req = requests.post(ENDPOINT_GENGEE_JOIN_GROUP, data=json.dumps(data_join_group), headers=headers2).json()
        else:
            ENDPOINT_GENGEE_EXIT_GROUP = f"https://insait-api-eu.gengee.com/joy-club/groups/{team_id}/players"
            exit_group_req = requests.delete(ENDPOINT_GENGEE_EXIT_GROUP, data=json.dumps(data_join_group), headers=headers2).json()


    return render_template("admin_page/switch_team.html", players=players, teams=teams, nr_teams=nr_teams, all_teams=all_teams, nr_rows=nr_rows)
