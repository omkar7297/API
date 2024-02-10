import mysql.connector
from flask import make_response,request
from functools import wraps
import json
import jwt
import re


class auth_model():
    def __init__(self):

        # connection established code

        try:
            self.con = mysql.connector.connect(host="localhost",user="root",password="",database="flask_tutorial")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True) 
            print("Database connected")
        except:
            print("Some error")

    def token_auth(self, endpoint):
        def inner1(func):
            @wraps(func)#n Python, they're called decorators. Decorators allow us to extend the behavior of a function or a class without changing the original implementation of the wrapped function.
            def inner2(*args):
                authorization = request.headers.get("authorization") #get incryption key
                if re.match("^Bearer *([^ ]+) *$",authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwtdecoded = jwt.decode(token,"Omkar", algorithms="HS256") #2nd parameter is encryption key 
                    except jwt.ExpiredSignatureError:
                        return make_response({"Error":"Token Expired"},401)
                    #here the apply algorithms=["HS256"] like theat but we are not using same pattern in the use_model file
                    role_id = jwtdecoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessbility_view WHERE endpoint = '{endpoint}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        allowed_roles = json.loads(result[0]['roles']) #json.loads() it returns the string without '' 
                        if role_id in allowed_roles:
                            return func(*args)
                        else:
                            return make_response({"Error":"Invalid Role...."},401)
                    else:
                        return make_response({"Error":"UNKNOWN _ENDPOINT"})
                else:
                    return make_response({"Erreo":"Invalid Token"},401)
            
            return inner2
        return inner1 