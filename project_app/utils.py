import config
import pickle
import json
import numpy as np

class MedicalInsurance():
    def __init__(self,age,sex,bmi,children,smoker,region):
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
        self.region = 'region_' + region


    def load_model(self):
        with open(config.MODEL_FILE_PATH,'rb') as f:
            self.model = pickle.load(f)

        with open(config.JSON_FILE_PATH,'r') as f:
            self.json_data = json.load(f)    # project_data


    def get_predict_charges(self):

        self.load_model()

        region_index = self.json_data['columns'].index(self.region)

        test_array = np.zeros(len(self.json_data['columns'])) #9 col 
        test_array[0] = self.age
        test_array[1] = self.json_data['sex'][self.sex]
        test_array[2] = self.bmi
        test_array[3] = self.children
        test_array[4] = self.json_data['smoker'][self.smoker]
        test_array[region_index] = 1

        print('TEST ARRAY:',test_array)  # 9 values

        predicted_charges = self.model.predict([test_array])

        return predicted_charges

if __name__ == '__main__':

    # age = 30.0   
    # sex = 'male'
    # bmi = 28.3
    # children = 2
    # smoker = 'no'
    # region = 'southwest'

    med_ins = MedicalInsurance(age,sex,bmi,children,smoker,region)
    med_ins.get_predict_charges()



