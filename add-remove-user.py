import secrets
from flask import request, jsonify, current_app
from app.auth import bp
from app import auth, mail, get_admin
from flask_mail import Message
from keycloak.exceptions import KeycloakAuthenticationError
import requests
import json


def send_registration_mail(name, password, user_mail, redirect_uri):
    login_url = f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/realms/{current_app.config['KEYCLOAK_REALM']}/protocol/openid-connect/auth?client_id={current_app.config['KEYCLOAK_CLIENT_NAME']}&redirect_uri={redirect_uri}&response_type=code"

    #registration_message = Message(
    #    "Technoleon Account Registration",
    #    html=f"""
    #        <p>Hello {name},</p>

    #        <p>An account has been registered for {user_mail} via the Inside Joy app 
    #        with temporary password <b>{password}</b>.</p>

    #        <p>You can login <a href={login_url}>here</a>
    #        with this e-mail address and the password provided above.</p>

    #        <p>On login you will be prompted to change your password.</p>
    #    """,
    #    sender=current_app.config["MAIL_USERNAME"],
    #    recipients=[user_mail],
    #)
    #mail.send(registration_message)


def authenticate(admin, user_data, password):
    user_id = auth.admin.create_user(
        {
            "email": user_data["email"],
            "username": user_data["username"],
            "enabled": True,
        }
    )
    auth.admin.set_user_password(user_id=user_id, password=password, temporary=True)
    client_id = auth.admin.get_client_id(current_app.config["KEYCLOAK_CLIENT_NAME"])
    client_roles = auth.admin.get_client_roles(
        client_id=client_id
    )
    role = [client_role for client_role in client_roles if client_role['name'] == user_data['role']][0]
    auth.admin.assign_client_role(
        client_id=client_id,
        user_id=user_id,
        roles=[role],
    )
    return user_id


@bp.route("/create-user", methods=["POST"])
def create_user():
    user_data = request.form
    password = secrets.token_urlsafe(
        10
    )  # randomly generated password user is required to change on login

    print(f"username: {user_data['username']} password: {password}")
    try:
        user_id = authenticate(auth.admin, user_data, password)
    except KeycloakAuthenticationError:
        admin = get_admin(
            server_url=f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/",
            username=current_app.config["KEYCLOAK_USER"],
            password=current_app.config["KEYCLOAK_PASSWORD"],
            realm_name=current_app.config["KEYCLOAK_REALM"],
            client_name=current_app.config["KEYCLOAK_CLIENT_NAME"],
        )
        auth.init_auth(admin)
        user_id = authenticate(auth.admin, user_data, password)

        send_registration_mail(
            name=user_data["username"], password=password, user_mail=user_data["email"], redirect_uri=user_data['redirect_uri']
        )


    return jsonify(user_id=user_id)


def rem_user(admin, user_id):
    auth.admin.delete_user(user_id=user_id)




@bp.route("/user/<username>/delete", methods=["POST"])
def delete_user(username):
    # auth.admin.get_client_id(current_app.config["KEYCLOAK_CLIENT_NAME"])

    # Much better but not working. Getting the user ID based on the passed name in the URL parameter but keeps on returning "404 User Not Found"
    # user_id = auth.admin.get_user_id(username)

    # This will fetch all users and find the id of the wanted user
    user_id = ""
    print(user_id)
    
    try:
        all_users = auth.admin.get_users()
        for x in range(len(all_users)):
            if (username.lower() in all_users[x].values()):
                user_id = all_users[x]["id"]

        rem_user(auth.admin, user_id)
    except KeycloakAuthenticationError:
        admin = get_admin(
            server_url=f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/",
            username=current_app.config["KEYCLOAK_USER"],
            password=current_app.config["KEYCLOAK_PASSWORD"],
            realm_name=current_app.config["KEYCLOAK_REALM"],
            client_name=current_app.config["KEYCLOAK_CLIENT_NAME"],
        )
        auth.init_auth(admin)
        all_users = auth.admin.get_users()
        for x in range(len(all_users)):
            if (username.lower() in all_users[x].values()):
                user_id = all_users[x]["id"]

        rem_user(auth.admin, user_id)



    return jsonify(success=True)



def get_access_token():
    ENDPOINT_KC_TOKEN = f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/realms/master/protocol/openid-connect/token"
    payload = {"username": f"{current_app.config['KEYCLOAK_USER']}", "password": f"{current_app.config['KEYCLOAK_PASSWORD']}",
            "client_id": "admin-cli", "grant_type": "password"}
    req = requests.post(url=ENDPOINT_KC_TOKEN, data=payload).json()
    access_token = req["access_token"]
    return access_token



def update_user_kc(token, user_id, current_status):
    headers = {"Authorization": f"Bearer {token}"}
    headers["Content-Type"] = "application/json"
    ENDPOINT_UPDATE = f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/admin/realms/{current_app.config['KEYCLOAK_REALM']}/users/{user_id}"

    if current_status:
        payload = {"enabled": "False"}
    else:
        payload = {"enabled": "True"}

    req = requests.put(url=ENDPOINT_UPDATE, headers=headers,
                    data=json.dumps(payload))



@bp.route("/user/<username>/update", methods=["POST"])
def update_user(username):

    user_id = ""

    try:
        all_users = auth.admin.get_users()
        for x in range(len(all_users)):
            if (username.lower() in all_users[x].values()):
                user_id = all_users[x]["id"]

        access_token = get_access_token()
        ENDPOINT_USERS = f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/admin/realms/{current_app.config['KEYCLOAK_REALM']}/users/{user_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        req = requests.get(url=ENDPOINT_USERS, headers=headers).json()
        
        current_status = req["enabled"]
        
        update_user_kc(access_token, user_id, current_status)

    except KeycloakAuthenticationError:
        admin = get_admin(
            server_url=f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/",
            username=current_app.config["KEYCLOAK_USER"],
            password=current_app.config["KEYCLOAK_PASSWORD"],
            realm_name=current_app.config["KEYCLOAK_REALM"],
            client_name=current_app.config["KEYCLOAK_CLIENT_NAME"],
        )
        auth.init_auth(admin)
        all_users = auth.admin.get_users()
        for x in range(len(all_users)):
            if (username.lower() in all_users[x].values()):
                user_id = all_users[x]["id"]
        
        access_token = get_access_token()
        ENDPOINT_USERS = f"{current_app.config['KEYCLOAK_FRONTEND_URL']}/admin/realms/{current_app.config['KEYCLOAK_REALM']}/users/{user_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        req = requests.get(url=ENDPOINT_USERS, headers=headers).json()
        
        current_status = req["enabled"]
        
        update_user_kc(access_token, user_id, current_status)



    return jsonify(success=True)
