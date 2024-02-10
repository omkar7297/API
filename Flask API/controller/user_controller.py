from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request
from flask import send_file
from datetime import datetime


obj=user_model()
auth = auth_model()



@app.route("/user/getall")

def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/addone", methods=["POST"])
def user_addone_controller():
    return obj.user_addone_model(request.form)

@app.route("/user/update", methods=["PUT"])

def user_update_controller():
    return obj.user_update_model(request.form)

@app.route("/user/delete/<id>", methods=["DELETE"])

def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route("/user/patch/<id>", methods=["PATCH"])

def user_patch_controller(id):
    return obj.user_patch_controller(request.form,id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods =["GET"])

def user_pagination_controller(limit,page):
    return obj.user_pagination_model(limit,page)



'''---------------------------------------Set this three thing in your terminal ----------------------------------------
export FLASK_APP=app
export FLASK_ENV=DEVELOPMENT
export PYTHONDONTWRITEBYTECODE=1
'''


'''-----------------------This  is a file uploading proccess it is divided int 4 parts which is folowing--------------------

1.uploading file from postman to server.
2.Saving file into the filesystem with unique filname.
3.Updating filepath in database with respective entity.
4.creating an endpoint to read the file.
'''

@app.route("/user/<uid>/upload/avtar",methods=["PUT"])
def user_upload_avtar_controller(uid):
    file = request.files["avtar"]
    unique_filename=str(datetime.now().timestamp()).replace(".","") #Timestamp() it converts all number in numeric form it called as a epoch time format
    fileNameSplit = file.filename.split(".")
    ext = fileNameSplit[len(fileNameSplit)-1]
    finalFilePath =  f"uploads/{unique_filename}.{ext}"
    file.save(f"uploads/{unique_filename}.{ext}") #Save() method save a file
    return obj.user_upload_avtar_model(uid,finalFilePath)


'''-----------------------This function is return a image in browser --------------------'''

@app.route("/uploads/<filename>")    # Host url insert before this end point after hosting   
def user_getavtar_controller(filename):
    return send_file(f"uploads/{filename}")


@app.route("/user/login",methods=["POST"])
def user_login_controller():
    #request.form
    return obj.user_login_model(request.form)  