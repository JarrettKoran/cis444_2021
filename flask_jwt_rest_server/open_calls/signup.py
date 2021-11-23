from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.db_tools import addNewUser
from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")

    newPass = request.form['newPass']
    newUser = request.form['newUser']
    newUser(newUser, newPass)
    user = {
            "sub" : newUser #sub is used by pyJwt as the owner of the token
            }

    return json_response( token = create_token(user) , authenticated = True, username = newUser)
