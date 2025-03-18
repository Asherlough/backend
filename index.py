import requests
import random
from flask import Flask, jsonify, request

class GameInfo:
    def __init__(self):
        self.TitleId : str = "196C1E"
        self.SecretKey : str = "BXX77KOJJ6PMGD6SH5WUTIX81KAXYRUIK47S3TQ7NYAHD4PY7H"
        self.ApiKey : str = "9247135675321490"

    def get_auth_headers(self):
        return {
            "content-type": "application/json",
            "X-SecretKey": self.SecretKey
        }

settings = GameInfo()
app = Flask(__name__)
playfab_cache = {}
mute_cache = {}

settings.TitleId : str = "196C1E"
settings.SecretKey : str = "BXX77KOJJ6PMGD6SH5WUTIX81KAXYRUIK47S3TQ7NYAHD4PY7H"
settings.ApiKey : str = "9247135675321490"

@app.route("/", methods=["POST", "GET"])
def main():
    return "Backend Is Running! <3"

@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():
    # no more modders!
    if request.method != "POST":
        return "", 404

    if request.headers.get('User-Agent') != "UnityPlayer/2022.3.2f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)" or request.headers.get('X-Unity-Version') != "2022.3.2f1":
        return Response(json.dumps({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite"}, indent=4), mimetype="application/json")

    rjson = request.get_json()
    oculus_id = rjson.get("OculusId")
    nonce = rjson.get("Nonce")
    title = rjson.get("AppId")
    platform = rjson.get("Platform")
    env_token = rjson.get("MothershipEnvId")

    if title != settings.TitleId: 
        return Response(json.dumps({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite"}, indent=4), mimetype="application/json")

    if env_token != "7f3a99dd-5598-4725-98cf-6538d28feb9f": 
        return Response(json.dumps({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite"}, indent=4), mimetype="application/json")

    if platform != "Quest": 
        return Response(json.dumps({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite"}, indent=4), mimetype="application/json")

    oculus_response = requests.post("https://graph.oculus.com/user_nonce_validate", json={
        "access_token": f"{settings.ApiKey}",
        "nonce": nonce,
        "user_id": oculus_id
    }) 

    if oculus_response.status_code != 200 or not oculus_response.json().get("is_valid", False):
        return Response(json.dumps({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite"}, indent=4), mimetype="application/json")

    # end no more modders!


    url = f"https://{settings.TitleId}.playfabapi.com/Server/LoginWithServerCustomId"
    login_request = requests.post(
        url=url,
        json={
            "ServerCustomId": "OCULUS" + rjson.get("OculusId"),
            "CreateAccount": True
        },
        headers=settings.get_auth_headers()
    )

    if login_request.status_code == 200:
        data = login_request.json().get("data")
        session_ticket = data.get("SessionTicket")
        entity_token = data.get("EntityToken").get("EntityToken")
        playfab_id = data.get("PlayFabId")
        entity_type = data.get("EntityToken").get("Entity").get("Type")
        entity_id = data.get("EntityToken").get("Entity").get("Id")

        return jsonify({
            "PlayFabId": playfab_id,
            "SessionTicket": session_ticket,
            "EntityToken": entity_token,
            "EntityId": entity_id,
            "EntityType": entity_type
        }), 200
    else: 
        ban_info = login_req.json()
        if ban_info.get("errorCode") == 1002:
            ban_message = ban_info.get("errorMessage", "No ban message provided.")
            ban_details = ban_info.get("errorDetails", {})
            ban_expiration_key = next(iter(ban_details.keys()), None)
            ban_expiration_list = ban_details.get(ban_expiration_key, [])
            ban_expiration = (
                ban_expiration_list[0]
                if len(ban_expiration_list) > 0
                else "Indefinite"
            )
            return jsonify({
                "BanMessage": ban_expiration_key,
                "BanExpirationTime": ban_expiration,
            }), 403

@app.route("/api/CachePlayFabId", methods=["POST"])
def cache_playfab_id():
    return "", 200

@app.route("/api/td", methods=["POST", "GET"])
def title_data():
    response = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/GetTitleData",
        headers=settings.get_auth_headers()
    )

    if response.status_code == 200:
        return jsonify(response.json().get("data").get("Data"))
    else:
        return jsonify({}), response.status_code

@app.route('/api/td', methods=['POST', 'GET'])
def titled_data():
    return jsonify({"MOTD":"<color=yellow>WELCOME TO PROECT SKYZ!</color>\n\n<color=red>MOKE BLOCKS UPDATE! WE CAN DO NEWER UPDATES!</color>\n\n\n!</color>\n<color=orange>CREDITS: PRIGLES</color>"})

@app.route("/api/CheckForBadName", methods=["POST"])
def check_for_bad_name():
    rjson = request.get_json().get("FunctionResult")
    name = rjson.get("name").upper()

    if name in ["KKK", "PENIS", "NIGG", "NEG", "NIGA", "MONKEYSLAVE", "SLAVE", "FAG",
        "NAGGI", "TRANNY", "QUEER", "KYS", "DICK", "PUSSY", "VAGINA", "BIGBLACKCOCK",
        "DILDO", "HITLER", "KKX", "XKK", "NIGA", "NIGE", "NIG", "NI6", "PORN",
        "JEW", "JAXX", "TTTPIG", "SEX", "COCK", "CUM", "FUCK", "PENIS", "DICK",
        "ELLIOT", "JMAN", "K9", "NIGGA", "TTTPIG", "NICKER", "NICKA",
        "REEL", "NII", "@here", "!", " ", "JMAN", "PPPTIG", "CLEANINGBOT", "JANITOR", "K9",
        "H4PKY", "MOSA", "NIGGER", "NIGGA", "IHATENIGGERS", "@everyone", "FAGGYWAGGY", "NIGGYWIGGY", "XXX"]:
        return jsonify({"result": 2})
    else:
        return jsonify({"result": 0})

@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    rjson = request.get_json()

    access_token = rjson.get("userToken")
    user_id = rjson.get("userID")
    nonce = rjson.get("nonce")
    sku = rjson.get("sku")

    response = requests.post(
        url=f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={settings.ApiKey}",
        headers={"content-type": "application/json"}
    )

    if response.json().get("success"):
        return jsonify({"result": True})
    else:
        return jsonify({"error": True})

@app.route("/api/ShouldUserAutomutePlayer", methods=["POST", "GET"])
def should_user_automute_player():
    data = request.json
    function_argument = data.get('FunctionArgument')
    
    ids = function_argument.split(',')
    response = {id_: "NONE" for id_ in ids}
    
    return jsonify(response)

@app.route("/api/photon", methods=["POST", "GET"])
def photon():
    rjson = request.get_json()
    print(rjson)
    if not rjson or "Ticket" not in rjson:
        return jsonify({"ResultCode": 0, "UserId": None}), 400
    
    if rjson["Platform"] != "Quest":
        return jsonify({"ResultCode": 0, "UserId": None}), 400
    
    if rjson["AppId"] != "B7597":
        return jsonify({"ResultCode": 0, "UserId": None}), 400
    
    ticket = rjson["Ticket"]
    user_id = ticket.split('-')[0]
    
    response = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        json={"SessionTicket": ticket},
        headers=settings.get_auth_headers()
    )
    
    if response.status_code != 200:
        return jsonify({"ResultCode": 0, "UserId": None}), 400
    
    return jsonify({"ResultCode": 1, "UserId": user_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1416)
