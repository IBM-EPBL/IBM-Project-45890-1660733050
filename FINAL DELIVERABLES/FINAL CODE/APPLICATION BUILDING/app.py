import pickle 
from flask import Flask,request,render_template

app = Flask(__name__)

#model = pickle.load(open('flightdelay.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    return render_template('inputpage.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
  model = pickle.load(open('flightdelay.pk1','rb'))
  name = request.form['name']
  month = request.form['month']
  dayofmonth = request.form['dayofmonth'] 
  dayofweek = request.form['dayofweek']
  origin = request.form['origin']
  if (origin== "MSP"):  
        originl, origin2,origin3, origin4, orgin5= 0,0,0,0,1 
  if (origin == "DTW"):
        originl, origin2,origin3, origin4, orgin5 = 1,0,0,0,0
  if (origin == "JFK"):
          originl, origin2,origin3, origin4, orgin5 = 0,0,1,0,0
  if (origin == "SEA"):
        originl, origin2,origin3, origin4, orgin5 = 0,1,0,0,0
  if (origin == "ALT"):
        originl, origin2, origin3, origin4, orgin5 = 0,0,0,1,0
  destination = request.form['destination']
  if (destination == "MSP"):
            destinationl, destination2, destination3, destination4, destination5 = 0,0,0,0,1
  if(destination == 'DTW'):
            destinationl, destination2, destination3, destination4, destination5 = 1,0,0,0,0
  if (destination == "JFT") :
          destinationl, destination2, destination3, destination4, destination5 = 0,0,1,0,0 
  if (destination == "SEA") :
         destinationl, destination2, destination3, destination4, destination5 =0,1,0,0,0 
  if (destination == "ALT") :
         destinationl, destination2, destination3, destination4, destination5 = 0,0,0,1,0
  dept = request.form['dept']
  arrtime = request.form['arrtime']
  actdept = request.form['actdept']
  dept15=int(dept)- int(actdept)
  total = [[name, month, dayofmonth, dayofweek,arrtime,actdept,originl, origin2, origin3, origin4, orgin5, destinationl, destination2, destination3, destination4, destination5 ]]

  y_pred = model.predict (total)
  if(y_pred==[0.]):
       ans= "The Flight will be on time"
  else:
       ans= "The Flight will be delayed"
  return render_template("predict.html", showcase = ans)



if __name__ == '__main__':
    app.run(debug=True)
