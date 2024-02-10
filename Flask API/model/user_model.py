import mysql.connector
import json
from flask import make_response
from datetime import datetime,timedelta
import jwt


class user_model():
    def __init__(self):

        # connection established code

        try:
            self.con = mysql.connector.connect(host="localhost",user="root",password="",database="flask_tutorial")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True) 
            print("Database connected")
        except:
            print("Some error")

    #'''------------------------------Get All item API------------------------------ ''' 
                    
    def user_getall_model(self):

        # Query exicution

        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()  #fetchall-it returns all the result value after execute the sql query 
        if len(result)>0:

            # return json.dumps(result) [this is return data as text and html form]
            res = make_response({"payrole":result},200) # make_response is used for  Its purpose is to create an HTTP response object that can be customized before sending it back to the client's browser
            res.headers['access-control-Allow-Origin'] = "*"   # This process is access-control-Allow-Origin
            #the line 20,21 is working if a request is getting from any origin so allow to give them response
            return res 
        #[there make_response({"payrole":result},200) is return data as json form]
        else:
            return make_response({"msg":"No data Found"},204)

    #'''------------------------------Add one item API------------------------------ '''   
              
    def user_addone_model(self,data):

        #Value binding process

        self.cur.execute(f"INSERT INTO flask_tutorial.users (name, email, phone, role, password) VALUES ('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')")
        print(data)
        return make_response({"msg":"User added successfully"},201)

    #'''------------------------------Update item by put method API------------------------------ '''   
      
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}',role='{data['role']}', password='{data['password']}' where id = {data['id']}")
        if self.cur.rowcount>0:
            return make_response({"msg":"User updated"},201)
        else:
            return make_response({"msg":"nothing to update"},202)
        

    #'''------------------------------Update item by put method API------------------------------ '''
   
    def user_patch_controller(self,data,id):

    # Dynamically create Sql Query based on the above query
    #self.cur.execute("UPDATE users SET name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role']}',password='{data['password'}' where id = {id }")
      

        '''it not take one argument at one time'''
        qry = "UPDATE users SET "

        if len(data) == 1:
            key, value = next(iter(data.items()))
            qry += f"{key}='{value}'"
        else:
            for key in data:
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1]+f" where id = {id}"
    #Query execution
            
        print(qry)
        self.cur.execute(qry)
        if self.cur.rowcount > 0:
            return {"msg":"Record updated successfully!!"}
        else:
             return {"msg":"Nothing to update"}

    #'''------------------------------Delete item by id API------------------------------ ''' 
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE FROM users where id ={id}")
        if self.cur.rowcount > 0:
            return make_response({"msg":"User Deleted"},20)
        else:
            return make_response({"msg":"Nothing to delete"},202)


    #'''------------------------------pagination process method API------------------------------ ''' 
    
    def user_pagination_model(self,limit,page):
        limit =int(limit)
        page = int(page)
        start = (limit*page)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            res = make_response({"playload":result, "page No":page,"limit":limit}, 200)
            return res
        else:
            return make_response({"msg":"NO data found"},204)   
        
    def user_upload_avtar_model(self,uid,filePath):
        self.cur.execute(f"UPDATE users SET avtar = '{filePath}' WHERE ID = {uid}")
        if self.cur.rowcount>0:
            return make_response({"msg":"File Uploaded Succssfully!!!", "File_PATH":filePath},201)
        else:
            return make_response({"msg":"Nothing to upload"}),202


    def user_login_model(self,data):
        self.cur.execute(f"SELECT id, name, email, phone, avtar,role_id FROM users WHERE email = '{data['email']}' and password = '{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now()+timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp()) 
        payload = {
            "payload":userdata,
            "exp":exp_epoch_time
            }
        
        jwttoken     = jwt.encode(payload,"Omkar",algorithm="HS256")   # "Omkar"it is incription key
        return make_response({"token":jwttoken},200) 