import requests
import flask
from flask import url_for, request, render_template
from flask_cors import CORS
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "zCU3gbntxqL8kInfTM2Q95jPfkfkVI9Mt8sLNC8NRipq"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = flask.Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def sendhomePage():
    print("home")
    return render_template('home.html')


@app.route('/signupPage', methods=['GET'])
def signupPage():
    print("signup")
    return render_template('signup.html')


@app.route('/index', methods=['GET', 'POST'])
def sendindexPage():
    print("index")
    return render_template('index.html')

# @app.route('/signupfn',methods = ['POST', 'GET'])
# def signupfn():
#    if request.method == 'POST':
#       try:
#          emailid = request.form['emailid']
#          passwrd = request.form['password']
#          usrname = request.form['username']
         
#          with sql.connect("flightdelay.db") as con:
#             cur1 = con.cursor()
#             cur1.execute("select * from user_login where email=?",(emailid))
#             check=cur1.rowcount
#          if(check!=0):
#             error1="User with this Email ID already Exists !!"
#          else:
#             cur = con.cursor()
#             cur.execute("INSERT INTO user_login (email,password,name) VALUES (?,?,?)",(emailid,passwrd,usrname) )
#             con.commit()
#             error1="User Sign Up Successfull ! Proceed Login"
#             flash("Record successfully added!")
#       except:
#          con.rollback()
      
#       finally:
#          return render_template("Signup.html",error=error1)
#          con.close()

# @app.route('/loginfn',methods = ['POST', 'GET'])
# def loginfn():  
#     emailid = request.form["emailid"]
#     passwrd = request.form["password"]  
#     with sql.connect("fligtdelay.db") as con:  
#         try:  
#             cur = con.cursor()  
#             cur.execute("select * from user_login where email=? and password=? limit 1",(emailid,passwrd))  
#             records=cur.fetchall  
#             session['email']=emailid
#             if not records:
#                record1="No Such Users Found"
#             else:
#                record1=records
#         except:  
#             msg = "Incorrect Password / No Such Users Found"  
#         finally:  
#             return render_template("home.html",msg=record1) 


 
@app.route('/predict', methods=['GET','POST'])
def predict():
  print("predict")
  name = request.form['name']
  month = request.form['month']
  dayofmonth = request.form['dayofmonth'] 
  dayofweek = request.form['dayofweek']
  origin = request.form['origin']
  if (origin== "MSP"):  
        origin1, origin2,origin3, origin4, origin5 = 0,0,0,0,1 
  if (origin == "DTW"):
        origin1, origin2,origin3, origin4, origin5 = 1,0,0,0,0
  if (origin == "JFK"):
        origin1, origin2,origin3, origin4, origin5 = 0,0,1,0,0
  if (origin == "SEA"):
        origin1, origin2,origin3, origin4, origin5 = 0,1,0,0,0
  if (origin == "ATL"):
        origin1, origin2, origin3, origin4, origin5 = 0,0,0,1,0
  destination = request.form['destination']
  if (destination == "MSP"):
        destination1, destination2, destination3, destination4, destination5 = 0,0,0,0,1
  if(destination == 'DTW'):
        destination1, destination2, destination3, destination4, destination5 = 1,0,0,0,0
  if (destination == "JFk") :
        destination1, destination2, destination3, destination4, destination5 = 0,0,1,0,0 
  if (destination == "SEA") :
        destination1, destination2, destination3, destination4, destination5 =0,1,0,0,0 
  if (destination == "ATL") :
        destination1, destination2, destination3, destination4, destination5 = 0,0,0,1,0

  dept = request.form['dept']
  arrtime =int(request.form['arrtime'])/100
  actdept = request.form['actdept']
  dept15=int(actdept)- int(dept)
  if (dept15<15):
        dept15=0
  else:
        dept15=1
  print(dept15)
  total = [[name, month, dayofmonth, dayofweek,arrtime,dept15,origin1, origin2, origin3, origin4, origin5, destination1, destination2, destination3, destination4, destination5 ]] 
  payload_scoring = {"input_data": [{"field": [[name, month, dayofmonth, dayofweek,arrtime,dept15,origin1, origin2, origin3, origin4, origin5, destination1, destination2, destination3, destination4, destination5 ]], "values": total}]}
  response_scoring = requests.post('https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/abf3959e-b7bd-4fde-9f34-1295348fea93/predictions?version=2022-11-18', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
  print(response_scoring)
  predictions = response_scoring.json()
  y_pred= predictions['predictions'][0]['values'][0][0]
  print("Final prediction :",predict)
  if(y_pred==[0.]):
       ans= "The Flight will be on time"
  else:
       ans= "The Flight will be delayed"
  return render_template("predict.html", showcase = ans)

    
  

if __name__ == '__main__' :
    app.run(debug= True)
