from flask import Flask, render_template, request, session
from pymongo import MongoClient
client = MongoClient("mongodb+srv://abc:abcdefghi@cluster0-6kppu.mongodb.net/test?retryWrites=true&w=majority")
db = client["password"]
mycol = db["details"]

db1= client["student"]
mycol1 = db1["m3"]

db2= client["history"]
mycol2= db2["storage"]

app=Flask(__name__)
app.secret_key="abc"

def func(s):
    x1=mycol.find({"username":s})
    for i in x1:
        print(i["password"])
        return(i["password"])

def func1(s):
    x1=mycol1.find({"request":s})
    for i in x1:

        print(i["response"])
        return(i["response"])

@app.route('/')
def index():
    return render_template("newlogin.html")

@app.route('/home')
def index__():
    return render_template("home.html")

@app.route('/success')
def index__1():
    return render_template("success.html")

@app.route('/register')
def index__2():
    return render_template("newreg.html")

@app.route("/history")
def history():
    if(session["username"]==""):
        return ""
    x5=mycol2.find_one({"name":session["username"]})
    if(x5==None):return " "
    hist={"name":x5["name"],"user":x5["user"],"bot":x5["bot"]}
    return hist

@app.route("/get",methods=["POST"])
def get_bot_response():
    #userText = request.args.get('msg')
    userText=request.json["msg"]
    if userText=="bye":
        session["username"]=""
        return {"response":""}

    message=func1(userText.lower())
    if message==None:
        message="Please enter the correct query or try in a different format"

    if(mycol2.find_one({"name":session["username"]})==None):
        mydict = {"name":session["username"],"user": [userText],"bot":["Hi! I'm darwinbox chatbot.How may I help you!",message]}
        mycol2.insert_one(mydict)
    else:
        mycol2.update_one({"name":session["username"]}, {"$push":{"user":userText,"bot":message}})

    if message:
        #return message
        return {"ans":message}
    return({"ans":"Please enter the correct query or try in a different format"})
@app.route('/validate',methods=['POST'])
def getvalue():
    data=request.json

    pwds=data["password"]
    name=data["name"]
    if(pwds==func(name)):
        session["username"]=name
        return({"status":"valid"})
    else:
        return ({"status":"invalid"})
@app.route("/signup",methods=["POST"])
def asd():
    data = request.json
    pwds = data["password"]
    name = data["name"]
    # print(name,pwds)
    mydict = {"username": name, "password": pwds}
    x2 = mycol.insert_one(mydict)
    return ({"status": "registered"})
if __name__=="__main__":
    app.run(debug=True)
