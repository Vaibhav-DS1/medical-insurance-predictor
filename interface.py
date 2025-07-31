from flask import Flask,render_template,jsonify,request
import config
from project_app.utils import MedicalInsurance

app = Flask(__name__)

@app.route('/') #Home API
def hello_Flask():
    print("Welcome to Flask")
    return "Hello Python"


@app.route('/predict_charges')

def get_insurance_charges():
    data = request.form
    print("Data is:",data)
    age = eval(data['age'])
    sex = data['sex']
    bmi = eval(data['bmi'])
    children = eval(data['children'])
    smoker = data['smoker']
    region = data['region']

    # print("age,sex,bmi,children,smoker,region:>>",age,sex,bmi,children,smoker,region)

    med_ins = MedicalInsurance(age,sex,bmi,children,smoker,region)
    charges = med_ins.get_predict_charges()

    return jsonify({'Result':f"Predicted Medical Insurance Charges are: {charges}"})

app.run(port = config.PORT_NUMBER,debug = 'False')