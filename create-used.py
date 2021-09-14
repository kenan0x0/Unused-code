# Route where player role will be created
@bp.route("create-player", methods=["POST", "GET"])
def add_player():

    user_email = request.form.get("email")

    # bearer_token = get_credentials()['data']['access_token']

    # invite_code = 3000
    
    # headers = {"Authorization": f"Bearer {bearer_token}"}
    # ENDPOINT_GENGEE_GROUPS = "https://insait-api-eu.gengee.com/joy-club/567629ea-b661-11e8-a7c2-069acdac8ec2/groups?pageNumber=1&pageSize=100"

    # # Gengee API Endpoint which creates an account in the protal
    # ENDPOINT_GENGEE_REGISTER_ACCOUNT = "https://insait-api-eu.gengee.com/joy-football/account/register"

    # # Gengee API Endpoint which adds the mandatory profile information to the newly created account
    # ENDPOINT_GENGEE_PROFILE_INFO = "https://insait-api-eu.gengee.com/joy-football/account/profile"

    # # Gengee API Endpoint which is used to add the newly created user to a club using an invite code
    # ENDPOINT_GENGEE_JOIN_CLUB = f"https://insait-api-eu.gengee.com/joy-club/invitation/{invite_code}"


    # groups = []
    # group_ids = []
    # groups_and_ids = {}
    # get_groups_req = requests.get(ENDPOINT_GENGEE_GROUPS, headers=headers).json()
    # all_groups_gg = get_groups_req["data"]["content"]

    # for group in all_groups_gg:
    #     groups.append(group["name"])
    #     group_ids.append(group["id"])
    #     groups_and_ids[group["name"]] = group["id"]

    # loop_counter = len(groups)

    # if request.method == "POST":
    #     # The amil under which all players are registered
    #     used_email = os.environ.get("EMAIL_ADDR")

    #     # The email that will be used later to register players in DB and keycloak
    #     email = request.form.get("email")
    #     username = request.form.get("username")
    #     gender = request.form.get("gender")
    #     team = request.form.get("team")
    #     weight = int(request.form.get("weight"))
    #     height = int(request.form.get("height"))
    #     bday = request.form.get("bday")
    #     image_url = request.form.get("url")


    #     # Gengee API Endpoint which sends confirmation emails
    #     ENDPOINT_GENGEE_SEND_CODE = "https://insait-api-eu.gengee.com/joy-football/captcha"
    #     headers = {"Content-Type": "application/json"}
    #     data_send_email_req = {"email":used_email}

    #     send_code = requests.post(ENDPOINT_GENGEE_SEND_CODE, data=json.dumps(data_send_email_req), headers=headers).json()
    #     code_email_sent = send_code["message"]
    #     if code_email_sent == "SUCCESS":
    #         time.sleep(10)
    #         code = str(get_verification_code(os.environ.get("EMAIL_ADDR"), os.environ.get("EMAIL_PSWD")))
    #         if (len(code) == 5):
    #             code = "0" + code
    #         temp_pswd = ''.join(random.SystemRandom().choice(string.ascii_uppercase +string.digits + string.ascii_lowercase) for _ in range(16))
    #         data_register_account = {"email":used_email,
    #                 "phone":None,
    #                 "password":temp_pswd,
    #                 "nickname":username,
    #                 "captcha":code}
    #         create_account = requests.post(ENDPOINT_GENGEE_REGISTER_ACCOUNT, data=json.dumps(data_register_account), headers=headers).json()
    #         try:
    #             account_created = create_account["message"]
    #             user_id = create_account["data"]["principal"]["userId"]
    #             access_token = create_account["data"]["access_token"]
    #         except TypeError:
    #             time.sleep(10)
    #             code = str(get_verification_code(os.environ.get("EMAIL_ADDR"), os.environ.get("EMAIL_PSWD")))
    #             if (len(code) == 5):
    #                 code = "0" + code
    #             data_register_account = {"email": used_email,
    #                                     "phone": None,
    #                                     "password": temp_pswd,
    #                                     "nickname": username,
    #                                     "captcha": code}
    #             create_account = requests.post(ENDPOINT_GENGEE_REGISTER_ACCOUNT, data=json.dumps(data_register_account), headers=headers).json()
    #             account_created = create_account["message"]
    #             user_id = create_account["data"]["principal"]["userId"]
    #             access_token = create_account["data"]["access_token"]
    #         if account_created == "SUCCESS":
    #             headers2 = {"Content-Type": "application/json", "Authorization":f"Bearer {access_token}"}
    #             # TODO check the regionID ##########################################
    #             profile_data = {"userId":user_id,
    #                             "avatar":None,
    #                             "gender":gender,
    #                             "regionId":324234,
    #                             "phone":None,
    #                             "height":height,
    #                             "birthday":bday,
    #                             "email": used_email,
    #                             "weight": weight,
    #                             "name":username}
    #             add_profile_info = requests.put(ENDPOINT_GENGEE_PROFILE_INFO, data=json.dumps(profile_data), headers=headers2).json()
    #             profile_info_added = add_profile_info["message"]
    #             if profile_info_added == "SUCCESS":
    #                 join_club_data = {
    #                     "phone":"",
    #                     "playerId": user_id,
    #                     "imgUrl":image_url,
    #                     "name": username,
    #                     "gender": gender
    #                 }
    #                 join_club_req = requests.post(ENDPOINT_GENGEE_JOIN_CLUB, data=json.dumps(join_club_data), headers=headers2).json()
    #                 club_joined = join_club_req["message"]
    #                 if club_joined == "SUCCESS":
    #                     data_join_group = [user_id]
    #                     # Gengee API Endpoint which is used to add the newly created user to a group within the club
    #                     ENDPOINT_GENGEE_JOIN_GROUP = f"https://insait-api-eu.gengee.com/joy-club/groups/{team}/bulk"
    #                     join_group_req = requests.post(ENDPOINT_GENGEE_JOIN_GROUP, data=json.dumps(data_join_group), headers=headers2).json()
    #                     group_joined = join_group_req["message"]
    #                     if group_joined == "SUCCESS":
    #                         print("User has been added!")
    #                         print(temp_pswd)



        # crt_player = requests.post(f"{current_app.config['AUTH_APPLICATION']}/create-user",
        #             data={
        #                 "email": email,
        #                 "username": username,
        #                 "role": "player",
        #                 "redirect_uri": current_app.config["APP_URL"],
        #             },)
        
        
            return render_template("admin_page/create_player.html", groups=groups, ids=group_ids, len=loop_counter)
